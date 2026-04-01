# core.py
from memory import get_history_text, add_message, get_memory, save_memory, load_memory
from state import user_input, build_prompt, history
from main import DEBUG, llm, void_context, get_void_response
from errors import GenerationError

memory = get_memory()

class Void:
    def __init__(self):
        self.mood = 0.0
        self.last_response = ""

    def think(self, input_str) -> str:
        self.mood += 0.1
        response = f"Я думаю о '{input_str}', настроение {self.mood}"
        self.last_response = response
        return response
    
def process(input_str: str) -> str:
    global Void
    return Void.think(input_str)

void = Void()


def init():
    load_memory()

def chat_step(user_text):
    global history
    full_prompt = build_prompt(user_text, history)
    response = get_void_response(llm, full_prompt)
    history.append({"role": "user", "text": user_text})
    history.append({"role": "assistant", "text": response})
    history = history[-10:]
    return response

def ask_void(user_input):
    try:
        add_message("Ты", user_input)
        memory = get_history_text()
        full_prompt = f"{build_prompt(user_input, history)}"
        if DEBUG:
            print(full_prompt)
        response = get_void_response(llm, full_prompt)
        add_message("Void", response)
        save_memory()
        return response
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"[Void error] {e}"