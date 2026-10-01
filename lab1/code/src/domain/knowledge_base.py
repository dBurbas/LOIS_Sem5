# Лабораторная работа №1 по дисциплине ЛОИС
# Выполнена студентами группы 421702 Бурбасом Дмитрием Юрьевичем и
# Башурой Артемом Олеговичем
#
# Файл структуры данных базы знаний, содержащей в себе списки правил и фактов
# и позволяющей получать, добавлять или удалять их.
# 26.09.2026
# Источники:
# TODO: написать источники
from domain.fact import Fact
from domain.rule import Rule


class KnowledgeBase:
    def __init__(self):
        self._rules = []
        self._facts: list[Fact] = []

    def add_rule(self, rule: Rule) -> None:
        self._rules.append(rule)

    def delete_rule(self, index: int) -> None:
        self._rules.pop(index)

    def save_fact(self, fact: Fact) -> bool:
        self._facts.append(fact)

    def has_similar_fact(self, new_fact: Fact) -> bool:
        return any(
            f.pred_name == new_fact.pred_name
            and f.fuzzy_set.almost_equals(new_fact.fuzzy_set)
            for f in self._facts
        )

    def facts_by_name(self, name: str) -> list[Fact]:
        return [f for f in self._facts if f.pred_name == name]

    def get_source_fact(self, name: str) -> Fact | None:
        found = self.facts_by_name(name)
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
