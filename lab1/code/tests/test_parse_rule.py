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
