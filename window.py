import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

class CoordinateInputApp(QWidget):
    def __init__(self):
        super().__init__()
        self.points = []  # Список для хранения точек
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ввод координат')
        layout = QVBoxLayout()

        self.label_x = QLabel('Введите X:')
        self.input_x = QLineEdit(self)
        layout.addWidget(self.label_x)
        layout.addWidget(self.input_x)

        self.label_y = QLabel('Введите Y:')
        self.input_y = QLineEdit(self)
        layout.addWidget(self.label_y)
        layout.addWidget(self.input_y)

        self.button_check = QPushButton('Добавить точку', self)
        self.button_check.clicked.connect(self.add_point)
        layout.addWidget(self.button_check)

        self.button_file = QPushButton('Выбрать файл', self)
        self.button_file.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.button_file)

        self.setLayout(layout)

    def add_point(self):
        try:
            x = float(self.input_x.text())
            y = float(self.input_y.text())
            self.points.append((x, y))
            QMessageBox.information(self, 'Успех', f'Точка добавлена: X = {x}, Y = {y}')
            self.input_x.clear()
            self.input_y.clear()
            self.show_points()
        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Введите корректные числовые значения для координат.')

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл с координатами", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                data = file.readlines()
                for line in data:
                    try:
                        x, y = map(float, line.strip().split())
                        self.points.append((x, y))
                    except ValueError:
                        QMessageBox.warning(self, 'Ошибка', 'Неправильный формат в строке: ' + line.strip())
            self.show_points()

    def show_points(self):
        self.points_window = PointsWindow(self.points)
        self.points_window.show()

class PointsWindow(QWidget):
    def __init__(self, points):
        super().__init__()
        self.points = points
        self.setWindowTitle('Точки')
        self.setGeometry(100, 100, 400, 400)

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.blue)
        painter.setPen(pen)

        for x, y in self.points:
            painter.drawPoint(x + 200, 400 - y)  # Центрируем координаты для отображения

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoordinateInputApp()
    ex.resize(300, 200)
    ex.show()
    sys.exit(app.exec_())
