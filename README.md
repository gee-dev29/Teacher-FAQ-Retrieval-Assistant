# Teacher FAQ Retrieval Assistant

Teachers spend a lot of time looking through policy documents to answer simple
questions like "how many sick days do I get" or "what happens if a student
hands in work late". This project is a small assistant that searches a set of
policy documents and answers with the exact passage it found, plus which file
it came from. If nothing matches, it says so honestly instead of guessing,
and writes the question to a log so someone can add a document for it later.

## How it works

1. `faq_assistant/index_builder.py` reads every `.txt` file in `documents/`
   and splits it into paragraphs. This is the curated document index.
2. `faq_assistant/search.py` takes a question, pulls out the keywords, and
   compares them against every paragraph in the index. It returns the
   paragraph with the most matching keywords, but only if the match is good
   enough. If nothing is good enough, it returns `None`.
3. `faq_assistant/unresolved_log.py` writes the question to
   `unresolved_questions.log` whenever step 2 found nothing.
4. `faq_assistant/api_answer.py` is optional. If an `ANTHROPIC_API_KEY`
   environment variable is set, it asks an LLM to turn the matched passage
   into a short natural sentence. The prompt tells the model to only use the
   passage it was given and to say so if the passage doesn't really answer
   the question — it is never allowed to answer without a passage, because
   this function is only ever called after step 2 already found one. With no
   key set, it just returns the raw passage, so the project works and can be
   tested with no internet connection and no API key at all.
5. `faq_assistant/app.py` is a small Flask app with one endpoint,
   `GET /search?q=...`, that runs steps 2-4 and returns the answer as JSON.

## Why rule-based first

The main challenge in this project is making sure the assistant returns real
sources instead of making things up. Keyword matching against real documents
can't invent text that isn't there — every answer either comes straight from
a document or the assistant admits it doesn't know. The API layer sits on
top of that and is only used to make the wording more natural, not to
replace the retrieval step.

## Running it

Install the requirements:

```
pip install -r requirements.txt
```

Run the demo (five sample questions, including one with no answer):

```
python demo.py
```

Start the search endpoint:

```
python -m faq_assistant.app
```

Then in another terminal:

```
curl "http://127.0.0.1:5000/search?q=how+many+days+of+sick+leave+can+a+teacher+take"
curl "http://127.0.0.1:5000/search?q=what+is+the+capital+of+france"
```

The second one comes back with `"found": false` and gets added to
`unresolved_questions.log`.

To turn on the optional API wording layer, set an API key first:

```
export ANTHROPIC_API_KEY=your-key-here
python -m faq_assistant.app
```

## Running the tests

```
pytest tests/
```

The tests check that two sample questions match their correct source
document, that a question with no matching document comes back as
not-found, and that an unresolved question actually gets written to the log.

## Sample data

The files in `documents/` are made-up sample policies (grading, attendance,
staff leave, grievances, classroom conduct, assessment deadlines) written for
this project, not a real school's policy documents.

## Known limits

- Matching is based on shared keywords, not real understanding of meaning.
  A question that uses very different words from the document (for example
  "when do I get paid extra" instead of "overtime pay") may not match even
  if a document covers it.
- The index is rebuilt from the `documents/` folder every time the app
  starts, so there's no need to re-run anything after editing a document.
- The optional API layer depends on an external service being available.
  If the call fails for any reason, it quietly falls back to showing the
  raw passage instead of breaking the response.
