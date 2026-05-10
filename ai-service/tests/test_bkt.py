"""Unit tests for BKT Knowledge Tracing (Layer 1)."""

import pytest

from app.services.bkt_service import (
    BKTParams,
    bkt_update,
    predict_correctness,
    DEFAULT_PARAMS,
)


# --- Default BKT parameters for tests ---

BASIC_PARAMS = BKTParams(**DEFAULT_PARAMS[1])           # Tier 1: Foundations
CORE_PARAMS = BKTParams(**DEFAULT_PARAMS[2])            # Tier 2: Core Skills
INTERMEDIATE_PARAMS = BKTParams(**DEFAULT_PARAMS[3])    # Tier 3: Intermediate
ADVANCED_PARAMS = BKTParams(**DEFAULT_PARAMS[4])        # Tier 4: Advanced Application
EXPERT_PARAMS = BKTParams(**DEFAULT_PARAMS[5])          # Tier 5: Expert


class TestBKTUpdate:
    """Tests for the bkt_update function."""

    def test_correct_answer_increases_mastery(self):
        """Correct answer should increase P(mastery)."""
        p_before = 0.3
        p_after = bkt_update(p_before, is_correct=True, params=BASIC_PARAMS)
        assert p_after > p_before

    def test_incorrect_answer_can_decrease_mastery(self):
        """Incorrect answer should decrease mastery (or increase less)."""
        p_before = 0.5
        p_correct = bkt_update(p_before, is_correct=True, params=BASIC_PARAMS)
        p_incorrect = bkt_update(p_before, is_correct=False, params=BASIC_PARAMS)
        assert p_correct > p_incorrect

    def test_initial_low_mastery_correct(self):
        """Starting from low mastery, a correct answer should increase it."""
        p = bkt_update(0.1, is_correct=True, params=BASIC_PARAMS)
        assert p > 0.1
        assert p < 1.0

    def test_initial_low_mastery_incorrect(self):
        """From low mastery, an incorrect still applies learning transition."""
        p = bkt_update(0.1, is_correct=False, params=BASIC_PARAMS)
        # Learning transition still applies, but posterior is lower
        assert 0.001 <= p <= 0.999

    def test_high_mastery_correct_stays_high(self):
        """High mastery + correct should stay high (near 1.0)."""
        p = bkt_update(0.95, is_correct=True, params=BASIC_PARAMS)
        assert p > 0.9
        assert p <= 0.999

    def test_result_always_in_valid_range(self):
        """Result should always be in [0.001, 0.999]."""
        all_params = [BASIC_PARAMS, CORE_PARAMS, INTERMEDIATE_PARAMS, ADVANCED_PARAMS, EXPERT_PARAMS]
        for p_start in [0.001, 0.01, 0.1, 0.5, 0.9, 0.99, 0.999]:
            for is_correct in [True, False]:
                for params in all_params:
                    result = bkt_update(p_start, is_correct, params)
                    assert 0.001 <= result <= 0.999, (
                        f"Out of range: p_start={p_start}, correct={is_correct}, result={result}"
                    )

    def test_zero_mastery_doesnt_crash(self):
        """Edge case: mastery at 0 should not cause division by zero."""
        p = bkt_update(0.001, is_correct=True, params=BASIC_PARAMS)
        assert 0.001 <= p <= 0.999

    def test_one_mastery_doesnt_crash(self):
        """Edge case: mastery at ~1 should not cause issues."""
        p = bkt_update(0.999, is_correct=False, params=BASIC_PARAMS)
        assert 0.001 <= p <= 0.999

    def test_learning_transition_effect(self):
        """The learning transition should push mastery up even after incorrect."""
        p_l = 0.0
        params = BKTParams(p_l0=0.0, p_transit=0.5, p_guess=0.0, p_slip=0.0)
        # With p_l=0, p_slip=0: incorrect → posterior p_l=0, then transit → 0.5
        p = bkt_update(p_l, is_correct=False, params=params)
        # After posterior + transit, should be > 0
        assert p > 0.001

    def test_consecutive_correct_convergence(self):
        """Multiple correct answers should converge toward mastery."""
        p = 0.1
        for _ in range(20):
            p = bkt_update(p, is_correct=True, params=BASIC_PARAMS)
        assert p > 0.9, f"After 20 correct answers, mastery should be high, got {p}"

    def test_tier_differences(self):
        """Over many updates, basic concepts should converge to mastery faster."""
        p_basic = 0.1
        p_advanced = 0.1
        for _ in range(10):
            p_basic = bkt_update(p_basic, is_correct=True, params=BASIC_PARAMS)
            p_advanced = bkt_update(p_advanced, is_correct=True, params=ADVANCED_PARAMS)
        # Basic tier has higher p_transit → converges to mastery faster
        assert p_basic > p_advanced or (p_basic > 0.95 and p_advanced > 0.95)


class TestPredictCorrectness:
    """Tests for the predict_correctness function."""

    def test_basic_prediction(self):
        """P(correct) should be between 0 and 1."""
        p = predict_correctness(0.5, BASIC_PARAMS)
        assert 0 < p < 1

    def test_high_mastery_high_prediction(self):
        """High mastery should predict high correctness."""
        p = predict_correctness(0.95, BASIC_PARAMS)
        assert p > 0.8

    def test_low_mastery_lower_prediction(self):
        """Low mastery should predict lower correctness (but not 0 due to guessing)."""
        p = predict_correctness(0.05, BASIC_PARAMS)
        # P(correct) = 0.05*(1-0.1) + 0.95*0.2 = 0.045 + 0.19 = 0.235
        assert p > 0.1  # guess probability keeps it above 0
        assert p < 0.5

    def test_mastered_concept_prediction(self):
        """Fully mastered concept: P(correct) ≈ 1 - P(slip)."""
        p = predict_correctness(1.0, BKTParams(p_l0=0, p_transit=0, p_guess=0.2, p_slip=0.1))
        # P(correct) = 1.0*(1-0.1) + 0*0.2 = 0.9
        assert abs(p - 0.9) < 0.001

    def test_unlearned_concept_prediction(self):
        """Unlearned concept: P(correct) ≈ P(guess)."""
        p = predict_correctness(0.0, BKTParams(p_l0=0, p_transit=0, p_guess=0.25, p_slip=0.1))
        # P(correct) = 0*(1-0.1) + 1*0.25 = 0.25
        assert abs(p - 0.25) < 0.001

    def test_prediction_monotonically_increasing(self):
        """Higher mastery → higher P(correct)."""
        predictions = [
            predict_correctness(p, BASIC_PARAMS) for p in [0.1, 0.3, 0.5, 0.7, 0.9]
        ]
        for i in range(len(predictions) - 1):
            assert predictions[i] < predictions[i + 1]


class TestDefaultParams:
    """Tests for default parameter configuration."""

    def test_all_tiers_defined(self):
        """All 5 tiers should have default params."""
        assert 1 in DEFAULT_PARAMS
        assert 2 in DEFAULT_PARAMS
        assert 3 in DEFAULT_PARAMS
        assert 4 in DEFAULT_PARAMS
        assert 5 in DEFAULT_PARAMS

    def test_params_in_valid_range(self):
        """All probabilities should be in (0, 1)."""
        for tier, params in DEFAULT_PARAMS.items():
            for key, val in params.items():
                assert 0 < val < 1, f"Tier {tier}, {key}={val} out of range"

    def test_basic_learns_faster(self):
        """Basic tier should have higher p_transit (learns faster)."""
        assert DEFAULT_PARAMS[1]["p_transit"] > DEFAULT_PARAMS[5]["p_transit"]

    def test_advanced_lower_initial_mastery(self):
        """Advanced tier should have lower initial mastery."""
        assert DEFAULT_PARAMS[5]["p_l0"] < DEFAULT_PARAMS[1]["p_l0"]

    def test_params_monotonically_decrease_across_tiers(self):
        """p_l0 and p_transit should decrease from tier 1 to tier 5."""
        for key in ["p_l0", "p_transit"]:
            for tier in range(1, 5):
                assert DEFAULT_PARAMS[tier][key] >= DEFAULT_PARAMS[tier + 1][key], (
                    f"{key}: tier {tier} ({DEFAULT_PARAMS[tier][key]}) < tier {tier+1} ({DEFAULT_PARAMS[tier+1][key]})"
                )
