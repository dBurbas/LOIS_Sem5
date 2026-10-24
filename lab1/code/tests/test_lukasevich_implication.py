# Лабораторная работа №1 по дисциплине ЛОИС
# Выполнена студентами группы 421702 Бурбасом Дмитрием Юрьевичем и
# Башурой Артемом Олеговичем
#
# Файл основных базовых операций нечеткой логики необходимых для
# выполнения лабораторной (треугольная норма граничного произведения, импликация Лукаcевича)
# 03.10.2026
# Источники:
# pytest-dev: pytest документация [Электронный ресурс]
# pytest : документация фреймворка тестирования. – Режим доступа:
# https://docs.pytest.org. – Дата доступа: 03.10.2026.
import itertools

import pytest
from engine.operations import bounded_product_t_norm, lukasevich_implication

EPS = 1e-12

TENTHS = [i / 10 for i in range(11)]
AWKWARD = [
    0.0,
    1.0,
    0.123456789012,
    0.7111917696952796,
    0.9364405867994596,
    0.4221069999614152,
    0.1,
    0.2,
    0.7,
]
POINTS = sorted(set(TENTHS + AWKWARD))

T = bounded_product_t_norm
I = lukasevich_implication


def pairs(values=POINTS):
    return itertools.product(values, repeat=2)


def triples(values=POINTS):
    return itertools.product(values, repeat=3)


class TestLukasevichImplication:
    def test_zero_zero(self):
        assert I(0.0, 0.0) == 1.0

    def test_zero_one(self):
        assert I(0.0, 1.0) == 1.0

    def test_one_zero(self):
        assert I(1.0, 0.0) == 0.0

    def test_one_one(self):
        assert I(1.0, 1.0) == 1.0

    def test_half_half(self):
        assert I(0.5, 0.5) == 1.0

    def test_min_clamped(self):
        assert I(0.2, 0.3) == pytest.approx(1.0)

    def test_less_than_one(self):
        assert I(0.8, 0.3) == pytest.approx(0.5)

    def test_result_bounds(self):
        for a in [i / 10 for i in range(11)]:
            for b in [i / 10 for i in range(11)]:
                r = I(a, b)
                assert 0.0 <= r <= 1.0

    def test_monotonic_in_second_arg(self):
        assert I(0.5, 0.2) <= I(0.5, 0.8)

    # Монотонность по обоим аргументам
    def test_monotonic_in_second_arg_all_points(self):
        for y1, y2, x in itertools.product(POINTS, repeat=3):
            if y1 <= y2:
                assert I(x, y1) <= I(x, y2)

    def test_antitone_in_first_arg(self):
        for x1, x2, y in itertools.product(POINTS, repeat=3):
            if x1 <= x2:
                assert I(x1, y) >= I(x2, y)

    # Свойства импликации
    def test_boundary_conditions_match_classical_implication(self):
        assert I(0.0, 0.0) == 1.0
        assert I(0.0, 1.0) == 1.0
        assert I(1.0, 0.0) == 0.0
        assert I(1.0, 1.0) == 1.0

    def test_left_neutrality(self):
        # I(1, y) = y
        for y in POINTS:
            assert I(1.0, y) == round(y, 12)

    def test_falsity_implies_anything(self):
        for y in POINTS:
            assert I(0.0, y) == 1.0

    def test_anything_implies_truth(self):
        for x in POINTS:
            assert I(x, 1.0) == 1.0

    def test_identity_principle(self):
        for x in POINTS:
            assert I(x, x) == 1.0

    def test_ordering_property(self):
        # I(x, y) = 1  <=>  x <= y
        for x, y in pairs():
            if x <= y:
                assert I(x, y) == 1.0
            else:
                assert I(x, y) < 1.0

    def test_negation_is_one_minus_x(self):
        # I(x, 0) = 1 - x
        for x in POINTS:
            assert I(x, 0.0) == pytest.approx(1.0 - x, abs=EPS)

    def test_contraposition(self):
        # I(x, y) = I(1 - y, 1 - x)
        for x, y in pairs():
            assert I(x, y) == pytest.approx(I(1.0 - y, 1.0 - x), abs=EPS)

    def test_exchange_principle(self):
        # I(x, I(y, z)) = I(y, I(x, z))
        for x, y, z in triples():
            assert I(x, I(y, z)) == pytest.approx(I(y, I(x, z)), abs=EPS)

    def test_is_not_commutative(self):
        assert I(0.8, 0.2) == pytest.approx(0.4)
        assert I(0.2, 0.8) == 1.0

    def test_result_bounds_all_points(self):
        for x, y in pairs():
            assert 0.0 <= I(x, y) <= 1.0


class TestBoundedProductTNorm:
    def test_boundary_conditions_match_classical_and(self):
        assert T(0.0, 0.0) == 0.0
        assert T(0.0, 1.0) == 0.0
        assert T(1.0, 0.0) == 0.0
        assert T(1.0, 1.0) == 1.0

    def test_clamped_to_zero(self):
        assert T(0.3, 0.4) == 0.0

    def test_positive_value(self):
        assert T(0.8, 0.7) == pytest.approx(0.5)

    def test_commutativity(self):
        for x, y in pairs():
            assert T(x, y) == T(y, x)

    def test_associativity(self):
        for x, y, z in triples():
            assert T(T(x, y), z) == pytest.approx(T(x, T(y, z)), abs=EPS)

    def test_monotonicity_in_first_arg(self):
        for x1, x2, y in itertools.product(POINTS, repeat=3):
            if x1 <= x2:
                assert T(x1, y) <= T(x2, y)

    def test_monotonicity_in_second_arg(self):
        for y1, y2, x in itertools.product(POINTS, repeat=3):
            if y1 <= y2:
                assert T(x, y1) <= T(x, y2)

    def test_identity_element_is_one(self):
        for x in POINTS:
            assert T(x, 1.0) == round(x, 12)
            assert T(1.0, x) == round(x, 12)

    def test_absorbing_element_is_zero(self):
        for x in POINTS:
            assert T(x, 0.0) == 0.0
            assert T(0.0, x) == 0.0

    def test_result_bounds(self):
        for x, y in pairs():
            assert 0.0 <= T(x, y) <= 1.0

    def test_not_greater_than_min(self):
        for x, y in pairs():
            assert T(x, y) <= min(x, y)

    def test_nilpotency(self):
        # T(x, 1 - x) = 0 для любого x
        for x in TENTHS:
            assert T(x, 1.0 - x) == pytest.approx(0.0, abs=EPS)
