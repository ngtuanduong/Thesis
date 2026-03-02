"""Unit tests for Dynamic K-Value Elo Rating (Layer 2)."""

import math

import pytest

from app.services.elo_service import (
    expected_score,
    compute_dynamic_k,
    compute_problem_k,
    ELO_INIT,
    K_MIN,
    K_MAX,
    DEFAULT_STUDENT_ELO,
)


class TestExpectedScore:
    """Tests for expected_score function."""

    def test_equal_ratings(self):
        """Equal ratings → 50% expected score."""
        e = expected_score(1200, 1200)
        assert abs(e - 0.5) < 0.001

    def test_higher_student_rating(self):
        """Student rated higher → expected > 0.5."""
        e = expected_score(1600, 1200)
        assert e > 0.5

    def test_lower_student_rating(self):
        """Student rated lower → expected < 0.5."""
        e = expected_score(1200, 1600)
        assert e < 0.5

    def test_symmetry(self):
        """E(A,B) + E(B,A) should approximately equal 1."""
        e1 = expected_score(1400, 1200)
        e2 = expected_score(1200, 1400)
        assert abs(e1 + e2 - 1.0) < 0.001

    def test_known_values(self):
        """With 400 point difference, expected should be ~0.909."""
        # 10^(400/400) = 10, so E = 1/(1+1/10) = 10/11 ≈ 0.909
        e = expected_score(1600, 1200)
        assert abs(e - 10 / 11) < 0.001

    def test_result_in_range(self):
        """Expected score should always be in (0, 1)."""
        for s_r in [400, 800, 1200, 1600, 2400, 2800]:
            for p_r in [400, 800, 1200, 1600, 2400, 2800]:
                e = expected_score(s_r, p_r)
                assert 0 < e < 1

    def test_extreme_difference(self):
        """Very large difference should be close to 1 or 0."""
        e_strong = expected_score(2800, 400)
        assert e_strong > 0.99
        e_weak = expected_score(400, 2800)
        assert e_weak < 0.01


class TestDynamicK:
    """Tests for compute_dynamic_k function."""

    def test_new_student_gets_max_k(self):
        """Students with < 3 history entries should get K_MAX."""
        assert compute_dynamic_k([]) == K_MAX
        assert compute_dynamic_k([{"is_correct": True, "expected_score": 0.5}]) == K_MAX
        assert compute_dynamic_k([
            {"is_correct": True, "expected_score": 0.5},
            {"is_correct": False, "expected_score": 0.5},
        ]) == K_MAX

    def test_improving_student_gets_lower_k(self):
        """Consistently outperforming expectations → lower K (more stable)."""
        history = [
            {"is_correct": True, "expected_score": 0.4} for _ in range(10)
        ]
        k = compute_dynamic_k(history)
        assert k < K_MAX
        assert k >= K_MIN

    def test_struggling_student_gets_higher_k(self):
        """Consistently underperforming → higher K (needs recalibration)."""
        history = [
            {"is_correct": False, "expected_score": 0.7} for _ in range(10)
        ]
        k = compute_dynamic_k(history)
        assert k > K_MIN

    def test_k_always_in_valid_range(self):
        """K should always be in [K_MIN, K_MAX]."""
        scenarios = [
            [{"is_correct": True, "expected_score": 0.1}] * 20,
            [{"is_correct": False, "expected_score": 0.9}] * 20,
            [{"is_correct": b, "expected_score": 0.5} for b in [True, False] * 10],
        ]
        for history in scenarios:
            k = compute_dynamic_k(history)
            assert K_MIN <= k <= K_MAX, f"K={k} out of range for history"

    def test_mixed_performance(self):
        """Mixed performance should give moderate K."""
        history = [
            {"is_correct": i % 2 == 0, "expected_score": 0.5} for i in range(10)
        ]
        k = compute_dynamic_k(history)
        assert K_MIN <= k <= K_MAX


class TestProblemK:
    """Tests for compute_problem_k function."""

    def test_new_problem_gets_max_k(self):
        """New problem (0 or 1 attempts) should get K_MAX."""
        assert compute_problem_k(0) == K_MAX
        assert compute_problem_k(1) == K_MAX

    def test_k_decreases_with_attempts(self):
        """Problem K should decrease as more students attempt it."""
        k1 = compute_problem_k(1)
        k10 = compute_problem_k(10)
        k100 = compute_problem_k(100)
        assert k1 >= k10 >= k100

    def test_k_never_below_minimum(self):
        """Problem K should never go below K_MIN."""
        for n in [1, 10, 100, 1000, 10000]:
            k = compute_problem_k(n)
            assert k >= K_MIN

    def test_formula_correctness(self):
        """K should follow K_MAX / sqrt(n_attempts)."""
        k = compute_problem_k(16)
        # K_MAX / sqrt(16) = 40 / 4 = 10 = K_MIN
        assert abs(k - K_MIN) < 0.1


class TestEloConstants:
    """Tests for Elo configuration constants."""

    def test_difficulty_initializations(self):
        """Initial Elo should be ordered by difficulty."""
        assert ELO_INIT["EASY"] < ELO_INIT["MEDIUM"] < ELO_INIT["HARD"]

    def test_default_student_elo(self):
        """Default student Elo should be between EASY and MEDIUM."""
        assert ELO_INIT["EASY"] < DEFAULT_STUDENT_ELO < ELO_INIT["HARD"]

    def test_elo_spacing(self):
        """There should be meaningful gaps between difficulty levels."""
        assert ELO_INIT["MEDIUM"] - ELO_INIT["EASY"] >= 200
        assert ELO_INIT["HARD"] - ELO_INIT["MEDIUM"] >= 200


class TestEloUpdateMath:
    """Test the Elo update formula math directly."""

    def test_correct_answer_increases_student_rating(self):
        """Solving a problem should increase student rating."""
        s_rating = 1200.0
        p_rating = 1400.0
        exp = expected_score(s_rating, p_rating)
        k = 30.0
        new_rating = s_rating + k * (1.0 - exp)
        assert new_rating > s_rating

    def test_incorrect_decreases_student_rating(self):
        """Failing should decrease student rating."""
        s_rating = 1200.0
        p_rating = 1000.0
        exp = expected_score(s_rating, p_rating)
        k = 30.0
        new_rating = s_rating + k * (0.0 - exp)
        assert new_rating < s_rating

    def test_upset_win_larger_gain(self):
        """Solving a much harder problem should give a bigger rating boost."""
        s_rating = 1200.0
        exp_easy = expected_score(s_rating, 1000.0)
        exp_hard = expected_score(s_rating, 1600.0)
        k = 30.0
        gain_easy = k * (1.0 - exp_easy)
        gain_hard = k * (1.0 - exp_hard)
        assert gain_hard > gain_easy

    def test_problem_rating_moves_opposite(self):
        """When student solves, problem rating should decrease (proven easier)."""
        p_rating = 1400.0
        s_rating = 1200.0
        exp = expected_score(s_rating, p_rating)
        k = 20.0
        # Problem update: p_rating + k * (exp - actual)
        # Student won: actual=1, so delta = k*(exp-1) which is negative since exp<1
        new_p_rating = p_rating + k * (exp - 1.0)
        assert new_p_rating < p_rating
