"""Tests for wordle_engine.game."""

import pytest

from wordle_engine.game import WordleGame


def test_initial_state():
    game = WordleGame("CRANE")
    assert game.guesses == []
    assert not game.is_over
    assert not game.is_won
    assert game.guesses_remaining == 6


def test_submit_guess_records_result():
    game = WordleGame("CRANE")
    result = game.submit_guess("brave")  # lowercase — should be normalised
    assert len(game.guesses) == 1
    assert result.guess == "BRAVE"


def test_guesses_remaining_decrements():
    game = WordleGame("CRANE")
    game.submit_guess("BRAVE")
    assert game.guesses_remaining == 5
    game.submit_guess("STORM")
    assert game.guesses_remaining == 4


def test_is_won_after_correct_guess():
    game = WordleGame("CRANE")
    game.submit_guess("CRANE")
    assert game.is_won
    assert game.is_over


def test_is_not_won_after_wrong_guess():
    game = WordleGame("CRANE")
    game.submit_guess("BRAVE")
    assert not game.is_won
    assert not game.is_over


def test_is_over_after_max_guesses_exhausted():
    game = WordleGame("CRANE")
    for _ in range(6):
        game.submit_guess("BRAVE")
    assert game.is_over
    assert not game.is_won
    assert game.guesses_remaining == 0


def test_submit_guess_raises_when_already_won():
    game = WordleGame("CRANE")
    game.submit_guess("CRANE")
    with pytest.raises(ValueError, match="already over"):
        game.submit_guess("BRAVE")


def test_submit_guess_raises_when_max_guesses_reached():
    game = WordleGame("CRANE")
    for _ in range(6):
        game.submit_guess("BRAVE")
    with pytest.raises(ValueError, match="already over"):
        game.submit_guess("STORM")


def test_get_hint_returns_first_unknown_position():
    game = WordleGame("CRANE")
    idx, letter = game.get_hint()
    assert idx == 0
    assert letter == "C"


def test_get_hint_skips_known_positions():
    # CHESS vs CRANE: C@0 exact; H, E, S, S absent/misplaced
    # After this guess, position 0 is known.
    game = WordleGame("CRANE")
    game.submit_guess("CHESS")  # C correct at 0; rest do not match
    idx, letter = game.get_hint()
    assert idx == 1
    assert letter == "R"


def test_get_hint_raises_when_all_positions_known():
    game = WordleGame("CRANE")
    game.submit_guess("CRANE")  # all correct → all positions known
    with pytest.raises(ValueError):
        game.get_hint()


def test_get_hint_raises_when_game_is_over_by_exhaustion():
    game = WordleGame("CRANE")
    for _ in range(6):
        game.submit_guess("BRAVE")
    with pytest.raises(ValueError, match="already over"):
        game.get_hint()


def test_custom_max_guesses():
    game = WordleGame("CRANE", max_guesses=3)
    assert game.guesses_remaining == 3
    game.submit_guess("BRAVE")
    game.submit_guess("STORM")
    game.submit_guess("PLUMB")
    assert game.is_over
    assert not game.is_won
