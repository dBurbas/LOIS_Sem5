from lab1.code.src.domain.FuzzySet import FuzzySet


class Fact:
    def __init__(self, pred_name: str, fuzzy_set: FuzzySet):
        self._pred_name = pred_name
        self._fuzzy_set = fuzzy_set

    @property
    def pred_name(self):
        return self._pred_name

    @property
    def fuzzy_set(self):
        return self._fuzzy_set