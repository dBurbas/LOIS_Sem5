# Лабораторная работа №1 по дисциплине ЛОИС
# Выполнена студентами группы 421702 Бурбасом Дмитрием Юрьевичем и
# Башурой Артемом Олеговичем
#
# Файл основного цикла программы для ручного тестирования фукнционала программы
# 29.09.2026
# Источники:
# TODO: написать источники
import sys

import questionary
from domain.fuzzy_set import FuzzySet
from domain.knowledge_base import Fact, KnowledgeBase, Rule
from engine.engine import FuzzyInferenceEngine
from parser.parser import Parser
from parser.saver import save_knowledge_base
from questionary import Style
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

STOP_COMMANDS = {"q", "quit", "stop", "exit"}


def fuzzy_set_to_str(fuzzy_set: FuzzySet) -> str:
    return (
        "{"
        + ", ".join(
            f"{elem}/{round(membership, 3)}"
            for elem, membership in fuzzy_set.membership_pairs
        )
        + "}"
    )


def fact_to_str(fact: Fact, pred_var: str = "x") -> str:
    return str(f"{fact.pred_name}({pred_var}) = {fuzzy_set_to_str(fact.fuzzy_set)}")


def inferenced_fact_print(
    fact: Fact, rule: Rule, var1: str = "x", var2: str = "y"
) -> None:
    """Вывод в консоль выведенного нового факта на основе правила
    с отображением формулы вывода.
    :param fact: Новый выведенный факт
    :param rule: Правило на основе которого выведен факт
    :param var1: Переменная для антецедента
    :param var2: Переменная для консеквента"""
    print(
        f"{fact.pred_name}'({var2}) = sup({{A'(x)/~\\({rule_to_str(rule, var1, var2)})|{var1}}}) = {fuzzy_set_to_str(fact.fuzzy_set)}\n"
    )


def rule_to_str(
    rule: Rule, antecedent_var: str = "x", consequent_var: str = "y"
) -> str:
    return str(
        f"{rule.antecedent_name}({antecedent_var}) ~> {rule.consequent_name}({consequent_var})"
    )


def print_relation(rule: Rule, console: Console | None = None) -> None:
    """Вывод матрицы значений пар <элемент антецедента и элемент консеквента>."""
    console = console or Console()
    xs = sorted(rule.antecedent_elements)
    ys = sorted(rule.consequent_elements)

    table = Table(
        show_lines=True,
    )
    table.add_column(f"{rule_to_str(rule)}", style="bold cyan")
    for y in ys:
        table.add_column(y, justify="right")

    for x in xs:
        table.add_row(x, *(f"{rule.relation[(x, y)]:.2f}" for y in ys))

    console.print(table)


def ask_continue() -> bool:
    """Функция для прерывания прямого логического вывода
    через запрос пользователю на продолжение"""
    try:
        cmd = input("Enter - продолжить, q - остановить: ").strip().lower()
    except EOFError:
        return True
    return cmd not in STOP_COMMANDS


console = Console()

custom_style = Style(
    [
        ("qmark", "fg:#00d7af bold"),  # Цвет вопросительного знака
        ("question", "bold"),  # Стиль текста вопроса
        ("answer", "fg:#5fd7ff"),  # Цвет ответа пользователя
        ("pointer", "fg:#00d7af bold"),  # Цвет указателя выбора
        ("highlighted", "fg:#00d7af bold"),  # Цвет выделенного пункта
        ("selected", "fg:#00d7af"),  # Цвет выбранного пункта
    ]
)


class App:
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb
        self.engine = FuzzyInferenceEngine(kb)

    def run(self) -> None:
        """Отображает главное меню и обрабатывает выбор пользователя."""

        choices = [
            "1 - Загрузка нового файла базы знаний",
            "2 - Вывод фактов базы знаний",
            "3 - Вывод правил базы знаний",
            "4 - Сохранение текущей базы знаний в файл",
            "5 - Прямой нечеткий логический вывод",
            "6 - Выход",
            "7 - Вопросы",
        ]

        while True:
            console.clear()

            title_panel = Panel(
                Align.center("[bold cyan]Меню программы[/bold cyan]"),
                border_style="bright_blue",
                padding=(1, 2),
            )
            console.print(title_panel)
            console.print()

            action = questionary.select(
                "Выберите действие:",
                choices=choices,
                style=custom_style,
                use_shortcuts=True,
            ).ask()

            if action is None:
                console.print("\n[yellow]Выход из программы.[/yellow]")
                sys.exit(0)

            if action.startswith("1"):
                console.print("[green]Вы выбрали:[/green] Ввод имени нового файла")
                new_file_name = questionary.text("Введите имя файла:").ask()
                self.kb = Parser.process_knowledge_base(new_file_name)
                self.engine = FuzzyInferenceEngine(self.kb)

            elif action.startswith("2"):
                console.print("[green]Вы выбрали:[/green] Вывод фактов базы знаний")
                for f in self.kb.facts:
                    print(fact_to_str(f))

            elif action.startswith("3"):
                console.print("[green]Вы выбрали:[/green] Вывод правил базы знаний")
                for r in self.kb.rules:
                    print(rule_to_str(r))
                    print_relation(r, console)

            elif action.startswith("4"):
                console.print(
                    "[green]Вы выбрали:[/green] Сохранение текущей базы знаний в файл"
                )
                new_file_name = questionary.text("Введите имя файла:").ask()
                save_knowledge_base(self.kb, new_file_name)
            elif action.startswith("5"):
                console.print("[green]Вы выбрали:[/green] Прямой нечеткий вывод")
                if not self.engine.direct_inference(
                    inferenced_fact_print, ask_continue
                ):
                    "\nВывод был прерван пользователем\n"
            elif action.startswith("6"):
                console.print(
                    "[bold yellow]Выход из программы. До свидания![/bold yellow]"
                )
                sys.exit(0)
            elif action.startswith("7"):
                question_kb: KnowledgeBase = Parser.process_knowledge_base(
                    "lab1/code/source/questions.txt"
                )

                console.print("Ответы на вопросы:")
                console.print("Вопрос 1:")
                rule = question_kb.rule_by_antecedent_consequent("A", "B")
                observ = question_kb.get_source_fact("C")
                console.print(fact_to_str(question_kb.get_source_fact("A")))
                console.print(fact_to_str(question_kb.get_source_fact("B")))
                result = FuzzyInferenceEngine.generalized_modus_ponens(rule, observ)
                inferenced_fact_print(result, rule)

                console.print("Вопрос 2:")
                rule = question_kb.rule_by_antecedent_consequent("A1", "B1")
                observ = question_kb.get_source_fact("C1")
                console.print(fact_to_str(question_kb.get_source_fact("A1")))
                console.print(fact_to_str(question_kb.get_source_fact("B1")))
                result = FuzzyInferenceEngine.generalized_modus_ponens(rule, observ)
                inferenced_fact_print(result, rule)

                console.print("Вопрос 3:")
                rule = question_kb.rule_by_antecedent_consequent("A2", "B2")
                observ = question_kb.get_source_fact("C2")
                console.print(fact_to_str(question_kb.get_source_fact("A2")))
                console.print(fact_to_str(question_kb.get_source_fact("B2")))
                result = FuzzyInferenceEngine.generalized_modus_ponens(rule, observ)
                inferenced_fact_print(result, rule)

                console.print("Вопрос 4:")
                rule = question_kb.rule_by_antecedent_consequent("A3", "B3")
                observ = question_kb.get_source_fact("C3")
                console.print(fact_to_str(question_kb.get_source_fact("A3")))
                console.print(fact_to_str(question_kb.get_source_fact("B3")))
                result = FuzzyInferenceEngine.generalized_modus_ponens(rule, observ)
                inferenced_fact_print(result, rule)

                console.print("Вопрос 5:")
                rule = question_kb.rule_by_antecedent_consequent("A4", "B4")
                observ = question_kb.get_source_fact("C4")
                console.print(fact_to_str(question_kb.get_source_fact("A4")))
                console.print(fact_to_str(question_kb.get_source_fact("B4")))
                result = FuzzyInferenceEngine.generalized_modus_ponens(rule, observ)
                inferenced_fact_print(result, rule)

                console.print("Вопрос 6:")
                rule = question_kb.rule_by_antecedent_consequent("A5", "B5")
                observ = question_kb.get_source_fact("C5")
                console.print(fact_to_str(question_kb.get_source_fact("A5")))
                console.print(fact_to_str(question_kb.get_source_fact("B5")))
                result = FuzzyInferenceEngine.generalized_modus_ponens(rule, observ)
                inferenced_fact_print(result, rule)

            questionary.press_any_key_to_continue(
                "Нажмите любую клавишу для продолжения..."
            ).ask()


if __name__ == "__main__":
    kb = KnowledgeBase()
    app = App(kb)
    try:
        app.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Программа прервана пользователем.[/yellow]")
        sys.exit(0)
