import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QFileDialog, QMessageBox)
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtCore import Qt

class CoordinateInputApp(QWidget):
    def __init__(self):
        super().__init__()
        self.points = []
        self.points_window = None
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

        self.button_show_points = QPushButton('Показать точки', self)
        self.button_show_points.clicked.connect(self.show_points)
        layout.addWidget(self.button_show_points)

        self.setLayout(layout)

    def add_point(self):
        try:
            x = float(self.input_x.text().replace(',', '.'))
            y = float(self.input_y.text().replace(',', '.'))
            self.points.append((x, y))
            QMessageBox.information(self, 'Успех', f'Точка добавлена: X = {x}, Y = {y}')
            self.input_x.clear()
            self.input_y.clear()
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

    def show_points(self):
        if self.points_window is not None:
            self.points_window.close()
        self.points_window = PointsWindow(self.points)
        self.points_window.show()

class PointsWindow(QWidget):
    def __init__(self, points):
        super().__init__()
        self.points = points
        self.setWindowTitle('Точки')
        self.setGeometry(100, 100, 800, 800)

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.blue)
        painter.setPen(pen)

        # Оси
        painter.drawLine(50, 400, 750, 400)
        painter.drawLine(400, 50, 400, 750)

        # Подписи осей
        painter.setFont(QFont('Arial', 10))
        painter.drawText(760, 405, 'X')
        painter.drawText(395, 40, 'Y')

        # Координатная плоскость
        pen.setColor(Qt.lightGray)
        pen.setWidth(1)
        painter.setPen(pen)
        for i in range(50, 800, 50):
            painter.drawLine(i, 50, i, 750)
            painter.drawLine(50, i, 750, i)

        # Оси
        pen.setColor(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(50, 400, 750, 400)  # Ось X
        painter.drawLine(400, 50, 400, 750)  # Ось Y

        # Точки
        pen.setColor(Qt.red)
        pen.setWidth(4)
        painter.setPen(pen)
        for x, y in self.points:
            painter.drawPoint(int(x * 20 + 400), int(400 - y * 20)) #для масштаба

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoordinateInputApp()
    ex.resize(300, 200)
    ex.show()
    sys.exit(app.exec_())