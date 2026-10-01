# Лабораторная работа №1 по дисциплине ЛОИС
# Выполнена студентами группы 421702 Бурбасом Дмитрием Юрьевичем и
# Башурой Артемом Олеговичем
#
# Файл структуры данных логического правила (например A(x) ~> B(y))
# который хранит матрицу значений импликации между элементами антецедента
# и консеквента
# 26.09.2026
# Источники:
# TODO: написать источники
from domain.fact import Fact
from engine.operations import lukasevich_implication


class Rule:
    def __init__(self, antecedent: Fact, consequent: Fact):
        self._antecedent_name: str = antecedent.pred_name
        self._consequent_name: str = consequent.pred_name
        self._antecedent_elements: set[str] = antecedent.fuzzy_set.elements
        self._consequent_elements: set[str] = consequent.fuzzy_set.elements
        self._relation = {
            (a, c): lukasevich_implication(
                antecedent.fuzzy_set.get_membership(a),
                consequent.fuzzy_set.get_membership(c),
            )
            for a in self._antecedent_elements
            for c in self._consequent_elements
        }

    @property
    def antecedent_name(self) -> str:
        return self._antecedent_name

    @property
    def consequent_name(self) -> str:
        return self._consequent_name

    @property
    def antecedent_elements(self) -> set[str]:
        return self._antecedent_elements

    @property
    def consequent_elements(self) -> set[str]:
        return self._consequent_elements

    @property
    def relation(self) -> dict[tuple[str, str], float]:
        return self._relation
