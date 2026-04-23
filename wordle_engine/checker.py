"""Guess-checking logic for Wordle."""

from dataclasses import dataclass


@dataclass
class GuessResult:
    """The outcome of checking one guess against the secret word.

    Attributes:
        guess: The guessed word (5 uppercase letters).
        correct_positions: Letters matched at the exact index, e.g. {2: "T"}.
        wrong_positions: Letters present in the word but at the wrong index,
            e.g. {0: "R"} means "R" exists somewhere else in the secret.
        absent_letters: Letters that do not appear in the secret at all.
    """

    guess: str
    correct_positions: dict[int, str]
    wrong_positions: dict[int, str]
    absent_letters: list[str]


def check_guess(guess: str, secret: str) -> GuessResult:
    """Compare a guess against the secret word and classify every letter.

    Both arguments must be 5-letter uppercase strings. Validation is the
    caller's responsibility.

    Duplicate-letter handling:
      Pass 1 — scan both strings in parallel; any position where
               guess[i] == secret[i] is an exact match.  That secret
               letter is "consumed" so it cannot also satisfy a
               wrong-position match for the same letter later.
      Pass 2 — for every non-exact guess letter, check whether the
               *remaining* (unconsumed) secret letters contain it.
               If yes, it is a wrong-position match and we consume one
               occurrence from the remaining pool.  If no, it is absent.

    This prevents inflating match counts when the guess contains more
    copies of a letter than the secret does.

    Args:
        guess: The player's guess (5 uppercase letters).
        secret: The target word (5 uppercase letters).

    Returns:
        A GuessResult describing exact matches, misplaced letters, and
        absent letters.
    """
    correct_positions: dict[int, str] = {}
    wrong_positions: dict[int, str] = {}
    absent_letters: list[str] = []

    # Each slot starts as the secret letter; exact matches set it to None
    # so the same letter cannot be claimed twice in pass 2.
    secret_pool: list[str | None] = list(secret)
    # Indices of guess letters that did NOT land in the correct position.
    unmatched: list[int] = []

    # Pass 1: find exact (correct-position) matches.
    for i, (g, s) in enumerate(zip(guess, secret)):
        if g == s:
            correct_positions[i] = g
            secret_pool[i] = None  # consumed; unavailable for pass 2
        else:
            unmatched.append(i)

    # Pass 2: classify the remaining guess letters as misplaced or absent.
    for i in unmatched:
        g = guess[i]
        if g in secret_pool:
            # Letter exists in the secret at some other position.
            wrong_positions[i] = g
            # Consume exactly one occurrence so duplicates are not over-counted.
            secret_pool[secret_pool.index(g)] = None
        else:
            absent_letters.append(g)

    return GuessResult(
        guess=guess,
        correct_positions=correct_positions,
        wrong_positions=wrong_positions,
        absent_letters=absent_letters,
    )
