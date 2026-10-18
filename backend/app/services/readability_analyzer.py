"""Readability metrics computed from text with the published formulas.

Flesch Reading Ease and Flesch-Kincaid Grade (Flesch, 1948; Kincaid et al., 1975), Gunning Fog
(Gunning, 1952), and SMOG (McLaughlin, 1969). Syllables are counted with a vowel-group heuristic,
which is the usual approximation for these formulas.
"""

import math
import re
from dataclasses import dataclass
from typing import List

WORD_PATTERN = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
SENTENCE_SPLIT = re.compile(r"[.!?]+")
VOWEL_GROUP = re.compile(r"[aeiouy]+")


@dataclass(frozen=True)
class ReadabilityMetrics:
    word_count: int
    sentence_count: int
    paragraph_count: int
    flesch_reading_ease: float
    flesch_kincaid_grade: float
    gunning_fog_index: float
    smog_index: float
    avg_word_length: float
    avg_sentence_length: float
    readability_level: str
    target_audience_grade_level: str
    complexity_score: float


def count_syllables(word: str) -> int:
    """Vowel-group syllable estimate; every word has at least one syllable."""
    lowered = word.lower()
    groups = len(VOWEL_GROUP.findall(lowered))
    if lowered.endswith("e") and groups > 1 and not lowered.endswith(("le", "ee")):
        groups -= 1
    return max(1, groups)


def _level_for(reading_ease: float) -> str:
    if reading_ease >= 80:
        return "Easy"
    if reading_ease >= 60:
        return "Moderate"
    if reading_ease >= 30:
        return "Difficult"
    return "Very Difficult"


def analyze(text: str) -> ReadabilityMetrics:
    """Compute readability metrics for a piece of text.

    Raises ValueError when the text contains no words, because no ratio can be formed.
    """
    words: List[str] = WORD_PATTERN.findall(text)
    if not words:
        raise ValueError("The text has no words to analyse")

    sentences = [part for part in SENTENCE_SPLIT.split(text) if WORD_PATTERN.search(part)]
    sentence_count = max(1, len(sentences))
    paragraph_count = max(1, len([block for block in re.split(r"\n\s*\n", text) if block.strip()]))

    word_count = len(words)
    syllables = [count_syllables(word) for word in words]
    total_syllables = sum(syllables)
    polysyllables = sum(1 for count in syllables if count >= 3)

    words_per_sentence = word_count / sentence_count
    syllables_per_word = total_syllables / word_count

    reading_ease = 206.835 - 1.015 * words_per_sentence - 84.6 * syllables_per_word
    kincaid_grade = 0.39 * words_per_sentence + 11.8 * syllables_per_word - 15.59
    fog = 0.4 * (words_per_sentence + 100 * (polysyllables / word_count))
    smog = 1.043 * math.sqrt(polysyllables * (30 / sentence_count)) + 3.1291

    grade = max(1, round(kincaid_grade))
    avg_word_length = sum(len(word) for word in words) / word_count

    return ReadabilityMetrics(
        word_count=word_count,
        sentence_count=sentence_count,
        paragraph_count=paragraph_count,
        flesch_reading_ease=round(reading_ease, 2),
        flesch_kincaid_grade=round(kincaid_grade, 2),
        gunning_fog_index=round(fog, 2),
        smog_index=round(smog, 2),
        avg_word_length=round(avg_word_length, 2),
        avg_sentence_length=round(words_per_sentence, 2),
        readability_level=_level_for(reading_ease),
        target_audience_grade_level=f"Grade {grade}",
        complexity_score=round(min(100.0, max(0.0, 100 - reading_ease)), 2),
    )
