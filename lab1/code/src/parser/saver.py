from domain.fuzzy_set import FuzzySet
from domain.knowledge_base import KnowledgeBase


def _format_degree(value: float) -> str:
    """0.5 -> '0.5', 1 -> '1.0'; без экспоненты, чтобы проходить _DEGREE парсера."""
    text = f"{value:.10f}".rstrip("0")
    return text + "0" if text.endswith(".") else text


def _fuzzy_set_to_file(fuzzy_set: FuzzySet) -> str:
    pairs = sorted(fuzzy_set.membership_pairs)
    return "{" + ", ".join(f"<{el}, {_format_degree(d)}>" for el, d in pairs) + "}"


def save_knowledge_base(kb: KnowledgeBase, filename: str) -> None:
    lines: list[str] = ["facts"]

    seen: set[str] = set()
    for fact in kb.facts:
        print(fact.pred_name)
        if fact.pred_name in seen:
            continue
        seen.add(fact.pred_name)
        source = kb.get_source_fact(fact.pred_name)
        lines.append(f"{source.pred_name}(x) = {_fuzzy_set_to_file(source.fuzzy_set)}")

    if kb.rules:
        lines += ["", "rules"]
        for rule in kb.rules:
            lines.append(f"{rule.antecedent_name}(x) ~> {rule.consequent_name}(y)")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
