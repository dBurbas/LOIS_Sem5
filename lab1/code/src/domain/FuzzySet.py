class FuzzySet:
    def __init__(self):
        self._fuzzy_dict = {}

    def add(self, item: tuple[str, float]) -> None:
        element, degree = item
        self._validate(degree)
        self._fuzzy_dict[element] = degree

    def remove(self, element: str):
        if element not in self._fuzzy_dict:
            raise KeyError(f"Элемент '{element}' отсутствует в нечётком множестве")
        del self._fuzzy_dict[element]

    def get_elem_val(self, element: str, default: float = 0.0) -> float:
        return self._fuzzy_dict.get(element, default)

    @property
    def elements(self):
        return set(self._fuzzy_dict.items())

    def _validate(self, degree: float) -> None:
        if not (0.0 <= degree <= 1.0):
            raise ValueError(
                f"Степень принадлежности должна быть от 0 до 1. Получено: {degree}"
            )
