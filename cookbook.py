"""Deterministic tools used by the Gemini recipe assistant."""
import json
import re
from recipes import RECIPES

SUBSTITUTIONS = {
    "egg": "For binding in pancakes, try 1 tbsp ground flaxseed mixed with 3 tbsp water per egg; texture may differ.",
    "milk": "Use unsweetened oat or soy milk in equal quantity.",
    "butter": "Use olive oil in roughly equal quantity for savoury dishes.",
    "parsley": "Use fresh coriander or basil; flavour will change.",
    "soy sauce": "Use tamari for a similar flavour (check gluten-free labelling if needed).",
    "lemon": "Try lime in equal quantity; taste and adjust.",
    "chickpeas": "Try cooked white beans in equal volume; texture will differ.",
    "eggplant": "Try zucchini, though cooking time may differ."
}

def search_recipes(query: str) -> str:
    """Search recipe names, tags and ingredients; return matching structured recipes."""
    terms = set(re.findall(r"[a-z0-9]+", query.lower()))
    if not terms:
        return "Please provide a search term."
    scored = []
    for key, recipe in RECIPES.items():
        title = recipe["title"].lower()
        tags = " ".join(recipe["tags"]).lower()
        ingredients = " ".join(recipe["ingredients"]).lower()
        score = sum(4 if t in title else 2 if t in tags else 1 if t in ingredients else 0 for t in terms)
        if score:
            scored.append((score, key, recipe))
    scored.sort(key=lambda item: (-item[0], item[1]))
    if not scored:
        return "No matching recipes in this cookbook."
    return json.dumps([{"id": key, **recipe} for _, key, recipe in scored[:3]], indent=2)

def substitute_ingredient(ingredient: str) -> str:
    """Look up a tested-in-context suggestion, not a guaranteed equivalent."""
    key = ingredient.strip().lower()
    return SUBSTITUTIONS.get(key, f"No documented substitution for '{ingredient}' in this cookbook.")
