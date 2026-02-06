from langdetect import detect
from googletrans import Translator

translator = Translator()

def handle_language(question):
    try:
        lang = detect(question)
        if lang == "ta":
            q_en = translator.translate(question, dest="en").text
            return q_en, "ta"
    except Exception:
        # Fallback to assuming English or returning original if detection fails
        pass
    return question, "en"

def translate_back(answer, lang):
    try:
        if lang == "ta":
            return translator.translate(answer, dest="ta").text
    except Exception:
        pass
    return answer
