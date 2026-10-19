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


class TestParseFuzzySet:
    def test_single_pair(self):
        fs = Parser._parse_fuzzy_set("<a, 0.5>", 1)
        assert fs.get_membership("a") == 0.5

    def test_multiple_pairs(self):
        fs = Parser._parse_fuzzy_set("<a, 0.5>, <b, 0.7>", 1)
        assert fs.get_membership("a") == 0.5
        assert fs.get_membership("b") == 0.7

    def test_boundary_values(self):
        fs = Parser._parse_fuzzy_set("<a, 0>, <b, 1>", 1)
        assert fs.get_membership("a") == 0.0
        assert fs.get_membership("b") == 1.0

    def test_one_with_decimal(self):
        fs = Parser._parse_fuzzy_set("<a, 1.0>", 1)
        assert fs.get_membership("a") == 1.0

    def test_duplicate_element_raises(self):
        with pytest.raises(ParseError):
            Parser._parse_fuzzy_set("<a, 0.5>, <a, 0.7>", 1)

    def test_whitespace_tolerance(self):
        fs = Parser._parse_fuzzy_set("< a , 0.5 >", 1)
        assert fs.get_membership("a") == 0.5
