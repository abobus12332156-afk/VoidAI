# memory.py
import json
from config import MAX_MEMORY_MESSAGES, MEMORY_FILE

dialog_memory = []

MAX_MEMORY_TOKENS = 300

MAX_MEMORY_MESSAGES = 3

class memory:
    pass

def get_memory():
    with open("dialog_memory.json", "r", encoding="utf-8") as f:
        memory = json.load(f)
    return memory[-MAX_MEMORY_TOKENS:]

def add_message(role, text):
    dialog_memory.append({"role": role, "text": text})
    # лимит
    if len(dialog_memory) > MAX_MEMORY_MESSAGES:
        dialog_memory.pop(0)

def get_history_text():
    seen = set()
    cleaned = []
    for m in dialog_memory:
        line = f"{m['role']}: {m['text']}".strip()
        if line and line not in seen:
            cleaned.append(line)
            seen.add(line)
    return "\n".join(cleaned)

def save_memory():
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(dialog_memory, f, ensure_ascii=False, indent=2)

def load_memory():
    global dialog_memory

    try:
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            dialog_memory = json.load(f)
    except FileNotFoundError:
        dialog_memory = []