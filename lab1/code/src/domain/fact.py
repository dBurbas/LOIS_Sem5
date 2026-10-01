# Лабораторная работа №1 по дисциплине ЛОИС
# Выполнена студентами группы 421702 Бурбасом Дмитрием Юрьевичем и
# Башурой Артемом Олеговичем
#
# Файл структуры данных факта, которая хранит имя предиката и нечеткое множество.
# 26.09.2026
# Источники:
# TODO: написать источники
from domain.fuzzy_set import FuzzySet


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
