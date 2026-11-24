from faq_assistant.index_builder import build_index
from faq_assistant.search import search
from faq_assistant.unresolved_log import log_unresolved_question
from faq_assistant.api_answer import get_api_answer

sample_questions = [
    "how many days of sick leave can a teacher take",
    "can a student use their phone in class",
    "what happens if i hand in my assignment late",
    "how do i complain about another teacher",
    "what is the capital of france",
]


def run_demo():
    index = build_index()

    for question in sample_questions:
        print("Q:", question)
        result = search(question, index)

        if result is None:
            log_unresolved_question(question)
            print("A: Sorry, no policy document answers this question yet.")
            print("Source: none (logged as unresolved)")
        else:
            answer = get_api_answer(question, result["text"])
            print("A:", answer)
            print("Source:", result["source"])

        print()


if __name__ == "__main__":
    run_demo()
