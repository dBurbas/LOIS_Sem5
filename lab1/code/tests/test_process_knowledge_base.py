import pytest

from parser.parser import Parser, ParseError


class TestProcessKnowledgeBase:
    def test_simple(self, tmp_path):
        f = tmp_path / "kb.txt"
        f.write_text("facts\nA(x) = {<a, 0.5>}\nB(x) = {<b, 0.7>}\nrules\nA(x) ~> B(y)\n")
        kb = Parser.process_knowledge_base(str(f))
        assert len(kb.facts) == 2
        assert len(kb.rules) == 1

    def test_no_facts_raises(self, tmp_path):
        f = tmp_path / "kb.txt"
        f.write_text("rules\n")
        with pytest.raises(ParseError):
            Parser.process_knowledge_base(str(f))

    def test_duplicate_fact_raises(self, tmp_path):
        f = tmp_path / "kb.txt"
        f.write_text("facts\nA(x) = {<a, 0.5>}\nA(x) = {<b, 0.7>}\n")
        with pytest.raises(ParseError):
            Parser.process_knowledge_base(str(f))

    def test_rule_referencing_unknown_fact_raises(self, tmp_path):
        f = tmp_path / "kb.txt"
        f.write_text("facts\nA(x) = {<a, 0.5>}\nrules\nA(x) ~> B(y)\n")
        with pytest.raises(ParseError):
            Parser.process_knowledge_base(str(f))

    def test_duplicate_rule_raises(self, tmp_path):
        f = tmp_path / "kb.txt"
        f.write_text(
            "facts\nA(x) = {<a, 0.5>}\nB(x) = {<b, 0.7>}\n"
            "rules\nA(x) ~> B(y)\nA(x) ~> B(y)\n"
        )
        with pytest.raises(ParseError):
            Parser.process_knowledge_base(str(f))

    def test_comments_ignored(self, tmp_path):
        f = tmp_path / "kb.txt"
        f.write_text(
            "# comment\n"
            "facts\n"
            "// another\n"
            "A(x) = {<a, 0.5>}\n"
        )
        kb = Parser.process_knowledge_base(str(f))
        assert len(kb.facts) == 1

    def test_blank_lines_ignored(self, tmp_path):
        f = tmp_path / "kb.txt"
        f.write_text("facts\n\nA(x) = {<a, 0.5>}\n\n")
        kb = Parser.process_knowledge_base(str(f))
        assert len(kb.facts) == 1

    def test_lines_before_header_ignored(self, tmp_path):
        f = tmp_path / "kb.txt"
        f.write_text("garbage\nA(x) = {<a, 0.5>}\nfacts\nB(x) = {<b, 0.7>}\n")
        kb = Parser.process_knowledge_base(str(f))
        assert len(kb.facts) == 1
        assert kb.facts[0].pred_name == "B"

    def test_lines_without_marker_ignored(self, tmp_path):
        f = tmp_path / "kb.txt"
        f.write_text("facts\nsome random line\nA(x) = {<a, 0.5>}\n")
        kb = Parser.process_knowledge_base(str(f))
        assert len(kb.facts) == 1

    def test_bom_handling(self, tmp_path):
        f = tmp_path / "kb.txt"
        f.write_bytes(b"\xef\xbb\xbffacts\nA(x) = {<a, 0.5>}\n")
        kb = Parser.process_knowledge_base(str(f))
        assert len(kb.facts) == 1
