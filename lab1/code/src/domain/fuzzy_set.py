# Лабораторная работа №1 по дисциплине ЛОИС
# Выполнена студентами группы 421702 Бурбасом Дмитрием Юрьевичем и
# Башурой Артемом Олеговичем
#
# Файл структуры данных нечеткого множества, которая хранит словарь
# вида: {"элемент": значение функции принадлежности} и позволяет получать доступ
# к элементам, добавлять новые элементы, удалять элементы из множества.
# 26.09.2026
# Источники:
# TODO: написать источники
class FuzzySet:
    def __init__(self):
        self._fuzzy_dict = {}

    def add(self, item: tuple[str, float]) -> None:
        if not (0 <= item[1] <= 1):
            raise ValueError(
                f"Степень принадлежности должна быть в отрезке [0,1] (получено {item[1]})"
            )
        element, membership_degree = item
        self._fuzzy_dict[element] = membership_degree

    def remove(self, element: str) -> None:
        if element not in self._fuzzy_dict:
            raise KeyError(f"Элемент '{element}' отсутствует в нечётком множестве")
        del self._fuzzy_dict[element]

    def get_membership(self, element: str, default: float = 0.0) -> float:
        return self._fuzzy_dict.get(element, default)

    @property
    def membership_pairs(self) -> set[tuple[str, float]]:
        return set(self._fuzzy_dict.items())

    @property
    def elements(self) -> set[str]:
        return set(self._fuzzy_dict)

    def almost_equals(self, other: "FuzzySet", eps: float = 1e-6) -> bool:
        elements = self.elements | other.elements
        return all(
            abs(self.get_membership(e) - other.get_membership(e)) <= eps
            for e in elements
        )
