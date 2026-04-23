"""Game-state management for Wordle."""

from .checker import GuessResult, check_guess


class WordleGame:
    """Manages the full state of a single Wordle game.

    Args:
        secret: The target word.  Stored uppercased.
        max_guesses: Maximum number of allowed attempts (default 6).

    Attributes:
        guesses: Ordered list of GuessResult objects, one per submitted guess.
    """

    def __init__(self, secret: str, max_guesses: int = 6) -> None:
        self._secret = secret.upper()
        self._max_guesses = max_guesses
        self.guesses: list[GuessResult] = []

    @property
    def is_won(self) -> bool:
        """True when the last guess matched all positions."""
        if not self.guesses:
            return False
        return len(self.guesses[-1].correct_positions) == len(self._secret)

    @property
    def is_over(self) -> bool:
        """True when the game has been won or all guesses are exhausted."""
        return self.is_won or len(self.guesses) >= self._max_guesses

    @property
    def guesses_remaining(self) -> int:
        """Number of guesses the player may still submit."""
        return self._max_guesses - len(self.guesses)

    def submit_guess(self, guess: str) -> GuessResult:
        """Submit a guess and record the result.

        Args:
            guess: A 5-letter word.  Uppercased automatically.

        Returns:
            The GuessResult for this guess.

        Raises:
            ValueError: If the game is already over.
        """
        if self.is_over:
            raise ValueError("Game is already over.")
        result = check_guess(guess.upper(), self._secret)
        self.guesses.append(result)
        return result

    def get_hint(self) -> tuple[int, str]:
        """Reveal the first secret letter that has not yet been guessed correctly.

        Scans positions 0–4 in order and returns the first index where the
        correct letter is still unknown.

        Returns:
            A ``(index, letter)`` tuple.

        Raises:
            ValueError: If the game is over or all positions are already known.
        """
        if self.is_over:
            raise ValueError("Game is already over.")
        known: set[int] = set()
        for result in self.guesses:
            known.update(result.correct_positions.keys())
        for i, letter in enumerate(self._secret):
            if i not in known:
                return (i, letter)
        raise ValueError("All positions are already known.")
