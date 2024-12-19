import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
    QAction, QFileDialog, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from pyqtgraph import PlotWidget, mkPen
from matrix_reading import Task
from Alg_L_Classes import algorithm_Lit
import numpy as np
import csv
import json
import os
import classes


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mainwindow.ui', self)
        self.init_ui()
        self.start_point = None
        self.end_point = None

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        self.setup_plot()
        self.setup_table_widgets()
        self.setup_buttons()
        self.setup_menu()
        self.setup_connections()

    def setup_plot(self):
        """Настройка графика."""
        self.plot = self.findChild(QWidget, 'plot')
        self.plot_widget = PlotWidget(self)
        layout = QVBoxLayout(self.plot)
        layout.addWidget(self.plot_widget)
        self.plot_widget.setBackground('w')
        self.plot_widget.setAspectLocked(True)  # Одинаковый масштаб по осям X и Y

    def setup_table_widgets(self):
        """Настройка таблиц."""
        self.targetInfoTableWidget = self.findChild(QTableWidget, 'targetInfoTableWidget')
        self.trappyCircleInfoTableWidget = self.findChild(QTableWidget, 'trappyCircleInfoTableWidget')
        self.hillInfoTableWidget = self.findChild(QTableWidget, 'hillInfoTableWidget')

        # Настройка таблицы для точек
        self.targetInfoTableWidget.setColumnCount(2)
        self.targetInfoTableWidget.setHorizontalHeaderLabels(['X', 'Y'])

        # Настройка таблицы для окружностей
        self.trappyCircleInfoTableWidget.setColumnCount(3)
        self.trappyCircleInfoTableWidget.setHorizontalHeaderLabels(['X', 'Y', 'Radius'])

        # Настройка таблицы для многоугольников
        self.hillInfoTableWidget.setColumnCount(3)
        self.hillInfoTableWidget.setHorizontalHeaderLabels(['Polygon ID', 'X', 'Y'])

    def setup_buttons(self):
        """Настройка кнопок."""
        self.targetAddFromTablePushButton = self.findChild(QPushButton, 'targetAddFromTablePushButton')
        self.targetRemovePushButton = self.findChild(QPushButton, 'targetRemovePushButton')
        self.trappyCircleAddFromTablePushButton = self.findChild(QPushButton, 'trappyCircleAddFromTablePushButton')
        self.trappyCircleRemovePushButton = self.findChild(QPushButton, 'trappyCircleRemovePushButton')
        self.hillAddFromTablePushButton = self.findChild(QPushButton, 'hillAddFromTablePushButton')
        self.hillRemovePushButton = self.findChild(QPushButton, 'hillRemovePushButton')
        self.runPushButton = self.findChild(QPushButton, 'runPushButton')
        self.lolPushButton = self.findChild(QPushButton, 'lolPushButton')

        self.targetRemovePushButton.setEnabled(False)
        self.trappyCircleRemovePushButton.setEnabled(False)
        self.hillRemovePushButton.setEnabled(False)

    def setup_menu(self):
        """Настройка меню."""
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Files')

        load_points_action = QAction('Load points (CSV)', self)
        load_points_action.triggered.connect(self.load_points_from_file)
        file_menu.addAction(load_points_action)

        load_circles_action = QAction('Load Circles (CSV)', self)
        load_circles_action.triggered.connect(self.load_circles_from_file)
        file_menu.addAction(load_circles_action)

        load_polygons_action = QAction('Load hills (CSV)', self)
        load_polygons_action.triggered.connect(self.load_polygons_from_file)
        file_menu.addAction(load_polygons_action)

        load_points_json_action = QAction('Load points (JSON)', self)
        load_points_json_action.triggered.connect(self.load_points_from_json)
        file_menu.addAction(load_points_json_action)

        load_circles_json_action = QAction('Load Circles (JSON)', self)
        load_circles_json_action.triggered.connect(self.load_circles_from_json)
        file_menu.addAction(load_circles_json_action)

        load_polygons_json_action = QAction('Load hills (JSON)', self)
        load_polygons_json_action.triggered.connect(self.load_polygons_from_json)
        file_menu.addAction(load_polygons_json_action)

        save_json_action = QAction('Save to JSON', self)
        save_json_action.triggered.connect(self.save_to_json)
        file_menu.addAction(save_json_action)

    def setup_connections(self):
        """Настройка сигналов и слотов."""
        self.targetAddFromTablePushButton.clicked.connect(self.add_target_from_table)
        self.targetRemovePushButton.clicked.connect(self.remove_target)
        self.trappyCircleAddFromTablePushButton.clicked.connect(self.add_trappy_circle_from_table)
        self.trappyCircleRemovePushButton.clicked.connect(self.remove_trappy_circle)
        self.hillAddFromTablePushButton.clicked.connect(self.add_polygon_vertex_from_table)
        self.hillRemovePushButton.clicked.connect(self.remove_polygon_vertex)
        self.runPushButton.clicked.connect(self.run)
        self.lolPushButton.clicked.connect(self.load_data_from_data4_json)

        self.targetInfoTableWidget.selectionModel().selectionChanged.connect(self.update_remove_button_state)
        self.trappyCircleInfoTableWidget.selectionModel().selectionChanged.connect(self.update_remove_button_state)
        self.hillInfoTableWidget.selectionModel().selectionChanged.connect(self.update_remove_button_state)

        self.targetInfoTableWidget.cellChanged.connect(self.update_plot_on_cell_change)
        self.trappyCircleInfoTableWidget.cellChanged.connect(self.update_plot_on_cell_change)
        self.hillInfoTableWidget.cellChanged.connect(self.update_plot_on_cell_change)

    def load_points_from_file(self):
        """Загрузка точек из CSV файла."""
        file_name = self.open_file_dialog('Открыть файл с точками', 'CSV Files (*.csv);;All Files (*)')
        if file_name:
            self.load_data_from_csv(file_name, self.add_point_to_table)
            self.update_plot()

    def load_circles_from_file(self):
        """Загрузка окружностей из CSV файла."""
        file_name = self.open_file_dialog('Открыть файл с окружностями', 'CSV Files (*.csv);;All Files (*)')
        if file_name:
            self.load_data_from_csv(file_name, self.add_circle_to_table)
            self.update_plot()

    def load_polygons_from_file(self):
        """Загрузка многоугольников из CSV файла."""
        file_name = self.open_file_dialog('Открыть файл с многоугольниками', 'CSV Files (*.csv);;All Files (*)')
        if file_name:
            self.load_data_from_csv(file_name, self.add_polygon_vertices_to_table)
            self.update_plot()

    def load_points_from_json(self):
        """Загрузка точек из JSON файла."""
        file_name = self.open_file_dialog('Открыть JSON файл с точками', 'JSON Files (*.json);;All Files (*)')
        if file_name:
            self.load_data_from_json(file_name, self.add_point_to_table)
            self.update_plot()

    def load_circles_from_json(self):
        """Загрузка окружностей из JSON файла."""
        file_name = self.open_file_dialog('Открыть JSON файл с окружностями', 'JSON Files (*.json);;All Files (*)')
        if file_name:
            self.load_data_from_json(file_name, self.add_circle_to_table)
            self.update_plot()

    def load_polygons_from_json(self):
        """Загрузка многоугольников из JSON файла."""
        file_name = self.open_file_dialog('Открыть JSON файл с многоугольниками', 'JSON Files (*.json);;All Files (*)')
        if file_name:
            self.load_data_from_json(file_name, self.add_polygon_vertices_to_table)
            self.update_plot()

    def open_file_dialog(self, title, filter):
        """Открытие диалогового окна для выбора файла."""
        return QFileDialog.getOpenFileName(self, title, '', filter)[0]

    def load_data_from_csv(self, file_name, add_function):
        """Загрузка данных из CSV файла."""
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    if len(row) == 2:
                        x, y = map(float, row)
                        add_function(x, y)
                    elif len(row) == 3:
                        x, y, radius = map(float, row)
                        add_function(x, y, radius)
                    elif len(row) == 4:
                        polygon_id, x, y = map(float, row[:3])
                        add_function(polygon_id, x, y)

    def load_data_from_json(self, file_name, add_function):
        """Загрузка данных из JSON файла."""
        with open(file_name, 'r') as file:
            data = json.load(file)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        if 'x' in item and 'y' in item:
                            x = float(item['x'])
                            y = float(item['y'])
                            if 'radius' in item:
                                radius = float(item['radius'])
                                add_function(x, y, radius)
                            elif 'polygon_id' in item:
                                polygon_id = int(item['polygon_id'])
                                add_function(polygon_id, x, y)
                            else:
                                add_function(x, y)

    def add_point_to_table(self, x, y):
        """Добавление точки в таблицу."""
        row = self.targetInfoTableWidget.rowCount()
        self.targetInfoTableWidget.insertRow(row)
        self.targetInfoTableWidget.setItem(row, 0, QTableWidgetItem(str(x)))
        self.targetInfoTableWidget.setItem(row, 1, QTableWidgetItem(str(y)))

    def add_circle_to_table(self, x, y, radius):
        """Добавление окружности в таблицу."""
        row = self.trappyCircleInfoTableWidget.rowCount()
        self.trappyCircleInfoTableWidget.insertRow(row)
        self.trappyCircleInfoTableWidget.setItem(row, 0, QTableWidgetItem(str(x)))
        self.trappyCircleInfoTableWidget.setItem(row, 1, QTableWidgetItem(str(y)))
        self.trappyCircleInfoTableWidget.setItem(row, 2, QTableWidgetItem(str(radius)))

    def add_polygon_vertices_to_table(self, polygon_id, x, y):
        """Добавление вершины многоугольника в таблицу."""
        row = self.hillInfoTableWidget.rowCount()
        self.hillInfoTableWidget.insertRow(row)
        self.hillInfoTableWidget.setItem(row, 0, QTableWidgetItem(str(polygon_id)))
        self.hillInfoTableWidget.setItem(row, 1, QTableWidgetItem(str(x)))
        self.hillInfoTableWidget.setItem(row, 2, QTableWidgetItem(str(y)))

    def add_target_from_table(self):
        """Добавление новой строки для точки."""
        row = self.targetInfoTableWidget.rowCount()
        self.targetInfoTableWidget.insertRow(row)
        self.update_plot()
        self.update_remove_button_state()

    def remove_target(self):
        """Удаление выбранной точки."""
        selected_row = self.targetInfoTableWidget.currentRow()
        if selected_row >= 0:
            self.targetInfoTableWidget.removeRow(selected_row)
            self.update_plot()
        self.update_remove_button_state()

    def add_trappy_circle_from_table(self):
        """Добавление новой строки для окружности."""
        row = self.trappyCircleInfoTableWidget.rowCount()
        self.trappyCircleInfoTableWidget.insertRow(row)
        self.update_plot()
        self.update_remove_button_state()

    def remove_trappy_circle(self):
        """Удаление выбранной окружности."""
        selected_row = self.trappyCircleInfoTableWidget.currentRow()
        if selected_row >= 0:
            self.trappyCircleInfoTableWidget.removeRow(selected_row)
            self.update_plot()
        self.update_remove_button_state()

    def add_polygon_vertex_from_table(self):
        """Добавление новой строки для вершины многоугольника."""
        row = self.hillInfoTableWidget.rowCount()
        self.hillInfoTableWidget.insertRow(row)
        self.update_plot()
        self.update_remove_button_state()

    def remove_polygon_vertex(self):
        """Удаление выбранной вершины многоугольника."""
        selected_row = self.hillInfoTableWidget.currentRow()
        if selected_row >= 0:
            polygon_id_item = self.hillInfoTableWidget.item(selected_row, 0)
            if polygon_id_item:
                polygon_id = int(polygon_id_item.text())
                rows_to_remove = []
                for row in range(self.hillInfoTableWidget.rowCount()):
                    current_polygon_id_item = self.hillInfoTableWidget.item(row, 0)
                    if current_polygon_id_item and int(current_polygon_id_item.text()) == polygon_id:
                        rows_to_remove.append(row)

                for row in reversed(rows_to_remove):
                    self.hillInfoTableWidget.removeRow(row)

                for row in range(self.hillInfoTableWidget.rowCount()):
                    current_polygon_id_item = self.hillInfoTableWidget.item(row, 0)
                    if current_polygon_id_item:
                        current_polygon_id = int(current_polygon_id_item.text())
                        if current_polygon_id > polygon_id:
                            self.hillInfoTableWidget.setItem(row, 0, QTableWidgetItem(str(current_polygon_id - 1)))

                self.update_plot()

    def update_remove_button_state(self):
        """Обновление состояния кнопок удаления."""
        selected_target_row = self.targetInfoTableWidget.currentRow()
        selected_circle_row = self.trappyCircleInfoTableWidget.currentRow()
        selected_polygon_row = self.hillInfoTableWidget.currentRow()

        self.targetRemovePushButton.setEnabled(selected_target_row >= 0)
        self.trappyCircleRemovePushButton.setEnabled(selected_circle_row >= 0)
        self.hillRemovePushButton.setEnabled(selected_polygon_row >= 0)

    def update_plot_on_cell_change(self, row, column):
        """Обновление графика при изменении ячейки."""
        if column in [0, 1, 2]:
            self.update_plot()

    def update_plot(self):
        """Обновление графика."""
        self.plot_widget.clear()
        self.draw_targets()
        self.draw_circles()
        self.draw_polygons()
        self.plot_widget.replot()

    def draw_targets(self):
        """Отрисовка точек на графике."""
        for row in range(self.targetInfoTableWidget.rowCount()):
            x_item = self.targetInfoTableWidget.item(row, 0)
            y_item = self.targetInfoTableWidget.item(row, 1)
            if x_item and y_item:
                x = float(x_item.text())
                y = float(y_item.text())
                self.plot_widget.plot([x], [y], pen=None, symbol='o', symbolSize=5, symbolBrush=QColor(255, 0, 0))

    def draw_circles(self):
        """Отрисовка окружностей на графике."""
        for row in range(self.trappyCircleInfoTableWidget.rowCount()):
            x_item = self.trappyCircleInfoTableWidget.item(row, 0)
            y_item = self.trappyCircleInfoTableWidget.item(row, 1)
            radius_item = self.trappyCircleInfoTableWidget.item(row, 2)
            if x_item and y_item and radius_item:
                x = float(x_item.text())
                y = float(y_item.text())
                radius = float(radius_item.text())
                self.draw_circle(x, y, radius)

    def draw_circle(self, x, y, radius):
        """Отрисовка окружности."""
        theta = np.linspace(0, 2 * np.pi, 100)
        circle_x = x + radius * np.cos(theta)
        circle_y = y + radius * np.sin(theta)
        self.plot_widget.plot(circle_x, circle_y, pen=mkPen(color=QColor(0, 0, 255)))

    def draw_polygons(self):
        """Отрисовка многоугольников на графике."""
        polygons = {}
        for row in range(self.hillInfoTableWidget.rowCount()):
            polygon_id_item = self.hillInfoTableWidget.item(row, 0)
            x_item = self.hillInfoTableWidget.item(row, 1)
            y_item = self.hillInfoTableWidget.item(row, 2)
            if polygon_id_item and x_item and y_item:
                polygon_id = int(polygon_id_item.text())
                x = float(x_item.text())
                y = float(y_item.text())
                if polygon_id not in polygons:
                    polygons[polygon_id] = {'x': [], 'y': []}
                polygons[polygon_id]['x'].append(x)
                polygons[polygon_id]['y'].append(y)

        for polygon_id, data in polygons.items():
            x_values = data['x']
            y_values = data['y']
            x_values.append(x_values[0])
            y_values.append(y_values[0])
            self.plot_widget.plot(x_values, y_values, pen=mkPen(color=QColor(0, 255, 0)))

    def load_data_from_data4_json(self):
        """Загрузка данных из файла data4.json."""
        file_path = "data4.json"
        if not os.path.exists(file_path):
            QtWidgets.QMessageBox.warning(self, "Ошибка", f"Файл {file_path} не найден.")
            return

        with open(file_path, 'r') as file:
            data = json.load(file)

        self.targetInfoTableWidget.setRowCount(0)
        self.trappyCircleInfoTableWidget.setRowCount(0)
        self.hillInfoTableWidget.setRowCount(0)

        for point in data.get("points", []):
            self.add_point_to_table(point["x"], point["y"])

        for circle in data.get("circles", []):
            self.add_circle_to_table(circle[0], circle[1], circle[2])

        id = 0
        for polygon in data.get("polygons", []):
            for vertex in polygon:
                self.add_polygon_vertices_to_table(vertex.get("polygon_id", id), vertex["x"], vertex["y"])
            id += 1

        self.update_plot()
    

    def run(self):
        """Расчет и отрисовка траектории движения дрона."""
        data = self.tables_to_dict()

        t = Task(data)
        matrix = t.length_matrix
        s = t.length_matrix.shape[0]

        # Расчет траектории
        ans, answer = algorithm_Lit(matrix, s - 1, 1)
        print(matrix)
        print(ans, answer)

        # Преобразование данных для отрисовки
        points = data.get("points", [])
        circles = data.get("circles", [])
        polygons = data.get("polygons", [])

        # Создаем словарь для быстрого доступа к точкам по их номерам
        point_dict = {i + 1: (point["x"], point["y"]) for i, point in enumerate(points)}

        # Очистка графика
        self.plot_widget.clear()

        # Отрисовка точек
        for point in points:
            self.plot_widget.plot([point["x"]], [point["y"]], pen=None, symbol='o', symbolSize=5, symbolBrush=QColor(255, 0, 0))

        # Отрисовка окружностей
        for circle in circles:
            x, y, radius = circle
            self.draw_circle(x, y, radius)

        # Отрисовка многоугольников
        for polygon in polygons:
            x_values = [vertex["x"] for vertex in polygon]
            y_values = [vertex["y"] for vertex in polygon]
            x_values.append(x_values[0])
            y_values.append(y_values[0])
            self.plot_widget.plot(x_values, y_values, pen=mkPen(color=QColor(0, 255, 0)))

        # Отрисовка траектории
        if answer:
            gpath = classes.GPath()  # Создаем объект GPath для хранения пути
            for start, end in answer:
                # Преобразуем номера точек в координаты

                if start and end and start != end:
                    gpath += t.path_matrix[start - 1, end - 1]

            #Проверяем типы ребер в пути
            for figure in gpath.route:
                if isinstance(figure, classes.Line):
                    self.draw_line(figure)
                elif isinstance(figure, classes.Arc):
                    self.draw_arc(figure)

        self.plot_widget.replot()

    def draw_line(self, line):
        """Отрисовка линии на графике."""
        self.plot_widget.plot(
            [line.first_point.x, line.second_point.x],
            [line.first_point.y, line.second_point.y],
            pen=mkPen(color=(255, 0, 0), width=2)
    )

    def draw_arc(self, arc):
        """Отрисовка дуги на графике."""
        # Вычисляем начальный и конечный углы
        start_angle = np.arctan2(arc.first_point.y - arc.circle.center.y, arc.first_point.x - arc.circle.center.x)
        end_angle = np.arctan2(arc.second_point.y - arc.circle.center.y, arc.second_point.x - arc.circle.center.x)

        # Убеждаемся, что end_angle больше start_angle (для меньшей дуги)

        # Генерируем точки для отрисовки дуги
        num_points = 100
        angles = np.linspace(min(start_angle, end_angle), max(start_angle, end_angle), num_points)
        x = arc.circle.center.x + arc.circle.radius * np.cos(angles)
        y = arc.circle.center.y + arc.circle.radius * np.sin(angles)

        # Отрисовываем дугу
        self.plot_widget.plot(x, y, pen=mkPen(color=(255, 0, 0), width=2))

    def plot_trajectory(self, task, edges):
        """Отрисовка траектории на графике по списку рёбер."""
        for edge in edges:
            if isinstance(edge, classes.Line):
                self.draw_line(edge)
            elif isinstance(edge, classes.Arc):
                self.draw_arc(edge)

    def tables_to_dict(self):
        """Преобразование данных из таблиц в словарь."""
        data = {
            "points": [],
            "circles": [],
            "polygons": [],
            "forbid_segments": []
        }

        for row in range(self.targetInfoTableWidget.rowCount()):
            x_item = self.targetInfoTableWidget.item(row, 0)
            y_item = self.targetInfoTableWidget.item(row, 1)
            if x_item and y_item:
                x = float(x_item.text())
                y = float(y_item.text())
                data["points"].append({"x": x, "y": y})

        for row in range(self.trappyCircleInfoTableWidget.rowCount()):
            x_item = self.trappyCircleInfoTableWidget.item(row, 0)
            y_item = self.trappyCircleInfoTableWidget.item(row, 1)
            radius_item = self.trappyCircleInfoTableWidget.item(row, 2)
            if x_item and y_item and radius_item:
                x = float(x_item.text())
                y = float(y_item.text())
                radius = float(radius_item.text())
                data["circles"].append([x, y, radius])

        polygons = {}
        for row in range(self.hillInfoTableWidget.rowCount()):
            polygon_id_item = self.hillInfoTableWidget.item(row, 0)
            x_item = self.hillInfoTableWidget.item(row, 1)
            y_item = self.hillInfoTableWidget.item(row, 2)
            if polygon_id_item and x_item and y_item:
                polygon_id = int(polygon_id_item.text())
                x = float(x_item.text())
                y = float(y_item.text())
                if polygon_id not in polygons:
                    polygons[polygon_id] = []
                polygons[polygon_id].append({"x": x, "y": y})

        for polygon in polygons.values():
            data["polygons"].append(polygon)

        return data

    def save_to_json(self):
        """Сохранение данных в JSON файл."""
        data = self.tables_to_dict()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save JSON File", "", "JSON Files (*.json);;All Files (*)")
        if file_name:
            with open(file_name, 'w') as file:
                json.dump(data, file, indent=4)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
