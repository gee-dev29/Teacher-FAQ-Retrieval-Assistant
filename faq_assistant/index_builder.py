import os

DOCUMENTS_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "documents")


def build_index(folder=DOCUMENTS_FOLDER):
    # each item in the index is one paragraph and the file it came from
    index = []
    for file_name in sorted(os.listdir(folder)):
        if not file_name.endswith(".txt"):
            continue
        file_path = os.path.join(folder, file_name)
        with open(file_path, "r") as f:
            text = f.read()
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        for paragraph in paragraphs:
            index.append({"text": paragraph, "source": file_name})
    return index
