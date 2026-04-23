"""Tests for wordle_engine.checker."""

from wordle_engine.checker import check_guess


def test_all_correct():
    result = check_guess("CRANE", "CRANE")
    assert result.correct_positions == {0: "C", 1: "R", 2: "A", 3: "N", 4: "E"}
    assert result.wrong_positions == {}
    assert result.absent_letters == []


def test_all_absent():
    # No letter in CRISP appears in BOUND
    result = check_guess("CRISP", "BOUND")
    assert result.correct_positions == {}
    assert result.wrong_positions == {}
    assert set(result.absent_letters) == {"C", "R", "I", "S", "P"}


def test_all_wrong_position():
    # STARE vs RATES: same 5 letters, no letter shares an index
    # S(0)≠R(0), T(1)≠A(1), A(2)≠T(2), R(3)≠E(3), E(4)≠S(4)
    result = check_guess("STARE", "RATES")
    assert result.correct_positions == {}
    assert set(result.wrong_positions.values()) == {"S", "T", "A", "R", "E"}
    assert result.absent_letters == []


def test_partial_match():
    # CRANE vs ARMOR: R at index 1 is exact; A is misplaced; C, N, E absent
    result = check_guess("CRANE", "ARMOR")
    assert result.correct_positions == {1: "R"}
    assert result.wrong_positions == {2: "A"}
    assert set(result.absent_letters) == {"C", "N", "E"}


def test_duplicate_letters_guess_has_more():
    # SPEED vs CREEP:
    #   guess : S(0) P(1) E(2) E(3) D(4)
    #   secret: C(0) R(1) E(2) E(3) P(4)
    # Pass 1 exact: E@2, E@3
    # Pass 2 remaining pool [C, R, _, _, P]:
    #   S → absent, P → wrong@1 (consumes P), D → absent
    result = check_guess("SPEED", "CREEP")
    assert result.correct_positions == {2: "E", 3: "E"}
    assert result.wrong_positions == {1: "P"}
    assert set(result.absent_letters) == {"S", "D"}


def test_duplicate_letters_secret_has_more():
    # CRANE vs CREED: C@0 and R@1 exact; A absent; N absent; E wrong@4
    # secret pool after pass 1: [_, _, E, E, D] (C and R consumed)
    # E at index 4 of guess → in pool → wrong_position
    result = check_guess("CRANE", "CREED")
    assert result.correct_positions == {0: "C", 1: "R"}
    assert result.wrong_positions == {4: "E"}
    assert set(result.absent_letters) == {"A", "N"}


def test_single_letter_word_repeated_in_guess_only_matched_once():
    # SPELL vs PLUMB: S absent, P wrong@1 (P is at 0 in PLUMB), E absent,
    # L wrong@3 (L is at 3... wait PLUMB has no L)
    # PLUMB: P(0) L(1) U(2) M(3) B(4)
    # SPELL: S(0) P(1) E(2) L(3) L(4)
    # Pass 1 exact: none (S≠P, P≠L, E≠U, L≠M, L≠B)
    # Pool: [P, L, U, M, B]
    # S → absent; P → wrong@1 (consume P); E → absent;
    # L → wrong@3 (consume L); L → absent (pool has no more L)
    result = check_guess("SPELL", "PLUMB")
    assert result.correct_positions == {}
    assert result.wrong_positions == {1: "P", 3: "L"}
    assert set(result.absent_letters) == {"S", "E", "L"}
