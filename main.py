# main.py
from llama_cpp import Llama
from web_search import search_web
from state import void_context, user_input
from errors import ModelLoadError, MemoryErrorVoid

# === ГЛОБАЛЬНОЕ СОСТОЯНИЕ VOID ===
dialog_memory = []

DEBUG = True
def log(*args):
    if DEBUG:
        print(*args)

# путь к модели
model_path = "models/gpt-oss-20b-mxfp4.gguf"

# оздаём объект модели
llm = Llama(model_path=model_path)

# функция инициализации модели
def init_void_model(model_path):
    return Llama(model_path=model_path)
# функция общения с Void
def get_void_response(llm, user_input):
    if llm is None:
        raise ModelLoadError("Модель не загружена")
    response = llm(user_input,
                    max_tokens=200,
                    temperature=0.7,
                    top_p=0.9,
                    stop=["\n"]
                    )
    if "NEED_WEB_SEARCH:" in response:
        query = response.split("NEED_WEB_SEARCH:")[1].strip()

        print(f"[VOID] Ищу в интенете: {query}")

        web_data = search_web(query)

        second_prompt = f"""
    Контекст из интернета: {web_data}
    Ответь пользователю."""
        response = llm(second_prompt)
    if isinstance(response, dict):
        # если ключ 'choices' есть, берём оттуда
        if 'choices' in response and len(response['choices']) > 0:
            return response['choices'][0].get('text', '[Пустой ответ]')
        # иначе проверяем, есть ли 'text' на верхнем уровне
        elif 'text' in response:
            return response['text']

        # если ничего не нашли
        return '[Нет ответа]'
