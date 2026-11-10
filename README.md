# Recipe Agent with Gemini

Adapted from the supplied `recipe_agent_gemini.ipynb` Gist into a small, maintainable Python project.

## What's changed
- Replaced the original concatenated recipe strings with **four new structured recipes**: lemon herb pasta, chickpea curry, vegetable fried rice and banana oat pancakes.
- Replaced the mixed legacy `google-generativeai` / `google-genai` setup with **google-genai only**.
- Corrected tool naming and dispatch, added an **ingredient substitution tool**, and kept the model's tool-call content intact across turns.
- Added cookbook unit tests, configuration examples and an interactive CLI.

## Setup
Python 3.10+ is recommended.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

Create a Gemini API key in [Google AI Studio](https://aistudio.google.com/apikey). Set it in your terminal (never commit it):

```bash
export GEMINI_API_KEY="your-key-here"
python agent.py
```

On PowerShell: `$env:GEMINI_API_KEY="your-key-here"`.

You can override the model with `GEMINI_MODEL`; the default is `gemini-2.5-flash`. Model access and quota depend on your Google account.

## Tests
```bash
python -m unittest discover -v
```

Tests run without a Gemini API key. The end-to-end model call requires a key and network access.

## Edit recipes
Modify `RECIPES` in `recipes.py`. Each recipe needs a title, servings, time_minutes, ingredients, steps and tags. Update `SUBSTITUTIONS` in `cookbook.py` to extend ingredient alternatives.

## Original source
[Recipe agent Gist](https://gist.github.com/ca101ca288b3f594cfb865d4bdb5279f). This project is a refactor, not an unchanged GitHub fork. Verify any upstream license before redistributing upstream code.
