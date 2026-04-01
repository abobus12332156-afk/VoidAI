# styles.py
APP_STYLE = """
QWidget {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgb(20, 10, 40),
        stop:1 rgb(30, 10, 60));
}

QTextEdit, QLineEdit {
    background-color: rgba(10, 10, 20, 200);
    color: #dddddd;
    border-radius: 8px;
}

QPushButton {
    background-color: rgba(40, 40, 60, 220);
    color: white;
    border-radius: 8px;
    padding: 6px;
}

QPushButton:hover {
    background-color: rgba(70, 70, 130, 240);
}
"""
