# wordle-engine

A Wordle game built in Python. Guess the secret 5-letter word in 6 attempts
or fewer.

## Example session

```
  ==============================
    WORDLE ENGINE
    Guess the 5-letter word.
    You have 6 attempts.
    Type 'hint' for a hint.
    Type 'exit' to quit anytime.
  ==============================

  _: _ _ _ _ _
  _: _ _ _ _ _
  _: _ _ _ _ _
  _: _ _ _ _ _
  _: _ _ _ _ _
  _: _ _ _ _ _

  (type 'hint' for a hint)
  Guess (1/6): crane

  1: C R A N E   ->   . . . . .
  _: _ _ _ _ _
  _: _ _ _ _ _
  _: _ _ _ _ _
  _: _ _ _ _ _
  _: _ _ _ _ _
  Wrong: -C- -N- -E-
  In the word:
    R -> ? X ? ? ?
    A -> ? ? X ? ?
  ------------------------------

  Guess (2/6): storm

  1: C R A N E   ->   . . . . .
  2: S T O R M   ->   S T O R .
  _: _ _ _ _ _
  _: _ _ _ _ _
  _: _ _ _ _ _
  _: _ _ _ _ _
  Wrong: -C- -N- -E- -M-
  In the word:
    R -> ? X ? R ?
    A -> ? ? X ? ?
  ------------------------------

  Guess (3/6): story

  1: C R A N E   ->   . . . . .
  2: S T O R M   ->   S T O R .
  3: S T O R Y   ->   S T O R Y
  _: _ _ _ _ _
  _: _ _ _ _ _
  _: _ _ _ _ _

  Well done! You got it in 3 guesses.

  Play again? (y/n): n
  Thanks for playing. Goodbye!
```

## Installation

```
pip install -e .
```

## How to play

```
python cli.py
```

- Type any valid 5-letter word and press Enter
- Each guess shows which letters are confirmed, misplaced, or wrong
- Type `hint` at any prompt to reveal one unknown letter for free
- Type `exit` at any prompt to quit the game

## Running tests

```
pytest
```

All 29 tests should pass.

## Linting

```
ruff check .
```

Should return zero warnings.

## Architecture

The project is split into two layers:

**Library (`wordle_engine/`)** — Contains:
- `checker.py` — `check_guess()` logic and `GuessResult` dataclass
- `game.py` — `WordleGame` class managing state, guesses, and hints
- `words.py` — wordlist loading, random word selection, guess validation

**Interface (`cli.py`)** — the file that reads from stdin or writes
to stdout. It calls the library and handles all display logic.

## AI disclosure

This project was built using Claude. 
First, I discussed the project scope and design decisions including
the code structure. And then I generate each file based on the 
finalized design. After testign and running the file, I made serveral
changes and finalized the display format, the hint system, the 
misplaced-letter grid display, the stacked guess history,
and all subsequent bug fixes and UI improvements.


**What the Claude Produced:** Claude generated  all python files,
and the test files.


