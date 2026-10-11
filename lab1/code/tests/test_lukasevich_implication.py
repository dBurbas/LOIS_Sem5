import pytest

from engine.operations import lukasevich_implication


class TestLukasevichImplication:
    def test_zero_zero(self):
        assert lukasevich_implication(0.0, 0.0) == 1.0

    def test_zero_one(self):
        assert lukasevich_implication(0.0, 1.0) == 1.0

    def test_one_zero(self):
        assert lukasevich_implication(1.0, 0.0) == 0.0

    def test_one_one(self):
        assert lukasevich_implication(1.0, 1.0) == 1.0

    def test_half_half(self):
        assert lukasevich_implication(0.5, 0.5) == 1.0

    def test_min_clamped(self):
        assert lukasevich_implication(0.2, 0.3) == pytest.approx(1.0)

    def test_less_than_one(self):
        assert lukasevich_implication(0.8, 0.3) == pytest.approx(0.5)

    def test_result_bounds(self):
        for a in [i / 10 for i in range(11)]:
            for b in [i / 10 for i in range(11)]:
                r = lukasevich_implication(a, b)
                assert 0.0 <= r <= 1.0

    def test_monotonic_in_second_arg(self):
        assert lukasevich_implication(0.5, 0.2) <= lukasevich_implication(0.5, 0.8)
