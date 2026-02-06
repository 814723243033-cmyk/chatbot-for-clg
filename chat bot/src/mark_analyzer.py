def detect_marks(question):
    q = question.lower()
    if "2" in q:
        return 2
    if "5" in q:
        return 5
    if "10" in q:
        return 10
    if "13" in q or "15" in q or "discuss" in q:
        return 15
    return 10
