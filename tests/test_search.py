import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from faq_assistant.index_builder import build_index
from faq_assistant.search import search
from faq_assistant.unresolved_log import log_unresolved_question

index = build_index()


def test_known_question_returns_correct_source():
    result = search("how many days of sick leave can a teacher take", index)
    assert result is not None
    assert result["source"] == "leave_policy.txt"


def test_another_known_question_returns_correct_source():
    result = search("can a student use their phone in class", index)
    assert result is not None
    assert result["source"] == "classroom_conduct.txt"


def test_unknown_question_returns_none():
    result = search("what is the capital of france", index)
    assert result is None


def test_unresolved_question_gets_logged():
    log_file = os.path.join(os.path.dirname(__file__), "test_unresolved.log")
    if os.path.exists(log_file):
        os.remove(log_file)

    log_unresolved_question("what is the capital of france", log_file=log_file)

    with open(log_file) as f:
        lines = f.readlines()

    assert len(lines) == 1
    assert "what is the capital of france" in lines[0]

    os.remove(log_file)
