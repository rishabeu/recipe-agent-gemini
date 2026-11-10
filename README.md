# Recipe Agent with Gemini

A Python recipe assistant powered by Gemini, with a structured cookbook, ingredient substitutions and an interactive CLI.

## Features
- Includes **four structured recipes**: lemon herb pasta, chickpea curry, vegetable fried rice and banana oat pancakes.
- Uses the **google-genai** SDK for Gemini integration.
- Supports recipe search, ingredient substitution and multi-step tool calling.
- Includes unit tests, configuration examples and an interactive CLI.

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
