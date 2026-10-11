import pytest

from parser.parser import Parser, ParseError


class TestParseRule:
    def test_simple(self):
        left, right = Parser._parse_rule("A(x) ~> B(y)", 1)
        assert left == "A"
        assert right == "B"

    def test_spaces(self):
        left, right = Parser._parse_rule("A( x )  ~>  B( y )", 1)
        assert left == "A"
        assert right == "B"

    def test_invalid(self):
        with pytest.raises(ParseError):
            Parser._parse_rule("garbage", 1)
