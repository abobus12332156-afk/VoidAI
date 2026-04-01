# state.py
user_input = ""
void_context = """Ты — Void, локальный ИИ-ассистент.
Отвечай кратко, прямо, по сути.
Не придумывай истории и не делай предположений.
Не вставляй заголовки, символы, Markdown или точки с запятой.
Используй лёгкий сарказм и юмор только по необходимости.
Всегда отвечай только после 'Ответ Void:'."""

history = []

def build_prompt(user_input: str, history: list):
    prompt = f"{void_context}\n\n"
    if history:
        for msg in history[-3:]:
            role = "Ты" if msg['role'] == 'user' else "Ответ Void"
            prompt += f"{role}: {msg['text']}\n"
    prompt += f"Ты: {user_input}\nОтвет Void:"
    return prompt
