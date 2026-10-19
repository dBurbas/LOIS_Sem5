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
from domain.fact import Fact
from domain.fuzzy_set import FuzzySet
from domain.knowledge_base import KnowledgeBase
from domain.rule import Rule
from parser.parser import Parser
from parser.saver import save_knowledge_base


def make_fact(name, pairs):
    fs = FuzzySet()
    for el, d in pairs:
        fs.add((el, d))
    return Fact(name, fs)


class TestSaveKnowledgeBase:
    def test_roundtrip_simple(self, tmp_path):
        kb = KnowledgeBase()
        a = make_fact("A", [("x", 0.5)])
        b = make_fact("B", [("y", 0.7)])
        kb.save_fact(a)
        kb.save_fact(b)
        kb.add_rule(Rule(a, b))
        out = tmp_path / "out.txt"
        save_knowledge_base(kb, str(out))
        loaded = Parser.process_knowledge_base(str(out))
        assert len(loaded.facts) == 2
        assert len(loaded.rules) == 1

    def test_no_rules(self, tmp_path):
        kb = KnowledgeBase()
        kb.save_fact(make_fact("A", [("x", 0.5)]))
        out = tmp_path / "out.txt"
        save_knowledge_base(kb, str(out))
        content = out.read_text()
        assert "rules" not in content

    def test_with_rules_section(self, tmp_path):
        kb = KnowledgeBase()
        a = make_fact("A", [("x", 0.5)])
        b = make_fact("B", [("y", 0.7)])
        kb.save_fact(a)
        kb.save_fact(b)
        kb.add_rule(Rule(a, b))
        out = tmp_path / "out.txt"
        save_knowledge_base(kb, str(out))
        content = out.read_text()
        assert "rules" in content

    def test_boundary_values_format(self, tmp_path):
        kb = KnowledgeBase()
        kb.save_fact(make_fact("A", [("x", 0.0), ("y", 1.0)]))
        out = tmp_path / "out.txt"
        save_knowledge_base(kb, str(out))
        content = out.read_text()
        assert "<x, 0.0>" in content
        assert "<y, 1.0>" in content

    def test_deduplicates_facts(self, tmp_path):
        kb = KnowledgeBase()
        f = make_fact("A", [("x", 0.5)])
        kb.save_fact(f)
        kb.save_fact(f)
        out = tmp_path / "out.txt"
        save_knowledge_base(kb, str(out))
        content = out.read_text()
        assert content.count("A(x)") == 1
