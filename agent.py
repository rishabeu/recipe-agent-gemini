"""Gemini tool-calling recipe assistant using the supported google-genai SDK."""
import os
import time
from google import genai
from google.genai import types
from cookbook import search_recipes, substitute_ingredient

SYSTEM = (
    "You are a helpful recipe assistant. Use search_recipes for questions about "
    "the cookbook and substitute_ingredient for substitutions. Only claim a recipe, "
    "ingredient, timing or substitution is documented if the tools return it. "
    "If it is absent, say so. Do not invent cookbook entries."
)
TOOLS = {
    "search_recipes": search_recipes,
    "substitute_ingredient": substitute_ingredient,
}

def ask(question: str, model: str | None = None, max_steps: int = 6) -> str:
    if not (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")):
        raise RuntimeError("Set GEMINI_API_KEY (or GOOGLE_API_KEY) before running.")
    client = genai.Client()
    declarations = [
        types.FunctionDeclaration(
            name="search_recipes",
            description="Search the local cookbook by dish, ingredient or tag.",
            parameters={"type": "OBJECT", "properties": {"query": {"type": "STRING"}}, "required": ["query"]},
        ),
        types.FunctionDeclaration(
            name="substitute_ingredient",
            description="Find a documented substitute for an ingredient.",
            parameters={"type": "OBJECT", "properties": {"ingredient": {"type": "STRING"}}, "required": ["ingredient"]},
        ),
    ]
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM,
        tools=[types.Tool(function_declarations=declarations)],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )
    history = [types.Content(role="user", parts=[types.Part.from_text(text=question)])]
    for _ in range(max_steps):
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
                    contents=history,
                    config=config,
                )
                break
            except Exception as exc:
                if "429" not in str(exc) or attempt == 2:
                    raise
                time.sleep(2 ** attempt)
        if not response.candidates or not response.candidates[0].content:
            return "The model returned no response."
        content = response.candidates[0].content
        history.append(content)  # Preserve thought signatures and tool-call context.
        calls = [part.function_call for part in content.parts or [] if part.function_call]
        if not calls:
            return response.text or "No text response was generated."
        results = []
        for call in calls:
            fn = TOOLS.get(call.name)
            if fn is None:
                output = f"Unknown tool: {call.name}"
            else:
                try:
                    output = fn(**dict(call.args or {}))
                except (TypeError, ValueError) as exc:
                    output = f"Tool argument error: {exc}"
            results.append(types.Part.from_function_response(name=call.name, response={"result": output}))
        history.append(types.Content(role="tool", parts=results))
    return "Maximum tool-call steps reached without a final answer."

if __name__ == "__main__":
    print("Recipe assistant. Type 'exit' to quit.")
    while True:
        try:
            question = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if question.lower() in {"exit", "quit"}:
            break
        if question:
            print("\nAssistant:", ask(question))
