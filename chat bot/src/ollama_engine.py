import subprocess

def generate_answer(context, question, marks):
    structure = {
        2: "Answer briefly in 2–3 lines.",
        5: "Answer with key points.",
        10: "Give a detailed explanation with examples.",
        15: """Give an exam-oriented answer with:
- Introduction
- Explanation
- Diagram description
- Advantages
- Applications"""
    }

    prompt = f"""
You are a college professor.

Syllabus Context:
{context}

Question:
{question}

Instruction:
{structure.get(marks, "Give a clear explanation.")}
"""

    try:
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt,
            text=True,
            capture_output=True,
            encoding='utf-8',
            check=True
        )
        return result.stdout.strip()
    except FileNotFoundError:
        return "Error: Ollama is not installed or not in PATH."
    except subprocess.CalledProcessError as e:
        return f"Error running Ollama: {e.stderr}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


