"""Strips publisher boilerplate from fetched articles before they are stored.

Feeds and scraped pages carry the publisher's own marketing: "Follow us on WhatsApp",
app-download prompts, subscription and comment-policy text, copyright lines, journalist
biographies and paid adverts. None of that belongs on VidiaNews, and none of it is news.

The rules are deliberately conservative: whole paragraphs are dropped only when they match
a promotional pattern, and a publisher's name is never rewritten inside a sentence, because
"told BBC News" or "NDTV World Summit" is part of the story. Original source names and URLs
stay in the database columns; this module only touches reader-facing text.
"""

import re
from typing import Iterable, List, Optional

BRAND = "VidiaNews"

# Whole paragraphs (or lines) that are promotion, site furniture or credit lines.
_PROMO_PARAGRAPH = re.compile(
    r"""(?ix)
    (?:
      # calls to follow / join / download
      ^(?:stay\s+\w+!?\s+)?(?:please\s+)?(?:follow|join|like)\b.{0,60}\b(?:on|via)\s+(?:whatsapp|telegram|facebook|instagram|twitter|x|youtube|tiktok|google\s+news|linkedin)\b
    | ^follow\s+(?:us|the\s+\w+(?:\s+\w+){0,3})\s+on\b
    | \b(?:download|get|install)\b.{0,40}\b(?:app|apps)\b.{0,30}\b(?:app\s+store|google\s+play|now)\b
    | \bdownload\s+(?:the\s+)?[\w\s]{0,30}\bapp\b
    | \bwhatsapp\s+(?:channel|group|community)\b
    | \b(?:subscribe|sign\s+up)\b.{0,60}\b(?:newsletter|channel|updates|alerts|podcast|youtube|bulletin|digest)\b
    | \b(?:newsletter|breaking\s+news\s+alerts?)\b.{0,40}\b(?:sign\s+up|subscribe|delivered|inbox)\b
    | \bcheck\s+your\s+inbox\b
    | \bclick\s+(?:here|the\s+link|to\s+(?:read|subscribe|join|download|start|watch|follow))\b
    | \bpreferred\s+source\s+on\s+google\b
    | \bsupport\s+(?:our|the)\s+(?:journalism|work|reporting)\b
    | \b(?:become|a)\s+(?:a\s+)?(?:member|subscriber)\b.{0,40}\b(?:today|now)\b
    | \bsubscription\s+benefits\b
    | \binstitutional\s+subscriber\b
    | ^terms\s*(?:&|and)\s*conditions\b.{0,40}$
    | \babide\s+by\s+our\s+community\s+guidelines\b
    | \bcommenting\s+platform\b
    | \bcomments\s+have\s+to\s+be\b
    | \ball\s+(?:content\s+is\s+)?(?:rights\s+reserved|copyrighted)\b
    | ©|\bcopyright\b.{0,30}\b(?:19|20)\d\d
    | \bplease\s+enable\s+javascript\b|\benable\s+javascript\b
    | \bthis\s+(?:article|story|report|piece)\s+(?:was\s+)?(?:originally\s+)?(?:written|published|translated|reported|appeared)\s+(?:in|from|by|on)\b.{0,40}$
    | \bthis\s+article\s+was\s+translated\s+from\b
    | \bdiscover\s+the\s+stories\s+of\s+progress\b
    | \bgo\s+to\s+\S+\.com\b.{0,40}\bfor\s+more\s+news\b
    | \bfollow\s+bbc\b
    | \bbbc\s+indepth\s+is\s+the\s+home\b
    | \blisten\s+to\s+the\s+latest\b.{0,40}\bpodcast\b
    | \bwatch\s+(?:the\s+)?(?:full\s+)?(?:video|live|more)\b.{0,10}$
    | ^(?:advertisement|advertorial|sponsored(?:\s+content)?|promoted|ad)\s*:?\s*$
    | ^(?:read\s+(?:also|more)|also\s+read|related(?:\s+(?:news|stories|articles))?|see\s+also|trending|recommended|more\s+on\s+this)\b\s*:
    | ^(?:published|updated|first\s+published|last\s+updated)\s*[-:–]\s*\w+\s+\d{1,2},?\s+\d{4}.{0,60}$
    | ^attention\s+\w+\s*:
    | \bpremium\s+domains?\b
    | \b(?:buy|acquire|register)\b.{0,30}\bdomains?\b.{0,60}\b(?:profit|earn|\$)
    | \bstay\s+(?:informed|in\s+the\s+know|updated)\b.{0,80}\b(?:follow|download|join|subscribe|app|alerts|whatsapp)\b
    | \bphoto\s*(?:credit|:)\b.{0,80}$
    | ^\(?(?:photo|image|pic|picture|credit|source)\s*(?:credit|courtesy)?\s*:.{0,100}\)?$
    | ^(?:by|words\s+by|story\s+by|reporting\s+by|additional\s+reporting\s+by|with\s+additional\s+reporting\s+by|writing\s+by|editing\s+by|compiled\s+by)\s+[A-Z][\w'’.-]+(?:\s+[A-Z][\w'’.-]+){0,4}(?:\s*(?:,|and|&)\s+[A-Z][\w'’.-]+(?:\s+[A-Z][\w'’.-]+){0,3})*\.?$
    )
    """)

# "<Name> is a journalist/reporter/editor ..." biographies printed under or above an article.
_BIO_PARAGRAPH = re.compile(
    r"""(?ix)
    ^[A-Z][\w'’.-]+(?:\s+[A-Z][\w'’.-]+){0,3}\s+(?:is|has\s+been|serves\s+as|works\s+as)\s+
    (?:a|an|the)\s+(?:[\w\-,]+\s+){0,5}?
    (?:journalist|reporter|correspondent|editor|sub-?editor|writer|columnist|contributor|broadcaster|producer|anchor)\b
    """)

# "With three years of experience, Stephen, The PUNCH correspondent, has been covering ..."
_BIO_EXPERIENCE = re.compile(
    r"(?i)\b(?:years?|decade)s?\s+(?:of\s+)?(?:professional\s+)?(?:reporting\s+)?experience\b.{0,200}\b(?:correspondent|reporter|journalist|covering|has\s+been\s+covering)\b")
_PUBLISHER_CORRESPONDENT = re.compile(r"(?i)\bthe\s+(?:punch|vanguard|premium\s+times|hindu|nation)\s+(?:correspondent|reporter|journalist)\b")

# Sign-off a publisher glues onto the last sentence: "... delayed. Vanguard News"
_SIGNOFF = re.compile(
    r"(?i)(?<=[.!?\"”’])\s+(?:vanguard(?:\s+news)?|punch(?:\s+news)?|the\s+punch|premium\s+times|channels\s+tv|the\s+hindu|"
    r"myjoyonline(?:\.com)?|capital\s+fm|nation\s+africa)\s*$")

_BIO_HINT = re.compile(
    r"(?i)\b(?:covers|covering|beats?|years?\s+(?:of\s+)?experience|reports?\s+on|joined\s+(?:the|us)|"
    r"newsroom|contact\s+(?:him|her|them)|reach\s+(?:him|her|them)|follow\s+(?:him|her|them)|@\w+)\b")

# Sentences cut out of an otherwise legitimate paragraph.
_PROMO_SENTENCE = re.compile(
    r"""(?ix)
    (?:^|(?<=[.!?])\s+)
    (?:
      (?:stay\s+(?:informed|updated|in\s+the\s+know)[^.!?]{0,160}?(?:whatsapp|download|follow|subscribe|app|alerts)[^.!?]*[.!?]+)
    | (?:follow\s+(?:the\s+\w+\s+)?[\w\s]{0,40}?on\s+(?:whatsapp|telegram|facebook|instagram|twitter|youtube|tiktok|x)\b[^.!?]*[.!?]*)
    | (?:download\s+the\s+[\w\s]{0,40}?app\b[^.!?]*[.!?]*)
    | (?:click\s+here\b[^.!?]*[.!?]*)
    | (?:join\s+(?:our|the)\s+[\w\s]{0,30}?(?:channel|group|community|newsletter)\b[^.!?]*[.!?]*)
    | (?:sign\s+up\s+(?:for|to)\s+(?:our|the)\s+[\w\s]{0,40}?(?:newsletter|alerts)\b[^.!?]*[.!?]*)
    | (?:don['’]t\s+miss\s+a\s+headline[^.!?]*[.!?]*)
    )
    """)

# Parenthetical credits that name the publisher: "(PHOTO CREDIT: PREMIUM TIMES)".
_CREDIT_PAREN = re.compile(r"(?i)\s*[\(\[]\s*(?:photo|image|pic|picture)?\s*(?:credit|courtesy|source)\s*:[^)\]]{0,80}[\)\]]")
# Photographer / agency credit trailing an image caption: "Caption text. | Photo Credit: PTI".
_CREDIT_TAIL = re.compile(r"(?i)\s*\|?\s*(?:photo|image|pic|picture)(?:\s+credit)?\s*:.*$")
# BBC feeds mark every link with a trailing ", external".
_EXTERNAL_MARK = re.compile(r",\s*external(?=[\s,.;:!?)]|$)")
_STRAY_BULLET = re.compile(r"^[\s•·*\-–—|]+$")

# Trailing site names in headlines: "... - The Punch", "... | BBC News".
_TITLE_SUFFIX = re.compile(
    r"\s*[\|\-–—:]\s*(?:the\s+)?(?:punch(?:\s+(?:news|newspapers?|nigeria))?|premium\s+times|vanguard(?:\s+news)?|"
    r"channels(?:\s+tv|\s+television)?|bbc(?:\s+news|\s+africa)?|the\s+hindu|ndtv(?:\.com)?|al\s+jazeera|"
    r"the\s+guardian|sky\s+news|npr|dw(?:\.com)?|abc\s+news|myjoyonline(?:\.com)?|joy\s+(?:news|online)|"
    r"nation(?:\s+africa)?|capital\s+fm|nairaland)\s*$", re.I)
_TITLE_PREFIX = re.compile(r"^\s*(?:punch|premium\s+times|vanguard|channels\s+tv|bbc\s+news)\s*[:|\-–—]\s+", re.I)
# The Guardian appends the columnist or series to headlines: "... | Margaret Sullivan".
_GUARDIAN_TAIL = re.compile(r"\s+\|\s+[^|]{1,45}$")

_WS = re.compile(r"[ \t ]+")
_SPACE_BEFORE_PUNCT = re.compile(r"\s+([,.;:!?])")


def _is_junk_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped or _STRAY_BULLET.match(stripped):
        return True
    if _PROMO_PARAGRAPH.search(stripped) and len(stripped) <= 420:
        return True
    if _BIO_PARAGRAPH.match(stripped) and (len(stripped) <= 900 and _BIO_HINT.search(stripped)):
        return True
    if len(stripped) <= 500 and (_BIO_EXPERIENCE.search(stripped) or _PUBLISHER_CORRESPONDENT.search(stripped)) and (
            _BIO_HINT.search(stripped) or _PUBLISHER_CORRESPONDENT.search(stripped)):
        return True
    return False


def clean_paragraph(text: str, source_key: Optional[str] = None) -> str:
    """Clean one paragraph; returns '' when nothing worth keeping is left."""
    text = _CREDIT_PAREN.sub("", text)
    text = _CREDIT_TAIL.sub("", text)
    if source_key and source_key.startswith("bbc"):
        text = _EXTERNAL_MARK.sub("", text)
    text = _SIGNOFF.sub("", _WS.sub(" ", text).strip())
    if _is_junk_line(text):
        return ""
    # Long paragraph with promo sentences embedded: remove just those sentences.
    cleaned = _PROMO_SENTENCE.sub(" ", text)
    if cleaned != text:
        cleaned = _SPACE_BEFORE_PUNCT.sub(r"\1", _WS.sub(" ", cleaned)).strip()
        if len(cleaned) < 25:
            return ""
        text = cleaned
    return text


def clean_body(text: Optional[str], source_key: Optional[str] = None) -> str:
    """Clean article text made of paragraphs separated by blank lines (or a single block)."""
    if not text:
        return ""
    kept: List[str] = []
    for block in re.split(r"\n\s*\n", text):
        for line in (block.split("\n") if "\n" in block.strip() else [block]):
            para = clean_paragraph(line, source_key)
            if para and (not kept or kept[-1] != para):
                kept.append(para)
    return "\n\n".join(kept)


def clean_title(title: Optional[str], source_key: Optional[str] = None) -> str:
    if not title:
        return ""
    out = _WS.sub(" ", title).strip()
    for _ in range(2):
        out = _TITLE_SUFFIX.sub("", out).strip()
    out = _TITLE_PREFIX.sub("", out).strip()
    if source_key == "guardian_uk":
        out = _GUARDIAN_TAIL.sub("", out).strip()
    return out or title.strip()


def clean_summary(text: Optional[str], source_key: Optional[str] = None) -> Optional[str]:
    if not text:
        return text
    return clean_body(text, source_key).replace("\n\n", " ") or None


def is_blank_after_cleaning(text: Optional[str], source_key: Optional[str] = None) -> bool:
    return not clean_body(text, source_key)


def brand_tagline() -> str:
    """The only promotional wording we ever add: a plain statement, no invented channels or services."""
    return f"Stay informed with {BRAND}."


def strip_publisher_names(text: str, names: Iterable[str]) -> str:
    """Remove a publisher's name from machine-written text (descriptions), never from story text."""
    for name in sorted({n for n in names if n}, key=len, reverse=True):
        text = re.sub(rf"(?i)\b{re.escape(name)}\b", BRAND, text)
    return text
