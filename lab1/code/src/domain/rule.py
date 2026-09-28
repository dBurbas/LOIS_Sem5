class Rule:
    def __init__(self, antecedent: str, consequent: str):
        self._antecedent = antecedent
        self._consequent = consequent

    @property
    def antecedent(self):
        return self._antecedent

    @property
    def consequent(self):
        return self._consequent
