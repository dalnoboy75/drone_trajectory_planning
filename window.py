import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QFileDialog, QMessageBox)
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtCore import Qt

class CoordinateInputApp(QWidget):
    def __init__(self):
        super().__init__()
        self.points = []
        self.points_window = None  # Инициализация points_window как None
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
            x = float(self.input_x.text())
            y = float(self.input_y.text())
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
                        # Разделяем строку по пробелам и конвертируем в float
                        x, y = map(float, line.strip().split())
                        self.points.append((x, y))
                    except ValueError:
                        QMessageBox.warning(self, 'Ошибка', 'Неправильный формат в строке: ' + line.strip())

    def show_points(self):
        if self.points_window is not None:  # Если окно уже существует, закрываем его
            self.points_window.close()
        self.points_window = PointsWindow(self.points)  # Создаем новое окно
        self.points_window.show()

class PointsWindow(QWidget):
    def __init__(self, points):
        super().__init__()
        self.points = points
        self.setWindowTitle('Точки')
        self.setGeometry(100, 100, 800, 800)  # Увеличиваем размер окна

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.blue)
        painter.setPen(pen)

        # Рисуем оси
        painter.drawLine(50, 400, 750, 400)  # Ось X
        painter.drawLine(400, 50, 400, 750)  # Ось Y

        # Подписи осей
        painter.setFont(QFont('Arial', 10))
        painter.drawText(760, 405, 'X')
        painter.drawText(395, 40, 'Y')

        # Рисуем сетку
        pen.setColor(Qt.lightGray)
        pen.setWidth(1)  # Устанавливаем ширину линий сетки
        painter.setPen(pen)
        for i in range(50, 800, 50):
            painter.drawLine(i, 50, i, 750)  # Вертикальные линии
            painter.drawLine(50, i, 750, i)  # Горизонтальные линии

        # Рисуем оси на сетке
        pen.setColor(Qt.black)
        pen.setWidth(2)  # Устанавливаем ширину линий осей
        painter.setPen(pen)
        painter.drawLine(50, 400, 750, 400)  # Ось X
        painter.drawLine(400, 50, 400, 750)  # Ось Y

        # Рисуем стрелочки на осях
        self.draw_arrow(painter, 750, 400, -10, -5)  # Стрелка на оси X
        self.draw_arrow(painter, 400, 50, 5, 10)  # Стрелка на оси Y

        # Рисуем точки
        pen.setColor(Qt.red)
        pen.setWidth(4)  # Устанавливаем ширину точек
        painter.setPen(pen)
        for x, y in self.points:
            # Центрируем координаты для отображения и увеличиваем масштаб
            painter.drawPoint(int(x * 20 + 400), int(400 - y * 20))  # Увеличиваем масштаб

    def draw_arrow(self, painter, x, y, arrow_size_x, arrow_size_y):
        """Рисует стрелку на координатах (x, y)"""
        # Рисуем основную линию стрелки
        painter.drawLine(x, y, x + arrow_size_x, y + arrow_size_y)  # Основная линия стрелки
        painter.drawLine(x, y, x + arrow_size_x, y - arrow_size_y)  # Вторая линия стрелки
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoordinateInputApp()
    ex.resize(300, 200)
    ex.show()
    sys.exit(app.exec_())
