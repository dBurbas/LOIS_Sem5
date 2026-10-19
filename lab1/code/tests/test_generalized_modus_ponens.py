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

from domain.fact import Fact
from domain.fuzzy_set import FuzzySet
from domain.rule import Rule
from engine.engine import FuzzyInferenceEngine
from engine.operations import bounded_product_t_norm


def make_fact(name, pairs):
    fs = FuzzySet()
    for el, d in pairs:
        fs.add((el, d))
    return Fact(name, fs)


class TestGeneralizedModusPonens:
    def test_single_element_exact_match(self):
        a = make_fact("A", [("x", 1.0)])
        b = make_fact("B", [("y", 1.0)])
        rule = Rule(a, b)
        obs = make_fact("A", [("x", 1.0)])
        result = FuzzyInferenceEngine.generalized_modus_ponens(rule, obs)
        assert result.pred_name == "B"
        assert result.fuzzy_set.get_membership("y") == pytest.approx(1.0)

    def test_single_element_no_match(self):
        a = make_fact("A", [("x", 1.0)])
        b = make_fact("B", [("y", 1.0)])
        rule = Rule(a, b)
        obs = make_fact("A", [("x", 0.0)])
        result = FuzzyInferenceEngine.generalized_modus_ponens(rule, obs)
        assert result.fuzzy_set.get_membership("y") == pytest.approx(0.0)

    def test_result_name_is_consequent_name(self):
        a = make_fact("A", [("x", 0.5)])
        b = make_fact("B", [("y", 0.5)])
        rule = Rule(a, b)
        obs = make_fact("A", [("x", 0.5)])
        result = FuzzyInferenceEngine.generalized_modus_ponens(rule, obs)
        assert result.pred_name == "B"

    def test_max_over_antecedents(self):
        a = make_fact("A", [("x", 0.9), ("z", 0.2)])
        b = make_fact("B", [("y", 1.0)])
        rule = Rule(a, b)
        obs = make_fact("A", [("x", 0.9), ("z", 0.2)])
        result = FuzzyInferenceEngine.generalized_modus_ponens(rule, obs)
        expected = max(
            bounded_product_t_norm(0.9, rule.relation[("x", "y")]),
            bounded_product_t_norm(0.2, rule.relation[("z", "y")]),
        )
        assert result.fuzzy_set.get_membership("y") == pytest.approx(expected)

    def test_multiple_consequents(self):
        a = make_fact("A", [("x", 1.0)])
        b = make_fact("B", [("y", 0.5), ("w", 0.8)])
        rule = Rule(a, b)
        obs = make_fact("A", [("x", 1.0)])
        result = FuzzyInferenceEngine.generalized_modus_ponens(rule, obs)
        assert result.fuzzy_set.elements == {"y", "w"}

    def test_observation_missing_element_defaults_zero(self):
        a = make_fact("A", [("x", 1.0)])
        b = make_fact("B", [("y", 1.0)])
        rule = Rule(a, b)
        obs = make_fact("A", [])
        result = FuzzyInferenceEngine.generalized_modus_ponens(rule, obs)
        assert result.fuzzy_set.get_membership("y") == pytest.approx(0.0)
