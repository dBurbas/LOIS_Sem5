import pytest

from parser.parser import Parser, ParseError


class TestPredicateName:
    def test_simple(self):
        assert Parser._predicate_name("A(x)") == "A"

    def test_with_spaces(self):
        assert Parser._predicate_name("A( x )") == "A"

    def test_alphanumeric(self):
        assert Parser._predicate_name("Pred1(x)") == "Pred1"

    def test_invalid_no_parens(self):
        with pytest.raises(ParseError):
            Parser._predicate_name("A")

    def test_invalid_no_var(self):
        with pytest.raises(ParseError):
            Parser._predicate_name("A()")

    def test_invalid_numeric_start(self):
        with pytest.raises(ParseError):
            Parser._predicate_name("1A(x)")
