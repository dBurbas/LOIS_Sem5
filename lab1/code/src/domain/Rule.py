from lab1.code.src.domain.Pred import Pred


class Rule:
    def __init__(self, antecedent: Pred, consequent: Pred):
        self._antecedent = antecedent
        self._consequent = consequent

    @property
    def antecedent(self):
        return self._antecedent

    @property
    def consequent(self):
        return self._consequent