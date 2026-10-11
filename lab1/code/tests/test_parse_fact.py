import pytest

from parser.parser import Parser, ParseError


class TestParseFact:
    def test_simple(self):
        fact = Parser._parse_fact("A(x) = {<a, 0.5>}", 1)
        assert fact.pred_name == "A"
        assert fact.fuzzy_set.get_membership("a") == 0.5

    def test_multiple_pairs(self):
        fact = Parser._parse_fact("A(x) = {<a, 0.5>, <b, 0.7>}", 1)
        assert fact.fuzzy_set.elements == {"a", "b"}

    def test_invalid(self):
        with pytest.raises(ParseError):
            Parser._parse_fact("garbage", 1)
