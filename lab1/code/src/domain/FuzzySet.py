from typing import Any, Tuple

class FuzzySet:
    def __init__(self):
        self.__fuzzy_dict = {}

    def add(self, item: Tuple[Any, float]):
        element, degree = item
        self._validate(degree)
        self.__fuzzy_dict[element] = degree

    def remove(self, element: Any):
        del self.__fuzzy_dict[element]

    @property
    def fuzzy_set(self):
        return set(self.__fuzzy_dict.items())

    def _validate(self, degree:float) -> None:
        if not (0.0 <= degree <= 1.0):
            raise ValueError(f"Степень принадлежности должна быть от 0 до 1. Получено: {degree}")