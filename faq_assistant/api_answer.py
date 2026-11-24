import os

API_KEY = os.environ.get("ANTHROPIC_API_KEY")

PROMPT_TEMPLATE = """You are helping a teacher find a policy answer.
Only use the passage below. Do not add any information that is not in it.
If the passage does not actually answer the question, say so instead of guessing.

Passage:
{passage}

Question: {question}

Answer in one or two short sentences, using only the passage above."""


def get_api_answer(question, passage):
    # no key configured, or nothing was found to begin with: just show the raw passage
    if not API_KEY:
        return passage

    import anthropic

    client = anthropic.Anthropic(api_key=API_KEY)
    prompt = PROMPT_TEMPLATE.format(passage=passage, question=question)

    try:
        message = client.messages.create(
            model="claude-haiku-5-5",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text.strip()
    except Exception:
        # if the API call fails for any reason, fall back to the real passage
        # instead of showing an error or an unsupported answer
        return passage
