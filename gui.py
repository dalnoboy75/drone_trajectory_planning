import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
    QAction, QFileDialog, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from pyqtgraph import PlotWidget, mkPen
import numpy as np
import csv


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mainwindow.ui', self)
        self.init_ui()

    def init_ui(self):
        self.setup_plot()
        self.setup_table_widgets()
        self.setup_buttons()
        self.setup_menu()
        self.setup_connections()

    def setup_plot(self):
        self.plot = self.findChild(QWidget, 'plot')
        self.plot_widget = PlotWidget(self)
        layout = QVBoxLayout(self.plot)
        layout.addWidget(self.plot_widget)
        self.plot_widget.setBackground('w')
        self.comboBox.addItem("Littl")
        self.comboBox.addItem("Branch and boundary method")
        self.comboBox.currentIndexChanged.connect(self.on_combobox)    

    def setup_table_widgets(self):
        self.targetInfoTableWidget = self.findChild(QTableWidget, 'targetInfoTableWidget')
        self.hillInfoTableWidget = self.findChild(QTableWidget, 'hillInfoTableWidget')
        self.trappyCircleInfoTableWidget = self.findChild(QTableWidget, 'trappyCircleInfoTableWidget')

        self.targetInfoTableWidget.setColumnCount(4)
        self.targetInfoTableWidget.setHorizontalHeaderLabels(['ID', 'X', 'Y'])
        self.hillInfoTableWidget.setColumnCount(1)
        self.hillInfoTableWidget.setHorizontalHeaderLabels(['ID'])
        self.trappyCircleInfoTableWidget.setColumnCount(4)
        self.trappyCircleInfoTableWidget.setHorizontalHeaderLabels(['ID', 'X', 'Y', 'Radius'])

        

    def setup_buttons(self):
        self.targetAddFromTablePushButton = self.findChild(QPushButton, 'targetAddFromTablePushButton')
        self.targetRemovePushButton = self.findChild(QPushButton, 'targetRemovePushButton')
        self.trappyCircleAddFromTablePushButton = self.findChild(QPushButton, 'trappyCircleAddFromTablePushButton')
        self.trappyCircleRemovePushButton = self.findChild(QPushButton, 'trappyCircleRemovePushButton')

        self.targetRemovePushButton.setEnabled(False)
        self.trappyCircleRemovePushButton.setEnabled(False)

    def setup_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('FIles')

        load_points_action = QAction('Load points', self)
        load_points_action.triggered.connect(self.load_points_from_file)
        file_menu.addAction(load_points_action)

        load_circles_action = QAction('Load Circles', self)
        load_circles_action.triggered.connect(self.load_circles_from_file)
        file_menu.addAction(load_circles_action)

        load_polygons_action = QAction('Load hills', self)
        load_polygons_action.triggered.connect(self.load_polygons_from_file)
        file_menu.addAction(load_polygons_action)

    def setup_connections(self):
        self.targetAddFromTablePushButton.clicked.connect(self.add_target_from_table)
        self.targetRemovePushButton.clicked.connect(self.remove_target)
        self.trappyCircleAddFromTablePushButton.clicked.connect(self.add_trappy_circle_from_table)
        self.trappyCircleRemovePushButton.clicked.connect(self.remove_trappy_circle)

        self.targetInfoTableWidget.selectionModel().selectionChanged.connect(self.update_remove_button_state)
        self.trappyCircleInfoTableWidget.selectionModel().selectionChanged.connect(self.update_remove_button_state)

        self.targetInfoTableWidget.cellChanged.connect(self.update_plot_on_cell_change)
        self.trappyCircleInfoTableWidget.cellChanged.connect(self.update_plot_on_cell_change)

    def on_combobox(self, index):
        pass

    def load_points_from_file(self):
        file_name = self.open_file_dialog('Открыть файл с точками', 'CSV Files (*.csv);;All Files (*)')
        if file_name:
            self.load_data_from_csv(file_name, self.add_point_to_table)
            self.update_plot()

    def load_circles_from_file(self):
        file_name = self.open_file_dialog('Открыть файл с окружностями', 'CSV Files (*.csv);;All Files (*)')
        if file_name:
            self.load_data_from_csv(file_name, self.add_circle_to_table)
            self.update_plot()

    def load_polygons_from_file(self):
        file_name = self.open_file_dialog('Открыть файл с многоугольниками', 'CSV Files (*.csv);;All Files (*)')
        if file_name:
            self.load_data_from_csv(file_name, self.add_polygon_to_table)
            self.update_plot()

    def open_file_dialog(self, title, filter):
        return QFileDialog.getOpenFileName(self, title, '', filter)[0]

    def load_data_from_csv(self, file_name, add_function):
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 3:
                    x = float(row[1])
                    y = float(row[2])
                    radius = float(row[3]) if len(row) >= 4 else 0
                    add_function(x, y, radius)

    def add_target_from_table(self):
        row = self.targetInfoTableWidget.rowCount()
        self.targetInfoTableWidget.insertRow(row)
        self.update_plot()
        self.update_remove_button_state()

    def remove_target(self):
        selected_row = self.targetInfoTableWidget.currentRow()
        if selected_row >= 0:
            self.targetInfoTableWidget.removeRow(selected_row)
            self.update_plot()
        self.update_remove_button_state()

    def add_trappy_circle_from_table(self):
        row = self.trappyCircleInfoTableWidget.rowCount()
        self.trappyCircleInfoTableWidget.insertRow(row)
        self.update_plot()
        self.update_remove_button_state()

    def remove_trappy_circle(self):
        selected_row = self.trappyCircleInfoTableWidget.currentRow()
        if selected_row >= 0:
            self.trappyCircleInfoTableWidget.removeRow(selected_row)
            self.update_plot()
        self.update_remove_button_state()

    def update_remove_button_state(self):
        selected_target_row = self.targetInfoTableWidget.currentRow()
        selected_circle_row = self.trappyCircleInfoTableWidget.currentRow()

        self.targetRemovePushButton.setEnabled(selected_target_row >= 0)
        self.trappyCircleRemovePushButton.setEnabled(selected_circle_row >= 0)

    def update_plot_on_cell_change(self, row, column):
        if column in [1, 2, 3]:
            self.update_plot()

    def update_plot(self):
        self.plot_widget.clear()
        self.draw_targets()
        self.draw_circles()
        self.plot_widget.replot()

    def draw_targets(self):
        for row in range(self.targetInfoTableWidget.rowCount()):
            x = float(self.targetInfoTableWidget.item(row, 1).text())
            y = float(self.targetInfoTableWidget.item(row, 2).text())
            radius = float(self.targetInfoTableWidget.item(row, 3).text())
            if radius > 0:
                self.draw_circle(x, y, radius)
            else:
                self.plot_widget.plot([x], [y], pen=None, symbol='o', symbolSize=5, symbolBrush=QColor(255, 0, 0))

    def draw_circles(self):
        for row in range(self.trappyCircleInfoTableWidget.rowCount()):
            x = float(self.trappyCircleInfoTableWidget.item(row, 1).text())
            y = float(self.trappyCircleInfoTableWidget.item(row, 2).text())
            radius = float(self.trappyCircleInfoTableWidget.item(row, 3).text())
            self.draw_circle(x, y, radius)

    def draw_circle(self, x, y, radius):
        theta = np.linspace(0, 2 * np.pi, 100)
        circle_x = x + radius * np.cos(theta)
        circle_y = y + radius * np.sin(theta)
        self.plot_widget.plot(circle_x, circle_y, pen=mkPen(color=QColor(0, 0, 255)))


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
