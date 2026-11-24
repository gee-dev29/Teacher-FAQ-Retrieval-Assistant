import re

MINIMUM_MATCHING_WORDS = 2

# common words that do not help us tell one question from another
STOP_WORDS = {
    "a", "an", "the", "is", "are", "do", "does", "can", "i", "my", "to",
    "for", "of", "in", "on", "what", "when", "how", "who", "if", "and",
}


def normalize_word(word):
    # crude stemming so "phones" matches "phone" and "used" matches "use"
    if word.endswith("ies") and len(word) > 4:
        word = word[:-3] + "y"
    elif word.endswith("ing") and len(word) > 5:
        word = word[:-3]
    elif word.endswith("ed") and len(word) > 3:
        word = word[:-2]
    elif word.endswith("es") and len(word) > 3:
        word = word[:-2]
    elif word.endswith("s") and len(word) > 3:
        word = word[:-1]

    if word.endswith("e") and len(word) > 2:
        word = word[:-1]

    return word


def get_keywords(text):
    words = re.findall(r"[a-z]+", text.lower())
    words = [w for w in words if w not in STOP_WORDS]
    return [normalize_word(w) for w in words]


def search(question, index):
    question_words = set(get_keywords(question))

    best_match = None
    best_score = 0

    for item in index:
        item_words = set(get_keywords(item["text"]))
        score = len(question_words & item_words)
        if score > best_score:
            best_score = score
            best_match = item

    if best_match is not None and best_score >= MINIMUM_MATCHING_WORDS:
        return {"text": best_match["text"], "source": best_match["source"]}

    return None
