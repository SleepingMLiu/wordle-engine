"""Tests for wordle_engine.words."""

from wordle_engine.words import get_random_word, is_valid_guess

_WORDS = ["CRANE", "BRAVE", "STORM", "PLUMB", "NIGHT"]


def test_is_valid_guess_accepts_known_word():
    assert is_valid_guess("CRANE", _WORDS)


def test_is_valid_guess_case_insensitive():
    assert is_valid_guess("crane", _WORDS)
    assert is_valid_guess("Crane", _WORDS)


def test_is_valid_guess_rejects_too_short():
    assert not is_valid_guess("CRAN", _WORDS)


def test_is_valid_guess_rejects_too_long():
    assert not is_valid_guess("CRANES", _WORDS)


def test_is_valid_guess_rejects_unknown_word():
    assert not is_valid_guess("ZZZZZ", _WORDS)


def test_is_valid_guess_rejects_empty_string():
    assert not is_valid_guess("", _WORDS)


def test_get_random_word_returns_item_from_list():
    word = get_random_word(_WORDS)
    assert word in _WORDS


def test_get_random_word_single_element():
    assert get_random_word(["CRANE"]) == "CRANE"


def test_get_random_word_distribution():
    # Over many draws every word in a small list should appear at least once.
    seen: set[str] = set()
    for _ in range(200):
        seen.add(get_random_word(_WORDS))
    assert seen == set(_WORDS)
