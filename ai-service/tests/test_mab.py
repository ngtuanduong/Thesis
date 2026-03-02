"""Unit tests for Hierarchical MAB (Layer 3)."""

import pytest
import numpy as np

from app.services.mab_service import thompson_select, compute_reward


class TestThompsonSelect:
    """Tests for Thompson Sampling selection."""

    def test_selects_from_arms(self):
        """Should return one of the arms."""
        arms = [
            {"id": 1, "alpha": 1.0, "beta": 1.0},
            {"id": 2, "alpha": 1.0, "beta": 1.0},
            {"id": 3, "alpha": 1.0, "beta": 1.0},
        ]
        selected = thompson_select(arms)
        assert selected is not None
        assert selected["id"] in [1, 2, 3]

    def test_empty_arms_returns_none(self):
        """Empty arm list should return None."""
        assert thompson_select([]) is None

    def test_single_arm_always_selected(self):
        """Single arm should always be selected."""
        arms = [{"id": 1, "alpha": 1.0, "beta": 1.0}]
        for _ in range(10):
            selected = thompson_select(arms)
            assert selected["id"] == 1

    def test_high_alpha_preferred(self):
        """Arm with much higher alpha/beta ratio should be selected more often."""
        np.random.seed(42)
        arms = [
            {"id": "good", "alpha": 100.0, "beta": 1.0},   # Expected ~0.99
            {"id": "bad", "alpha": 1.0, "beta": 100.0},     # Expected ~0.01
        ]
        selections = {"good": 0, "bad": 0}
        for _ in range(1000):
            selected = thompson_select(arms)
            selections[selected["id"]] += 1

        # The "good" arm should be selected almost always
        assert selections["good"] > 950, f"Good arm only selected {selections['good']}/1000 times"

    def test_exploration_occurs(self):
        """With uniform priors, all arms should eventually be selected."""
        np.random.seed(42)
        arms = [
            {"id": i, "alpha": 1.0, "beta": 1.0} for i in range(5)
        ]
        selected_ids = set()
        for _ in range(100):
            selected = thompson_select(arms)
            selected_ids.add(selected["id"])

        assert len(selected_ids) == 5, "All 5 arms should be explored with uniform priors"

    def test_similar_arms_balanced_selection(self):
        """Arms with similar parameters should be selected roughly equally."""
        np.random.seed(42)
        arms = [
            {"id": i, "alpha": 10.0, "beta": 10.0} for i in range(3)
        ]
        counts = {0: 0, 1: 0, 2: 0}
        for _ in range(3000):
            selected = thompson_select(arms)
            counts[selected["id"]] += 1

        # Each should be selected roughly 1000 times (within 200 tolerance)
        for arm_id, count in counts.items():
            assert 600 < count < 1400, f"Arm {arm_id} selected {count}/3000 times"


class TestComputeReward:
    """Tests for the reward function."""

    def test_reward_in_valid_range(self):
        """Reward should always be in [0, 1]."""
        test_cases = [
            (0.1, 0.3, True, 1, 60),    # Good learning
            (0.1, 0.1, False, 1, 60),    # No learning, incorrect
            (0.9, 0.95, True, 1, 30),    # Near mastery, fast
            (0.5, 0.4, False, 5, 600),   # Decline, slow
            (0.0, 0.0, False, 1, 0),     # Worst case
            (0.0, 1.0, True, 1, 10),     # Best case
        ]
        for before, after, correct, attempt, time in test_cases:
            r = compute_reward(before, after, correct, attempt, time)
            assert 0 <= r <= 1, (
                f"Reward {r} out of range for: before={before}, after={after}, "
                f"correct={correct}, attempt={attempt}, time={time}"
            )

    def test_learning_gain_increases_reward(self):
        """Higher learning gain should give higher reward."""
        r_no_gain = compute_reward(0.3, 0.3, True, 1, 60)
        r_small_gain = compute_reward(0.3, 0.4, True, 1, 60)
        r_large_gain = compute_reward(0.3, 0.6, True, 1, 60)
        assert r_large_gain >= r_small_gain >= r_no_gain

    def test_correct_first_attempt_high_reward(self):
        """Correct on first attempt with some learning gain → high reward."""
        r = compute_reward(0.3, 0.5, True, 1, 120)
        assert r > 0.3  # Should be moderate to high

    def test_incorrect_many_attempts_low_reward(self):
        """Incorrect after many attempts → low reward."""
        r = compute_reward(0.5, 0.5, False, 5, 600)
        assert r < 0.3  # Should be low

    def test_fast_correct_higher_than_slow(self):
        """Fast correct should have slightly higher reward than slow correct."""
        r_fast = compute_reward(0.3, 0.5, True, 1, 30)
        r_slow = compute_reward(0.3, 0.5, True, 1, 600)
        assert r_fast >= r_slow

    def test_efficiency_component(self):
        """Very fast (30s) should maximize efficiency; very slow (600s) should minimize."""
        # Efficiency = min(1.0, 300 / max(time, 30))
        # At 30s: 300/30 = 10 → clamped to 1.0
        # At 300s: 300/300 = 1.0
        # At 600s: 300/600 = 0.5
        r_30 = compute_reward(0.3, 0.4, True, 1, 30)
        r_600 = compute_reward(0.3, 0.4, True, 1, 600)
        assert r_30 > r_600

    def test_negative_learning_gain_clamped(self):
        """Negative learning gain (mastery decreased) should still give non-negative reward."""
        r = compute_reward(0.5, 0.3, False, 3, 120)
        assert r >= 0.0

    def test_first_attempt_correct_better_than_many(self):
        """First attempt correct should give better difficulty reward than many attempts."""
        r_first = compute_reward(0.3, 0.5, True, 1, 120)
        r_fourth = compute_reward(0.3, 0.5, True, 4, 120)
        assert r_first >= r_fourth
