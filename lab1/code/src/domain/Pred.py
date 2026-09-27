class Pred:
    def __init__(self, pred: str):
        self.pred = pred

    def __validate(self, pred: str) -> bool:
        return True

    @property
    def pred(self):
        return self._pred

    @pred.setter
    def pred(self, value: str):
        if not self.__validate(value):
            raise ValueError(f"Недопустимое значение предиката: '{value}'.")
        self._pred = value