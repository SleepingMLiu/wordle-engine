"""Command-line interface for playing Wordle."""

import sys

from wordle_engine.game import WordleGame
from wordle_engine.words import get_random_word, is_valid_guess, load_wordlist

_GOODBYE = "  Thanks for playing. Goodbye!"


def _check_exit(raw: str) -> None:
    """Exit cleanly if the player typed 'exit' or 'quit'."""
    if raw.strip().lower() in ("exit", "quit"):
        print(_GOODBYE)
        sys.exit(0)


_WELCOME = """\
  ==============================
    WORDLE ENGINE
    Guess the 5-letter word.
    You have 6 attempts.
    Type 'hint' for a hint.
    Type 'exit' to quit anytime.
  =============================="""


def _collect_knowledge(
    game: WordleGame,
) -> tuple[set[str], dict[str, set[int]], dict[int, str]]:
    """Accumulate letter knowledge from every guess submitted so far.

    Returns:
        absent: letters confirmed to be entirely absent from the word.
            A letter only appears here if it has never shown up as a
            correct or misplaced match in any guess — this prevents
            duplicate-letter guesses from falsely marking a letter absent
            when one copy was correctly identified as misplaced.
        misplaced_at: letter -> positions where it has been ruled out.
        known_positions: position -> confirmed correct letter.
    """
    absent: set[str] = set()
    misplaced_at: dict[str, set[int]] = {}
    known_positions: dict[int, str] = {}
    in_word: set[str] = set()

    for result in game.guesses:
        known_positions.update(result.correct_positions)
        in_word.update(result.correct_positions.values())
        for pos, letter in result.wrong_positions.items():
            misplaced_at.setdefault(letter, set()).add(pos)
            in_word.add(letter)
        absent.update(result.absent_letters)

    # Remove any letter we now know IS in the word; it belongs in the
    # misplaced grid, not in the "wrong" list.
    absent -= in_word
    return absent, misplaced_at, known_positions


def _display_state(game: WordleGame) -> None:
    """Print full guess history, wrong letters, and misplaced-letter grid."""
    absent, misplaced_at, known_positions = _collect_knowledge(game)

    # -- Guess history: always 6 rows -----------------------------------------
    print()
    for n in range(1, 7):
        if n <= len(game.guesses):
            result = game.guesses[n - 1]
            word = " ".join(result.guess)
            pattern = " ".join(
                result.correct_positions.get(i, ".") for i in range(5)
            )
            print(f"  {n}: {word}   ->   {pattern}")
        else:
            print("  _: _ _ _ _ _")

    # -- Wrong letters (crossed-out style) ------------------------------------
    if absent:
        crossed = " ".join(f"-{c}-" for c in sorted(absent))
        print(f"\n  Wrong: {crossed}")

    # -- Misplaced-letter position grid ---------------------------------------
    # For each misplaced letter show a 5-cell row where:
    #   letter  = confirmed correct at that position
    #   X       = this letter was guessed here and ruled out
    #   _       = a different letter is already confirmed at this position
    #   ?       = still unknown for this letter
    if misplaced_at:
        print("\n  In the word:")
        for letter in sorted(misplaced_at):
            cells: list[str] = []
            for i in range(5):
                if known_positions.get(i) == letter:
                    cells.append(letter)
                elif i in misplaced_at[letter]:
                    cells.append("X")
                elif i in known_positions:
                    cells.append("_")
                else:
                    cells.append("?")
            print(f"    {letter}  -> {' '.join(cells)}")


def _end_message(game: WordleGame, secret: str) -> None:
    """Print the win or loss message."""
    if game.is_won:
        n = len(game.guesses)
        if n == 1:
            msg = "Incredible! First try!"
        elif n == 2:
            msg = "Amazing! You got it in 2!"
        elif n == 3:
            msg = "Great job! You got it in 3!"
        elif n <= 5:
            msg = f"Well done! You got it in {n} guesses."
        else:
            msg = "Phew! Got it on the last guess!"
    else:
        msg = f"So close! The word was: {secret}. Better luck next time!"
    print(f"\n  {msg}")


def _play_game(wordlist: list[str]) -> None:
    """Run a single Wordle game to completion."""
    secret = get_random_word(wordlist)
    game = WordleGame(secret)
    guessed: set[str] = set()

    while not game.is_over:
        _display_state(game)
        guess_num = len(game.guesses) + 1
        print("  (type 'hint' for a hint)")
        raw = input(f"  Guess ({guess_num}/6): ").strip()
        _check_exit(raw)
        raw = raw.upper()

        if raw == "HINT":
            try:
                idx, letter = game.get_hint()
                print(f"  Hint: position {idx} is the letter {letter}")
            except ValueError as exc:
                print(f"  {exc}")
            continue

        if raw in guessed:
            print("  You already guessed that word.")
            continue

        if not is_valid_guess(raw, wordlist):
            print("  Not a valid word.")
            continue

        guessed.add(raw)
        game.submit_guess(raw)

    _display_state(game)
    _end_message(game, secret)


def main() -> None:
    """Entry point: print welcome, load words, loop through games."""
    print(_WELCOME)
    wordlist = load_wordlist()
    while True:
        _play_game(wordlist)
        again = input("\n  Play again? (y/n): ").strip()
        _check_exit(again)
        if again.lower() != "y":
            print(_GOODBYE)
            sys.exit(0)


if __name__ == "__main__":
    main()
