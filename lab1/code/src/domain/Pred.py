class Pred:
    def __init__(self, name: str):
        self._name = name

    # ?: нужно ли двойное нижнее подчеркивание
    # TODO: реализовать валидацию
    def _validate(self, name: str) -> bool:
        return True

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if not self._validate(value):
            raise ValueError(f"Недопустимое значение предиката: '{value}'.")
        self._name = value
