import re
from typing import Optional

from lab1.code.src.domain.fact import Fact
from lab1.code.src.domain.fuzzy_set import FuzzySet
from lab1.code.src.domain.knowledge_base import KnowledgeBase
from lab1.code.src.domain.rule import Rule


class Parser:
    _FACT_PATTERN = re.compile(
        r'^[A-Z][A-Z0-9]*\([a-z](?:[1-9]\d*)?\)\s*=\s*'
        r'\{\s*(?:<[a-z](?:[1-9]\d*)?,\s*(?:0|1|0\.[1-9])>'
        r'\s*(?:,\s*<[a-z](?:[1-9]\d*)?,\s*(?:0|1|0\.[1-9])>\s*)*)?\}$'
    )

    _RULE_PATTERN = re.compile(
        r'^([A-Z][A-Z0-9]*\([a-z](?:[1-9]\d*)?\))'
        r'\s*~>\s*'
        r'([A-Z][A-Z0-9]*\([a-z](?:[1-9]\d*)?\))$'
    )

    _PREDICATE_PATTERN = re.compile(r'^[A-Z][A-Z0-9]*\([a-z](?:[1-9]\d*)?\)')

    _FUZZY_SET_PATTERN = re.compile(
        r'\{\s*(?:<[a-z](?:[1-9]\d*)?,\s*(?:0|1|0\.[1-9])>'
        r'\s*(?:,\s*<[a-z](?:[1-9]\d*)?,\s*(?:0|1|0\.[1-9])>\s*)*)?\}'
    )

    _FUZZY_SET_EL_PATTERN = re.compile(r'<([a-z](?:[1-9]\d*)?)\s*,\s*(0|1|0\.[1-9])>')

    @staticmethod
    def process_factors(filename: str, kb: KnowledgeBase) -> Optional[KnowledgeBase]:
        fuzzy_lines = set()
        rules_lines = set()
        is_facts = False
        with open(filename, 'r') as f:
            for raw_line in f:
                line = raw_line.strip()
                if line == '':
                    continue
                if line == 'facts':
                    is_facts = True
                    continue
                if line == 'rules':
                    is_facts = False
                    continue

                if is_facts:
                    if line in fuzzy_lines:
                        return None
                    fuzzy_lines.add(line)

                    if not re.fullmatch(Parser._FACT_PATTERN, line):
                        return None

                    pred = Parser._PREDICATE_PATTERN.match(line)
                    if pred is None:
                        return None

                    fuzzy_set = Parser._FUZZY_SET_PATTERN.search(line)
                    if fuzzy_set is None:
                        return None

                    fuzzy_set_el = Parser._FUZZY_SET_EL_PATTERN.findall(fuzzy_set.group())
                    temp_fuzzy_set = FuzzySet()
                    for el in fuzzy_set_el:
                        key, value = el
                        temp_fuzzy_set.add((str(key), float(value)))

                    fact = Fact(pred.group(), temp_fuzzy_set)
                    kb.save_fact(pred.group(), fact)

                else:
                    if line in rules_lines:
                        return None
                    rules_lines.add(line)

                    m = re.fullmatch(Parser._RULE_PATTERN, line)
                    if m is None:
                        return None

                    pred_left = m.group(1)
                    pred_right = m.group(2)

                    rule = Rule(pred_left, pred_right)
                    kb.add_rule(rule)

        return kb
