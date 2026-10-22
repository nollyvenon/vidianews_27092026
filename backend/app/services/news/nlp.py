"""NLP enrichment for news articles.

Uses spaCy (en_core_web_sm) for entities, keywords, topics and sentence
splitting when it is installed, and falls back to a rule-based pipeline
(gazetteer + frequency) when it is not. Summaries are extractive: sentences
are selected from the article text, never invented. The "description" is a
templated context line built from the extracted entities.

None of this is fact checking; see validation.py for what is and is not checked.
"""

import logging
import re
import threading
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Sequence

_log = logging.getLogger(__name__)

CATEGORIES = [
    "politics", "business", "sports", "technology", "entertainment",
    "health", "science", "world", "crime", "education", "lifestyle", "general",
]

_CATEGORY_LEXICON: Dict[str, List[str]] = {
    "politics": ["election", "senate", "senator", "president", "governor", "minister", "parliament",
                 "government", "apc", "pdp", "inec", "lawmaker", "legislat", "campaign", "vote", "ballot",
                 "congress", "democrat", "republican", "politic", "cabinet", "tinubu", "policy", "assembly",
                 "prime minister", "white house", "downing street"],
    "business": ["economy", "economic", "inflation", "naira", "dollar", "market", "stock", "bank", "cbn",
                 "business", "investor", "investment", "oil price", "crude", "trade", "tax", "revenue",
                 "company", "profit", "shares", "gdp", "budget", "tariff", "earnings", "fintech", "startup"],
    "sports": ["football", "match", "league", "goal", "coach", "player", "tournament", "cup", "olympic",
               "super eagles", "premier league", "champions league", "nba", "fifa", "cricket", "tennis",
               "athlete", "boxing", "world cup", "striker", "transfer"],
    "technology": ["technology", "tech", "software", "ai ", "artificial intelligence", "app", "cyber",
                   "internet", "smartphone", "google", "apple", "microsoft", "meta ", "openai", "robot",
                   "data breach", "hackers", "chip", "semiconductor", "startup"],
    "entertainment": ["movie", "film", "nollywood", "music", "album", "singer", "actor", "actress",
                      "celebrity", "box office", "netflix", "concert", "bbnaija", "award", "grammy",
                      "oscar", "festival", "showbiz", "tv series"],
    "health": ["health", "hospital", "disease", "virus", "outbreak", "vaccine", "doctor", "patients",
               "who ", "cancer", "malaria", "cholera", "lassa", "medical", "nurse", "drug", "covid", "mental health"],
    "science": ["scientist", "research", "study finds", "nasa", "space", "climate", "planet", "species",
                "discovery", "telescope", "physics", "biology", "fossil", "asteroid", "satellite"],
    "crime": ["police", "arrest", "kill", "murder", "robbery", "kidnap", "bandit", "court", "convict",
              "jail", "prison", "trial", "suspect", "attack", "gunmen", "terror", "fraud", "efcc",
              "shooting", "charged", "sentenced"],
    "education": ["school", "university", "student", "teacher", "asuu", "exam", "waec", "jamb", "neco",
                  "tuition", "college", "lecturer", "scholarship", "education", "polytechnic"],
    "lifestyle": ["fashion", "food", "recipe", "travel", "wedding", "relationship", "fitness", "beauty",
                  "lifestyle", "home", "parenting", "culture", "religion", "church"],
    "world": ["war", "ukraine", "russia", "gaza", "israel", "united nations", "nato", "summit", "diplomat",
              "sanctions", "refugee", "embassy", "european union", "middle east", "china"],
}

_LEXICON_RES = {
    cat: re.compile("|".join(r"(?<![a-z])" + re.escape(w) for w in words), re.I)
    for cat, words in _CATEGORY_LEXICON.items()
}

# Gazetteer: name/demonym/major city -> ISO country code. Used to tag stories that
# are about a country regardless of which outlet published them.
_COUNTRY_TERMS: Dict[str, List[str]] = {
    "NG": ["nigeria", "nigerian", "nigerians", "lagos", "abuja", "kano", "port harcourt", "ibadan", "kaduna",
           "enugu", "naija", "naira", "tinubu", "super eagles"],
    "US": ["united states", "u.s.", "american", "washington", "new york", "california", "texas", "white house",
           "congress", "pentagon"],
    "GB": ["britain", "british", "united kingdom", "uk ", "london", "england", "scotland", "wales", "downing street"],
    "ZA": ["south africa", "south african", "johannesburg", "cape town", "pretoria"],
    "KE": ["kenya", "kenyan", "nairobi", "mombasa"],
    "GH": ["ghana", "ghanaian", "accra", "kumasi"],
    "IN": ["india", "indian", "delhi", "mumbai", "bengaluru", "modi"],
    "CA": ["canada", "canadian", "ottawa", "toronto", "vancouver"],
    "AU": ["australia", "australian", "sydney", "melbourne", "canberra"],
    "DE": ["germany", "german", "berlin"],
    "FR": ["france", "french", "paris"],
    "EG": ["egypt", "egyptian", "cairo"],
    "CN": ["china", "chinese", "beijing", "shanghai"],
    "RU": ["russia", "russian", "moscow", "kremlin"],
    "BR": ["brazil", "brazilian", "brasilia"],
    "JP": ["japan", "japanese", "tokyo"],
    "AE": ["dubai", "abu dhabi", "emirates"],
    "IE": ["ireland", "irish", "dublin"],
}
_COUNTRY_RES = {
    code: re.compile("|".join(r"(?<![a-z])" + re.escape(t) + r"(?![a-z])" for t in terms), re.I)
    for code, terms in _COUNTRY_TERMS.items()
}

_STOP = set("""a an and are as at be been but by for from has have he her his i in is it its of on or she
that the their them they this to was were will with you your we our not no yes after before over under
about into out up down more most said says say new year years day days one two three also than then when
where which who whom what why how can could would should may might just like get got make made week
monday tuesday wednesday thursday friday saturday sunday today yesterday""".split())

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(])")
_WORD = re.compile(r"[A-Za-z][A-Za-z'-]{2,}")


@dataclass
class NlpResult:
    category: str = "general"
    keywords: List[str] = field(default_factory=list)
    topics: List[str] = field(default_factory=list)
    people: List[str] = field(default_factory=list)
    organizations: List[str] = field(default_factory=list)
    locations: List[str] = field(default_factory=list)
    mentioned_countries: List[str] = field(default_factory=list)
    summary: str = ""
    description: str = ""
    engine: str = "rules"


_nlp = None
_nlp_lock = threading.Lock()
_nlp_failed = False


def _load_spacy():
    """Load the spaCy pipeline once; return None if unavailable."""
    global _nlp, _nlp_failed
    if _nlp is not None or _nlp_failed:
        return _nlp
    with _nlp_lock:
        if _nlp is not None or _nlp_failed:
            return _nlp
        try:
            import spacy
            _nlp = spacy.load("en_core_web_sm")
            _log.info("spaCy en_core_web_sm loaded")
        except Exception as exc:  # noqa: BLE001
            _nlp_failed = True
            _log.warning("spaCy unavailable (%r); using rule-based NLP fallback", exc)
    return _nlp


def spacy_available() -> bool:
    return _load_spacy() is not None


def _clean_entity(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip(" ,.;:'\"()[]")
    text = re.sub(r"^(the|The)\s+", "", text)
    text = re.sub(r"'s$", "", text)
    return text


def _dedupe_ranked(values: Sequence[str], limit: int) -> List[str]:
    counts = Counter(v for v in values if 2 <= len(v) <= 60)
    # collapse "Tinubu" into "Bola Tinubu" when the longer form is also present
    names = sorted(counts, key=lambda n: (-counts[n], len(n)))
    kept: List[str] = []
    for name in names:
        low = name.lower()
        if any(low == k.lower() or low in k.lower().split() for k in kept):
            continue
        kept.append(name)
        if len(kept) >= limit:
            break
    return kept


def _classify(title: str, body: str, feed_categories: Sequence[str], default: Optional[str]) -> str:
    scores: Counter = Counter()
    feed_text = " ".join(feed_categories)
    for cat, rx in _LEXICON_RES.items():
        scores[cat] += 4 * len(rx.findall(title)) + len(rx.findall(body[:2500])) + 3 * len(rx.findall(feed_text))
    if default in scores:
        scores[default] += 1
    best, score = scores.most_common(1)[0] if scores else ("general", 0)
    return best if score >= 2 else (default or "general")


def _countries_in(text: str) -> List[str]:
    return [code for code, rx in _COUNTRY_RES.items() if rx.search(text)]


def _split_sentences(text: str, doc=None) -> List[str]:
    if doc is not None:
        sents = [s.text.strip() for s in doc.sents]
    else:
        sents = _SENT_SPLIT.split(text)
    return [s for s in (x.strip() for x in sents) if len(s) >= 25]


def _summarize(sentences: List[str], keyword_weights: Counter, title: str, entity_names: Sequence[str]) -> str:
    if not sentences:
        return ""
    title_l = title.lower().strip(" .")
    sentences = [s for s in sentences if s.lower().strip(" .") != title_l]
    if not sentences:
        return ""
    if len(sentences) <= 2:
        return " ".join(sentences)[:600]
    ents = [e.lower() for e in entity_names]
    scored = []
    for idx, sent in enumerate(sentences):
        words = [w.lower() for w in _WORD.findall(sent)]
        if not words:
            continue
        score = sum(keyword_weights.get(w, 0) for w in words) / (len(words) ** 0.6)
        score += 1.5 * sum(1 for e in ents if e in sent.lower())
        if idx == 0:
            score *= 1.4
        scored.append((score, idx, sent))
    top = sorted(scored, reverse=True)[:2]
    summary = " ".join(s for _, _, s in sorted(top, key=lambda t: t[1]))
    return summary[:600].rsplit(" ", 1)[0] + "…" if len(summary) > 600 else summary


def _describe(res: NlpResult, source_name: str, published_at: Optional[datetime]) -> str:
    parts = [f"{res.category.capitalize()} report from {source_name}"]
    if published_at:
        parts[0] += f", published {published_at.strftime('%d %b %Y')}"
    parts[0] += "."
    if res.people:
        parts.append("People mentioned: " + ", ".join(res.people[:3]) + ".")
    if res.organizations:
        parts.append("Organizations: " + ", ".join(res.organizations[:3]) + ".")
    if res.locations:
        parts.append("Places: " + ", ".join(res.locations[:3]) + ".")
    if res.topics:
        parts.append("Topics: " + ", ".join(res.topics[:4]) + ".")
    return " ".join(parts)


def _analyze_rules(title: str, body: str) -> NlpResult:
    res = NlpResult(engine="rules")
    text = f"{title}. {body}"
    freq = Counter(w.lower() for w in _WORD.findall(text) if w.lower() not in _STOP)
    for w in _WORD.findall(title):
        if w.lower() not in _STOP:
            freq[w.lower()] += 2
    res.keywords = [w for w, _ in freq.most_common(8)]
    res.topics = res.keywords[:4]
    for code in _countries_in(text):
        res.mentioned_countries.append(code)
    res.locations = [t.title() for code in res.mentioned_countries for t in _COUNTRY_TERMS[code][:1]]
    return res


def _analyze_spacy(nlp, title: str, body: str) -> NlpResult:
    res = NlpResult(engine="spacy")
    text = f"{title}. {body}"[:4000]
    doc = nlp(text)
    people, orgs, locs = [], [], []
    for ent in doc.ents:
        name = _clean_entity(ent.text)
        if len(name) < 2 or name.lower() in _STOP:
            continue
        if ent.label_ == "PERSON":
            people.append(name)
        elif ent.label_ == "ORG":
            orgs.append(name)
        elif ent.label_ in ("GPE", "LOC", "FAC"):
            locs.append(name)
    res.people = _dedupe_ranked(people, 6)
    res.organizations = _dedupe_ranked(orgs, 6)
    res.locations = _dedupe_ranked(locs, 6)

    title_words = {w.lower() for w in _WORD.findall(title)}
    freq: Counter = Counter()
    for tok in doc:
        if tok.is_stop or tok.is_punct or not tok.is_alpha or len(tok.text) < 3:
            continue
        if tok.pos_ not in ("PROPN", "NOUN"):
            continue
        lemma = tok.lemma_.lower() if tok.pos_ == "NOUN" else tok.text.lower()
        if lemma in _STOP:
            continue
        freq[lemma] += 2 if lemma in title_words else 1
    res.keywords = [w for w, _ in freq.most_common(8)]

    chunks: Counter = Counter()
    for chunk in doc.noun_chunks:
        words = [t for t in chunk if not (t.is_stop or t.is_punct or t.pos_ in ("PRON", "DET"))]
        if not words or len(words) > 3:
            continue
        phrase = " ".join(t.text for t in words).strip().lower()
        if len(phrase) < 4 or phrase in _STOP:
            continue
        chunks[phrase] += 2 if any(w.lower() in phrase for w in title_words) else 1
    res.topics = [p for p, _ in chunks.most_common(5)]
    res._doc = doc  # type: ignore[attr-defined]  # reused for sentence splitting
    return res


def analyze(title: str, content: str, feed_categories: Sequence[str] = (), source_name: str = "",
            published_at: Optional[datetime] = None, default_category: Optional[str] = None) -> NlpResult:
    body = content or ""
    nlp = _load_spacy()
    try:
        res = _analyze_spacy(nlp, title, body) if nlp else _analyze_rules(title, body)
    except Exception as exc:  # noqa: BLE001 - never let NLP failure drop an article
        _log.warning("NLP failed for %r: %r", title[:60], exc)
        res = _analyze_rules(title, body)

    doc = getattr(res, "_doc", None)
    res.mentioned_countries = _countries_in(f"{title} {body} {' '.join(res.locations)}")
    res.category = _classify(title, body, feed_categories, default_category)

    sentences = _split_sentences(body, doc)
    weights = Counter({k: 3 - min(i, 2) for i, k in enumerate(res.keywords)})
    for w in res.keywords:
        weights[w] += 1
    res.summary = _summarize(sentences, weights, title, res.people + res.organizations + res.locations)
    res.description = _describe(res, source_name or "the source", published_at)
    if hasattr(res, "_doc"):
        del res._doc
    return res


def analyze_many(items: Sequence[dict]) -> List[NlpResult]:
    """Synchronous batch helper (run it in a worker thread)."""
    return [analyze(**item) for item in items]
