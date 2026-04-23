"""Word loading and validation utilities."""

import random
from pathlib import Path

_DEFAULT_WORDLIST = Path(__file__).parent.parent / "data" / "wordlist.txt"


def load_wordlist(path: str | None = None) -> list[str]:
    """Load a word list from a file, one word per line.

    Args:
        path: Path to the word-list file.  Defaults to ``data/wordlist.txt``
              relative to the project root.

    Returns:
        A list of 5-letter uppercase words with blank lines stripped.
    """
    source = Path(path) if path else _DEFAULT_WORDLIST
    return [
        line.strip().upper()
        for line in source.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def get_random_word(wordlist: list[str]) -> str:
    """Return a random word from *wordlist*.

    Args:
        wordlist: A non-empty list of words.

    Returns:
        One word chosen uniformly at random.
    """
    return random.choice(wordlist)


def is_valid_guess(guess: str, wordlist: list[str]) -> bool:
    """Return True when *guess* is exactly 5 letters and present in *wordlist*.

    The comparison is case-insensitive: the guess is uppercased before
    checking membership.

    Args:
        guess: The player's input string.
        wordlist: The list of accepted words (uppercase).

    Returns:
        ``True`` if the guess is valid, ``False`` otherwise.
    """
    return len(guess) == 5 and guess.upper() in wordlist
