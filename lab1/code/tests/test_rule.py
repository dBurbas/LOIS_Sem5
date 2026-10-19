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
from engine.operations import lukasevich_implication


def make_fact(name, pairs):
    fs = FuzzySet()
    for el, d in pairs:
        fs.add((el, d))
    return Fact(name, fs)


class TestRule:
    def test_antecedent_name(self):
        rule = Rule(make_fact("A", [("x", 0.5)]), make_fact("B", [("y", 0.5)]))
        assert rule.antecedent_name == "A"

    def test_consequent_name(self):
        rule = Rule(make_fact("A", [("x", 0.5)]), make_fact("B", [("y", 0.5)]))
        assert rule.consequent_name == "B"

    def test_antecedent_elements(self):
        rule = Rule(
            make_fact("A", [("x", 0.5), ("z", 0.3)]), make_fact("B", [("y", 0.5)])
        )
        assert rule.antecedent_elements == {"x", "z"}

    def test_consequent_elements(self):
        rule = Rule(
            make_fact("A", [("x", 0.5)]), make_fact("B", [("y", 0.5), ("w", 0.2)])
        )
        assert rule.consequent_elements == {"y", "w"}

    def test_relation_size(self):
        rule = Rule(
            make_fact("A", [("x", 0.5), ("z", 0.3)]),
            make_fact("B", [("y", 0.5), ("w", 0.2)]),
        )
        assert len(rule.relation) == 4

    def test_relation_keys(self):
        rule = Rule(make_fact("A", [("x", 0.5)]), make_fact("B", [("y", 0.5)]))
        assert set(rule.relation.keys()) == {("x", "y")}

    def test_relation_values(self):
        rule = Rule(make_fact("A", [("x", 0.8)]), make_fact("B", [("y", 0.3)]))
        expected = lukasevich_implication(0.8, 0.3)
        assert rule.relation[("x", "y")] == pytest.approx(expected)

    def test_relation_values_multiple(self):
        a = make_fact("A", [("x", 0.8), ("z", 0.2)])
        b = make_fact("B", [("y", 0.3), ("w", 0.9)])
        rule = Rule(a, b)
        for ae in a.fuzzy_set.elements:
            for ce in b.fuzzy_set.elements:
                expected = lukasevich_implication(
                    a.fuzzy_set.get_membership(ae),
                    b.fuzzy_set.get_membership(ce),
                )
                assert rule.relation[(ae, ce)] == pytest.approx(expected)

    def test_empty_antecedent(self):
        rule = Rule(make_fact("A", []), make_fact("B", [("y", 0.5)]))
        assert rule.antecedent_elements == set()
        assert rule.relation == {}

    def test_empty_consequent(self):
        rule = Rule(make_fact("A", [("x", 0.5)]), make_fact("B", []))
        assert rule.consequent_elements == set()
        assert rule.relation == {}
