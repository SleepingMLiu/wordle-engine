"""wordle_engine — a Wordle game-engine library."""

from .checker import GuessResult, check_guess
from .game import WordleGame
from .words import get_random_word, is_valid_guess, load_wordlist

__all__ = [
    "GuessResult",
    "WordleGame",
    "check_guess",
    "get_random_word",
    "is_valid_guess",
    "load_wordlist",
]
