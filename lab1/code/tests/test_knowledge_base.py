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
from domain.knowledge_base import KnowledgeBase
from domain.rule import Rule


def make_fact(name, pairs):
    fs = FuzzySet()
    for el, d in pairs:
        fs.add((el, d))
    return Fact(name, fs)


class TestKnowledgeBase:
    def test_init_empty(self):
        kb = KnowledgeBase()
        assert kb.rules == []
        assert kb.facts == []

    def test_add_rule(self):
        kb = KnowledgeBase()
        a = make_fact("A", [("x", 0.5)])
        b = make_fact("B", [("y", 0.5)])
        rule = Rule(a, b)
        kb.add_rule(rule)
        assert kb.rules == [rule]

    def test_delete_rule(self):
        kb = KnowledgeBase()
        a = make_fact("A", [("x", 0.5)])
        b = make_fact("B", [("y", 0.5)])
        r1 = Rule(a, b)
        r2 = Rule(b, a)
        kb.add_rule(r1)
        kb.add_rule(r2)
        kb.delete_rule(0)
        assert kb.rules == [r2]

    def test_delete_rule_invalid_index(self):
        kb = KnowledgeBase()
        with pytest.raises(IndexError):
            kb.delete_rule(0)

    def test_save_fact(self):
        kb = KnowledgeBase()
        f = make_fact("A", [("x", 0.5)])
        kb.save_fact(f)
        assert kb.facts == [f]

    def test_has_similar_fact_same(self):
        kb = KnowledgeBase()
        kb.save_fact(make_fact("A", [("x", 0.5)]))
        assert kb.has_similar_fact(make_fact("A", [("x", 0.5)]))

    def test_has_similar_fact_different_name(self):
        kb = KnowledgeBase()
        kb.save_fact(make_fact("A", [("x", 0.5)]))
        assert not kb.has_similar_fact(make_fact("B", [("x", 0.5)]))

    def test_has_similar_fact_different_values(self):
        kb = KnowledgeBase()
        kb.save_fact(make_fact("A", [("x", 0.5)]))
        assert not kb.has_similar_fact(make_fact("A", [("x", 0.6)]))

    def test_has_similar_fact_empty_kb(self):
        kb = KnowledgeBase()
        assert not kb.has_similar_fact(make_fact("A", [("x", 0.5)]))

    def test_facts_by_name(self):
        kb = KnowledgeBase()
        f1 = make_fact("A", [("x", 0.5)])
        f2 = make_fact("A", [("y", 0.5)])
        f3 = make_fact("B", [("z", 0.5)])
        kb.save_fact(f1)
        kb.save_fact(f2)
        kb.save_fact(f3)
        assert kb.facts_by_name("A") == [f1, f2]
        assert kb.facts_by_name("B") == [f3]
        assert kb.facts_by_name("C") == []

    def test_get_source_fact(self):
        kb = KnowledgeBase()
        f = make_fact("A", [("x", 0.5)])
        kb.save_fact(f)
        assert kb.get_source_fact("A") is f

    def test_get_source_fact_missing(self):
        kb = KnowledgeBase()
        assert kb.get_source_fact("A") is None

    def test_get_source_fact_returns_first(self):
        kb = KnowledgeBase()
        f1 = make_fact("A", [("x", 0.5)])
        f2 = make_fact("A", [("y", 0.5)])
        kb.save_fact(f1)
        kb.save_fact(f2)
        assert kb.get_source_fact("A") is f1

    def test_remove_fact(self):
        kb = KnowledgeBase()
        f = make_fact("A", [("x", 0.5)])
        kb.save_fact(f)
        kb.remove_fact(f)
        assert kb.facts == []

    def test_remove_fact_missing(self):
        kb = KnowledgeBase()
        f = make_fact("A", [("x", 0.5)])
        with pytest.raises(KeyError):
            kb.remove_fact(f)

    def test_rules_property_returns_list(self):
        kb = KnowledgeBase()
        assert isinstance(kb.rules, list)

    def test_facts_property_returns_list(self):
        kb = KnowledgeBase()
        assert isinstance(kb.facts, list)
