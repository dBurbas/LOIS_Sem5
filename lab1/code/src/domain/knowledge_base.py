# Лабораторная работа №1 по дисциплине ЛОИС
# Выполнена студентами группы 421702 Бурбасом Дмитрием Юрьевичем и
# Башурой Артемом Олеговичем
#
# Файл структуры данных базы знаний, содержащей в себе списки правил и фактов
# и позволяющей получать, добавлять или удалять их.
# 26.09.2026
# Источники:
# Блюмин, С. Л. Нечёткая логика: алгебраические основы и приложения /
# С. Л. Блюмин, И. А. Шуйкова, П. В. Сараев, И. В. Черпаков. –
# Липецк : ЛЭГИ, 2002. – 111 с.

from domain.fact import Fact
from domain.rule import Rule


class KnowledgeBase:
    def __init__(self):
        self._rules: list[Rule] = []
        self._facts: list[Fact] = []

    def add_rule(self, rule: Rule) -> None:
        self._rules.append(rule)

    def delete_rule(self, index: int) -> None:
        self._rules.pop(index)

    def fact_unique_name(self, base: str) -> str:
        taken = {f.pred_name for f in self._facts}
        if base not in taken:
            return base
        i = 1
        while f"{base}{i}" in taken:
            i += 1
        return f"{base}{i}"

    def save_fact(self, fact: Fact) -> bool:
        self._facts.append(fact)

    def has_similar_fact(self, new_fact: Fact) -> bool:
        return any(
            f.fuzzy_set.elements == new_fact.fuzzy_set.elements
            and f.fuzzy_set.almost_equals(new_fact.fuzzy_set)
            for f in self._facts
        )

    def facts_by_name(self, name: str) -> list[Fact]:
        return [f for f in self._facts if f.pred_name == name]

    def facts_by_domain(self, domain: set[str]):
        return [f for f in self._facts if domain.issubset(f.fuzzy_set.elements)]

    def get_source_fact(self, name: str) -> Fact | None:
        found = self.facts_by_name(name)
        return found[0] if found else None

    def rule_by_antecedent_consequent(self, antec: str, conseq: str) -> Rule:
        found = [
            r
            for r in self._rules
            if r.antecedent_name == antec and r.consequent_name == conseq
        ]
        return found[0] if found else None

    # ?: возможно нужно удалять по имени (но тогда удаляется сразу много фактов)
    def remove_fact(self, fact: Fact) -> None:
        try:
            self._facts.remove(fact)
        except ValueError:
            raise KeyError(f"Факт '{fact.pred_name}' не найден")

    @property
    def rules(self) -> list[Rule]:
        return self._rules

    @property
    def facts(self) -> list[Fact]:
        return self._facts
