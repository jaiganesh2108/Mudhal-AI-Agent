import contextlib
import io
import os
import traceback

from google import genai


MODEL_NAME = "gemini-1.5-flash"
API_KEY = os.environ.get("GOOGLE_API_KEY")


if not API_KEY or API_KEY == "your-api-key":
    raise RuntimeError("Set GOOGLE_API_KEY to a real Gemini API key before running this script.")


client = genai.Client(api_key=API_KEY)
python_namespace = {"__name__": "__main__"}


def ask_gemini(prompt: str) -> str:
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    return response.text or ""


def debug_code(code: str) -> str:
    prompt = f"""
You are a senior Python engineer.

Analyze this code:
{code}

Return:
- Bugs
- Fixes
- Improved version
- Explanation
"""
    return ask_gemini(prompt)


def run_python(code: str) -> str:
    stdout_buffer = io.StringIO()

    try:
        with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stdout_buffer):
            exec(code, python_namespace, python_namespace)
    except Exception:
        captured_output = stdout_buffer.getvalue().strip()
        error_output = traceback.format_exc().strip()
        return "\n".join(part for part in [captured_output, error_output] if part)

    output = stdout_buffer.getvalue().strip()
    return output if output else "Code executed successfully."


def route_request(user_input: str) -> str:
    stripped_input = user_input.strip()
    lowered_input = stripped_input.lower()

    if lowered_input.startswith(("run:", "python:")):
        code = stripped_input.split(":", 1)[1].strip()
        return run_python(code)

    if lowered_input.startswith(("debug:", "fix:", "analyze:")):
        code = stripped_input.split(":", 1)[1].strip()
        return debug_code(code)

    prompt = (
        "You are a helpful Python coding assistant. "
        "Answer clearly and keep the response focused on the user's request.\n\n"
        f"User request:\n{user_input}"
    )
    return ask_gemini(prompt)


print("Gemini AI Code Agent")
print("Type 'exit' to quit.")
print("Use 'run:' to execute Python and 'debug:' to analyze code.\n")

while True:
    user_input = input("Enter your code or request:\n")

    if user_input.lower().strip() == "exit":
        break

    response = route_request(user_input)
    print("\nResponse:\n", response)