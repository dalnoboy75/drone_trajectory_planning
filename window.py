import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("Построение траектории БПЛА")

        layout = QVBoxLayout()

        self.label_x = QLabel("Окно для ввода координаты Х", self)
        layout.addWidget(self.label_x)

        self.entry_x = QLineEdit(self)
        layout.addWidget(self.entry_x)

        self.label_y = QLabel("Окно для ввода координаты У", self)
        layout.addWidget(self.label_y)

        self.entry_y = QLineEdit(self)
        layout.addWidget(self.entry_y)

        self.button = QPushButton("Ввести", self)
        self.button.clicked.connect(self.validate_input)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def validate_input(self):
        try:
            x = float(self.entry_x.text())
            y = float(self.entry_y.text())
            QMessageBox.information(self, "Ввод успешен", f"Координаты: X = {x}, Y = {y}")
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Введите корректные числовые значения для координат.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
