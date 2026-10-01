# Лабораторная работа №1 по дисциплине ЛОИС
# Выполнена студентами группы 421702 Бурбасом Дмитрием Юрьевичем и
# Башурой Артемом Олеговичем
#
# Файл класса парсера, для перевода данных из файла базы знаний в
# внутреннюю структуру данных KnowledgeBase
# 28.09.2026
# Источники:
# TODO: написать источники
import re
from collections.abc import Iterator

from domain.fact import Fact
from domain.fuzzy_set import FuzzySet
from domain.knowledge_base import KnowledgeBase
from domain.rule import Rule


class ParseError(ValueError):
    """Некорректный файл базы знаний."""

    def __init__(self, message: str, line_no: int | None = None):
        self.line_no = line_no
        prefix = f"Строка {line_no}: " if line_no is not None else ""
        super().__init__(prefix + message)


_NAME = r"[A-Za-z][A-Za-z0-9]*"
_DEGREE = r"(?:1(?:\.0+)?|0(?:\.[0-9]+)?)"
_PREDICATE = rf"{_NAME}\(\s*{_NAME}\s*\)"
_PAIR = rf"<\s*{_NAME}\s*,\s*{_DEGREE}\s*>"

_FACT_RE = re.compile(
    rf"(?P<pred>{_PREDICATE})\s*=\s*\{{\s*(?P<body>{_PAIR}(?:\s*,\s*{_PAIR})*)\s*\}}"
)
_RULE_RE = re.compile(rf"(?P<left>{_PREDICATE})\s*~>\s*(?P<right>{_PREDICATE})")
_PAIR_RE = re.compile(rf"<\s*(?P<el>{_NAME})\s*,\s*(?P<deg>{_DEGREE})\s*>")
_PRED_PARTS_RE = re.compile(rf"(?P<name>{_NAME})\(\s*(?P<var>{_NAME})\s*\)")

_FACTS_HEADER = "facts"
_RULES_HEADER = "rules"
_COMMENT_PREFIXES = ("#", "//")


class Parser:
    @staticmethod
    def _iter_lines(filename: str) -> Iterator[tuple[int, str]]:
        """Отдаёт (номер строки, очищенная строка), пропуская пустые и комментарии."""
        with open(filename, "r", encoding="utf-8") as f:
            for line_no, raw in enumerate(f, start=1):
                line = raw.strip().lstrip("\ufeff")
                if not line or line.startswith(_COMMENT_PREFIXES):
                    continue
                yield line_no, line

    @staticmethod
    def _predicate_name(predicate: str) -> str:
        """'A(x)' -> 'A' (переменная не входит в имя факта)."""
        m = _PRED_PARTS_RE.fullmatch(predicate)
        if m is None:
            raise ParseError(f"некорректный предикат '{predicate}'")
        return m.group("name")

    @staticmethod
    def _parse_fuzzy_set(body: str, line_no: int) -> FuzzySet:
        fuzzy_set = FuzzySet()
        seen: set[str] = set()
        for m in _PAIR_RE.finditer(body):
            element, degree = m.group("el"), float(m.group("deg"))
            if element in seen:
                raise ParseError(
                    f"элемент '{element}' повторяется в множестве", line_no
                )
            seen.add(element)
            fuzzy_set.add((element, degree))
        return fuzzy_set

    @staticmethod
    def _parse_fact(line: str, line_no: int) -> Fact:
        m = _FACT_RE.fullmatch(line)
        if m is None:
            raise ParseError(f"некорректный факт: '{line}'", line_no)
        name = Parser._predicate_name(m.group("pred"))
        return Fact(name, Parser._parse_fuzzy_set(m.group("body"), line_no))

    @staticmethod
    def _parse_rule(line: str, line_no: int) -> tuple[str, str]:
        m = _RULE_RE.fullmatch(line)
        if m is None:
            raise ParseError(f"некорректное правило: '{line}'", line_no)
        return (
            Parser._predicate_name(m.group("left")),
            Parser._predicate_name(m.group("right")),
        )

    @staticmethod
    def _collect_sections(
        filename: str,
    ) -> tuple[list[tuple[int, str]], list[tuple[int, str]]]:
        """Разносит значимые строки по секциям. Всё до первого заголовка игнорируется.
        Строка без маркера секции ('=' для фактов, '~>' для правил) игнорируется;
        строка с маркером обязана быть корректной (проверяется позже)."""
        fact_lines: list[tuple[int, str]] = []
        rule_lines: list[tuple[int, str]] = []
        section = None
        for line_no, line in Parser._iter_lines(filename):
            if line == _FACTS_HEADER:
                section = _FACTS_HEADER
            elif line == _RULES_HEADER:
                section = _RULES_HEADER
            elif section == _FACTS_HEADER and "=" in line:
                fact_lines.append((line_no, line))
            elif section == _RULES_HEADER and "~>" in line:
                rule_lines.append((line_no, line))
        return fact_lines, rule_lines

    @staticmethod
    def _load_facts(kb: KnowledgeBase, fact_lines: list[tuple[int, str]]) -> None:
        names: set[str] = set()
        for line_no, line in fact_lines:
            fact = Parser._parse_fact(line, line_no)
            if fact.pred_name in names:
                raise ParseError(f"факт '{fact.pred_name}' определён повторно", line_no)
            names.add(fact.pred_name)
            kb.save_fact(fact)

    @staticmethod
    def _load_rules(kb: KnowledgeBase, rule_lines: list[tuple[int, str]]) -> None:
        seen: set[tuple[str, str]] = set()
        for line_no, line in rule_lines:
            left_name, right_name = Parser._parse_rule(line, line_no)
            if (left_name, right_name) in seen:
                raise ParseError(f"правило '{line}' повторяется", line_no)
            seen.add((left_name, right_name))

            left = kb.get_source_fact(left_name)
            right = kb.get_source_fact(right_name)
            if left is None or right is None:
                missing = left_name if left is None else right_name
                raise ParseError(f"для предиката '{missing}' нет факта", line_no)
            kb.add_rule(Rule(left, right))

    @staticmethod
    def process_knowledge_base(filename: str) -> KnowledgeBase:
        """Читает файл и возвращает KnowledgeBase. При ошибке в файле бросает ParseError."""
        fact_lines, rule_lines = Parser._collect_sections(filename)
        if not fact_lines:
            raise ParseError("в файле нет ни одного факта")

        kb = KnowledgeBase()
        Parser._load_facts(kb, fact_lines)
        Parser._load_rules(kb, rule_lines)
        return kb
