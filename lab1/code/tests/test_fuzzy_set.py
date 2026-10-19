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
import pytest

from domain.fuzzy_set import FuzzySet


class TestFuzzySet:
    def test_empty_on_init(self):
        fs = FuzzySet()
        assert fs.elements == set()
        assert fs.membership_pairs == set()

    def test_add_valid(self):
        fs = FuzzySet()
        fs.add(("a", 0.5))
        assert fs.get_membership("a") == 0.5

    def test_add_boundary_zero(self):
        fs = FuzzySet()
        fs.add(("a", 0.0))
        assert fs.get_membership("a") == 0.0

    def test_add_boundary_one(self):
        fs = FuzzySet()
        fs.add(("a", 1.0))
        assert fs.get_membership("a") == 1.0

    def test_add_negative_raises(self):
        fs = FuzzySet()
        with pytest.raises(ValueError):
            fs.add(("a", -0.1))

    def test_add_greater_than_one_raises(self):
        fs = FuzzySet()
        with pytest.raises(ValueError):
            fs.add(("a", 1.1))

    def test_add_overwrites(self):
        fs = FuzzySet()
        fs.add(("a", 0.3))
        fs.add(("a", 0.7))
        assert fs.get_membership("a") == 0.7
        assert len(fs.elements) == 1

    def test_remove_existing(self):
        fs = FuzzySet()
        fs.add(("a", 0.5))
        fs.remove("a")
        assert "a" not in fs.elements

    def test_remove_missing_raises(self):
        fs = FuzzySet()
        with pytest.raises(KeyError):
            fs.remove("a")

    def test_get_membership_default(self):
        fs = FuzzySet()
        assert fs.get_membership("missing") == 0.0

    def test_get_membership_custom_default(self):
        fs = FuzzySet()
        assert fs.get_membership("missing", default=0.5) == 0.5

    def test_get_membership_existing_ignores_default(self):
        fs = FuzzySet()
        fs.add(("a", 0.3))
        assert fs.get_membership("a", default=0.9) == 0.3

    def test_membership_pairs(self):
        fs = FuzzySet()
        fs.add(("a", 0.1))
        fs.add(("b", 0.2))
        assert fs.membership_pairs == {("a", 0.1), ("b", 0.2)}

    def test_elements(self):
        fs = FuzzySet()
        fs.add(("a", 0.1))
        fs.add(("b", 0.2))
        assert fs.elements == {"a", "b"}

    def test_almost_equals_identical(self):
        fs1 = FuzzySet()
        fs1.add(("a", 0.5))
        fs2 = FuzzySet()
        fs2.add(("a", 0.5))
        assert fs1.almost_equals(fs2)

    def test_almost_equals_within_eps(self):
        fs1 = FuzzySet()
        fs1.add(("a", 0.5))
        fs2 = FuzzySet()
        fs2.add(("a", 0.5 + 1e-7))
        assert fs1.almost_equals(fs2)

    def test_almost_equals_outside_eps(self):
        fs1 = FuzzySet()
        fs1.add(("a", 0.5))
        fs2 = FuzzySet()
        fs2.add(("a", 0.6))
        assert not fs1.almost_equals(fs2)

    def test_almost_equals_different_elements(self):
        fs1 = FuzzySet()
        fs1.add(("a", 0.5))
        fs2 = FuzzySet()
        fs2.add(("b", 0.5))
        assert not fs1.almost_equals(fs2)

    def test_almost_equals_missing_treated_as_zero(self):
        fs1 = FuzzySet()
        fs1.add(("a", 0.0))
        fs2 = FuzzySet()
        assert fs1.almost_equals(fs2)

    def test_almost_equals_custom_eps(self):
        fs1 = FuzzySet()
        fs1.add(("a", 0.5))
        fs2 = FuzzySet()
        fs2.add(("a", 0.51))
        assert fs1.almost_equals(fs2, eps=0.02)
        assert not fs1.almost_equals(fs2, eps=0.001)
