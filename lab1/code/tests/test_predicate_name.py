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
