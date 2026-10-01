# Лабораторная работа №1 по дисциплине ЛОИС
# Выполнена студентами группы 421702 Бурбасом Дмитрием Юрьевичем и
# Башурой Артемом Олеговичем
#
# Файл функций прямого логического вывода (modus ponens,
# полный цикл вывода новых факто), использующих треугольную
# норму граничного произведения и импликацию Лукасевича
# 27.09.2026
# Источники:
# TODO: Написать источники

from domain.fact import Fact, FuzzySet
from domain.knowledge_base import KnowledgeBase
from domain.rule import Rule
from engine.operations import bounded_product_t_norm


class FuzzyInferenceEngine:
    def __init__(self, kb: KnowledgeBase):
        self._kb = kb

    @property
    def kb(self):
        return self._kb

    @staticmethod
    def generalized_modus_ponens(rule: Rule, observation: Fact) -> Fact:
        """Функция нечеткого правила прямого логического вывода (modus ponens)
        через треугольную норму граничного произведения и импликацию Лукасевича.

        :param rule: Правило
        :type rule: Rule
        :param observation: Факт
        :type observation: Fact
        :return: Новый факт
        :rtype: Fact
        """
        result = FuzzySet()
        for consequent_elem in rule.consequent_elements:
            sup_result = max(
                bounded_product_t_norm(
                    observation.fuzzy_set.get_membership(antecedent_elem),
                    rule.relation[(antecedent_elem, consequent_elem)],
                )
                for antecedent_elem in rule.antecedent_elements
            )
            result.add((consequent_elem, sup_result))
        return Fact(rule.consequent_name, result)

    def direct_inference(
        self,
        on_new_fact: callable = lambda fact, rule: None,
        ask_continue: callable = lambda: True,
    ) -> bool:
        """
        Функция вывода новых фактов, с помощью правил в базе знаний

        :param on_new_fact: Вызывается на каждом новом факте, значение по-умолчанию функция, возвращающая `None`
        :type on_new_fact: callable(fact, rule)
        :param ask_continue: Функция прерывания, значение по-умолчанию функция, всегда возвращающая `True`
        :type ask_continue: callable()
        :return: `True` когда вывод выполнен полностью без прерывания, `False` если был прерван пользователем.
        :rtype: bool
        """
        try:
            changed = True
            while changed:
                changed = False
                for rule in self.kb.rules:
                    for observation in list(
                        self.kb.facts_by_name(rule.antecedent_name)
                    ):
                        new_fact = self.generalized_modus_ponens(rule, observation)
                        if self.kb.has_similar_fact(new_fact):
                            continue
                        self.kb.save_fact(new_fact)
                        changed = True
                        on_new_fact(new_fact, rule)

                        if not ask_continue():
                            return False
        except KeyboardInterrupt:
            return False
        return True
