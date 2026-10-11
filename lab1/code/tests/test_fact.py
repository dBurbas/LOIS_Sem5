import pytest

from domain.fact import Fact
from domain.fuzzy_set import FuzzySet


class TestFact:
    def test_pred_name(self):
        fs = FuzzySet()
        fact = Fact("A", fs)
        assert fact.pred_name == "A"

    def test_fuzzy_set(self):
        fs = FuzzySet()
        fs.add(("x", 0.5))
        fact = Fact("A", fs)
        assert fact.fuzzy_set is fs
        assert fact.fuzzy_set.get_membership("x") == 0.5

    def test_empty_fuzzy_set(self):
        fact = Fact("A", FuzzySet())
        assert fact.fuzzy_set.elements == set()

    def test_attributes_are_read_only(self):
        fact = Fact("A", FuzzySet())
        with pytest.raises(AttributeError):
            fact.pred_name = "B"
        with pytest.raises(AttributeError):
            fact.fuzzy_set = FuzzySet()
