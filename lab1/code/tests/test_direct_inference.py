from domain.fact import Fact
from domain.fuzzy_set import FuzzySet
from domain.knowledge_base import KnowledgeBase
from domain.rule import Rule
from engine.engine import FuzzyInferenceEngine


def make_fact(name, pairs):
    fs = FuzzySet()
    for el, d in pairs:
        fs.add((el, d))
    return Fact(name, fs)


class TestDirectInference:
    def test_no_rules_returns_true(self):
        kb = KnowledgeBase()
        kb.save_fact(make_fact("A", [("x", 0.5)]))
        engine = FuzzyInferenceEngine(kb)
        assert engine.direct_inference() is True

    def test_single_rule_produces_new_fact(self):
        kb = KnowledgeBase()
        a = make_fact("A", [("x", 0.5)])
        b = make_fact("B", [("y", 0.7)])
        kb.save_fact(a)
        kb.save_fact(b)
        kb.add_rule(Rule(a, b))
        engine = FuzzyInferenceEngine(kb)
        collected = []
        engine.direct_inference(on_new_fact=lambda f, r: collected.append(f))
        assert len(collected) >= 1
        assert any(f.pred_name == "B" for f in collected)

    def test_stops_when_ask_continue_false(self):
        kb = KnowledgeBase()
        a = make_fact("A", [("x", 0.5)])
        b = make_fact("B", [("y", 0.7)])
        kb.save_fact(a)
        kb.save_fact(b)
        kb.add_rule(Rule(a, b))
        engine = FuzzyInferenceEngine(kb)
        result = engine.direct_inference(ask_continue=lambda: False)
        assert result is False

    def test_no_duplicate_facts(self):
        kb = KnowledgeBase()
        a = make_fact("A", [("x", 0.5)])
        b = make_fact("B", [("y", 0.7)])
        kb.save_fact(a)
        kb.save_fact(b)
        kb.add_rule(Rule(a, b))
        engine = FuzzyInferenceEngine(kb)
        engine.direct_inference()
        b_facts = kb.facts_by_name("B")
        assert len(b_facts) == 2

    def test_chained_inference(self):
        kb = KnowledgeBase()
        a = make_fact("A", [("x", 0.5)])
        b = make_fact("B", [("y", 0.7)])
        c = make_fact("C", [("z", 0.9)])
        kb.save_fact(a)
        kb.save_fact(b)
        kb.save_fact(c)
        kb.add_rule(Rule(a, b))
        kb.add_rule(Rule(b, c))
        engine = FuzzyInferenceEngine(kb)
        engine.direct_inference()
        c_facts = kb.facts_by_name("C")
        assert len(c_facts) >= 2

    def test_kb_property(self):
        kb = KnowledgeBase()
        engine = FuzzyInferenceEngine(kb)
        assert engine.kb is kb

    def test_on_new_fact_called(self):
        kb = KnowledgeBase()
        a = make_fact("A", [("x", 0.5)])
        b = make_fact("B", [("y", 0.7)])
        kb.save_fact(a)
        kb.save_fact(b)
        kb.add_rule(Rule(a, b))
        engine = FuzzyInferenceEngine(kb)
        calls = []
        engine.direct_inference(on_new_fact=lambda f, r: calls.append((f, r)))
        assert len(calls) >= 1
