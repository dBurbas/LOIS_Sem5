class FuzzySet:
    def __init__(self):
        self._fuzzy_dict = {}

    def add(self, item: tuple[str, float]) -> None:
        element, degree = item
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

    def almost_equals(self, other: "FuzzySet", eps: float = 1e-6) -> bool:
        keys = self.elements | other.elements
        return all(abs(self.get_elem_val(k[0]) - other.get_elem_val(k[0])) < eps for k in keys)
