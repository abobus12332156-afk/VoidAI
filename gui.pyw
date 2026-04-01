# gui.pyw
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PySide6.QtGui import QTextCursor
from PySide6.QtCore import QThread, Signal, QTimer
from config import APP_TITLE, WINDOW_SIZE, TYPING_SPEED_MS, BG_SPEED, BG_TIMER_MS
from core import init, ask_void
from state import user_input, void_context
from styles import APP_STYLE
from errors import VoidError

class VoidWorker(QThread):
    finished = Signal(str)

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt

    def run(self):
            from core import ask_void
            response = ask_void(self.prompt)
            self.finished.emit(response)

        
class VoidGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.resize(*WINDOW_SIZE)

        init()

        layout = QVBoxLayout(self)

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Спроси Void...")

        self.send_btn = QPushButton("Отправить")

        layout.addWidget(self.chat)
        layout.addWidget(self.input)
        layout.addWidget(self.send_btn)

        self.send_btn.clicked.connect(self.send_message)
        self.input.returnPressed.connect(self.send_message)

        # background animation
        self.bg_step = 0
        self.bg_timer = QTimer()
        self.bg_timer.timeout.connect(self.update_background)
        self.bg_timer.start(BG_TIMER_MS)

        # typing animation
        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.type_next_char)
        self.full_response = ""
        self.char_index = 0

    def send_message(self):
        text = self.input.text().strip()
        if not text:
            return

        self.chat.append(f"Ты: {text}")
        self.input.clear()

        self.chat.append("Void думает...(запрос отправлен)")

        self.worker = VoidWorker(text)
        self.worker.finished.connect(self.on_void_response)
        self.worker.start()

    def on_void_response(self, response):
        # удаляем "думает..."
        self.chat.setPlainText(self.chat.toPlainText().replace("Void думает...(запрос отправлен)\n", ""))

        self.full_response = f"Void: {response}"
        self.char_index = 0
        self.chat.append("")  # пустая строка для печати
        self.typing_timer.start(TYPING_SPEED_MS)

    def type_next_char(self):
        if self.char_index >= len(self.full_response):
            self.typing_timer.stop()
            return

        cursor = self.chat.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(self.full_response[self.char_index])
        self.char_index += 1

    def update_background(self):
        import math

        self.bg_step += BG_SPEED

        r1 = int(20 + 10 * math.sin(self.bg_step))
        g1 = int(10 + 5 * math.sin(self.bg_step + 2))
        b1 = int(40 + 20 * math.sin(self.bg_step + 4))
        r2 = int(30 + 10 * math.sin(self.bg_step + 1))
        g2 = int(10 + 5 * math.sin(self.bg_step + 3))
        b2 = int(60 + 20 * math.sin(self.bg_step + 5))
    # ТОЛЬКО фон, без кнопок/полей
        self.setStyleSheet(f"""
        QWidget {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 rgb({r1}, {g1}, {b1}),
                stop:1 rgb({r2}, {g2}, {b2}));
        }}
    """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoidGUI()
    window.show()
    sys.exit(app.exec())
