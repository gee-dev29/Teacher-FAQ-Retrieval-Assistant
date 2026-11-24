from flask import Flask, request, jsonify

from faq_assistant.index_builder import build_index
from faq_assistant.search import search
from faq_assistant.unresolved_log import log_unresolved_question
from faq_assistant.api_answer import get_api_answer

app = Flask(__name__)
document_index = build_index()


@app.route("/search")
def search_endpoint():
    question = request.args.get("q", "").strip()

    if not question:
        return jsonify({"error": "please provide a question with ?q="}), 400

    result = search(question, document_index)

    if result is None:
        log_unresolved_question(question)
        return jsonify({
            "found": False,
            "answer": "Sorry, no policy document answers this question yet.",
            "source": None,
        })

    answer = get_api_answer(question, result["text"])

    return jsonify({
        "found": True,
        "answer": answer,
        "source": result["source"],
    })


if __name__ == "__main__":
    app.run(debug=True)
