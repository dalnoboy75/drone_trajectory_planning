import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from pyqtgraph import PlotWidget, mkPen, EllipseROI
import numpy as np


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('mainwindow.ui', self)
        self.init_ui()

    def init_ui(self):
        self.plot = self.findChild(QWidget, 'plot')
        self.plot_widget = PlotWidget(self)

        layout = QVBoxLayout(self.plot)
        layout.addWidget(self.plot_widget)

        self.plot_widget.setBackground('w')
        self.targetAddFromTablePushButton = self.findChild(QPushButton, 'targetAddFromTablePushButton')
        self.targetRemovePushButton = self.findChild(QPushButton, 'targetRemovePushButton')
        self.hillAddFromTablePushButton = self.findChild(QPushButton, 'hillAddFromTablePushButton')
        self.hillRemovePushButton = self.findChild(QPushButton, 'hillRemovePushButton')
        self.trappyCircleAddFromTablePushButton = self.findChild(QPushButton, 'trappyCircleAddFromTablePushButton')
        self.trappyCircleRemovePushButton = self.findChild(QPushButton, 'trappyCircleRemovePushButton')

        self.targetInfoTableWidget = self.findChild(QTableWidget, 'targetInfoTableWidget')
        self.hillInfoTableWidget = self.findChild(QTableWidget, 'hillInfoTableWidget')
        self.trappyCircleInfoTableWidget = self.findChild(QTableWidget, 'trappyCircleInfoTableWidget')

        self.targetAddFromTablePushButton.clicked.connect(self.add_target_from_table)
        self.targetRemovePushButton.clicked.connect(self.remove_target)
        # self.hillAddFromTablePushButton.clicked.connect(self.add_hill_from_table)
        # self.hillRemovePushButton.clicked.connect(self.remove_hill)
        self.trappyCircleAddFromTablePushButton.clicked.connect(self.add_trappy_circle_from_table)
        self.trappyCircleRemovePushButton.clicked.connect(self.remove_trappy_circle)

        self.targetInfoTableWidget.setColumnCount(3)
        self.targetInfoTableWidget.setHorizontalHeaderLabels(['ID', 'X', 'Y'])
        self.hillInfoTableWidget.setColumnCount(1)
        self.hillInfoTableWidget.setHorizontalHeaderLabels(['ID'])
        self.trappyCircleInfoTableWidget.setColumnCount(4)
        self.trappyCircleInfoTableWidget.setHorizontalHeaderLabels(['ID', 'X', 'Y', 'Radius'])

        self.points = []
        self.circles = []

        self.targetRemovePushButton.setEnabled(False)
        self.hillRemovePushButton.setEnabled(False)
        self.trappyCircleRemovePushButton.setEnabled(False)
        self.targetInfoTableWidget.selectionModel().selectionChanged.connect(self.update_remove_button_state)
        self.hillInfoTableWidget.selectionModel().selectionChanged.connect(self.update_remove_button_state)
        self.trappyCircleInfoTableWidget.selectionModel().selectionChanged.connect(self.update_remove_button_state)

    def add_target_from_table(self):
        row = self.targetInfoTableWidget.rowCount()
        self.targetInfoTableWidget.insertRow(row)
        self.targetInfoTableWidget.setItem(row, 0, QTableWidgetItem(f'Target{row}'))
        self.targetInfoTableWidget.setItem(row, 1, QTableWidgetItem('0.0'))
        self.targetInfoTableWidget.setItem(row, 2, QTableWidgetItem('0.0'))
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
        self.trappyCircleInfoTableWidget.setItem(row, 0, QTableWidgetItem(f'Circle{row}'))
        self.trappyCircleInfoTableWidget.setItem(row, 1, QTableWidgetItem('0.0'))
        self.trappyCircleInfoTableWidget.setItem(row, 2, QTableWidgetItem('0.0'))
        self.trappyCircleInfoTableWidget.setItem(row, 3, QTableWidgetItem('1.0'))
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
        selected_hill_row = self.hillInfoTableWidget.currentRow()
        selected_circle_row = self.trappyCircleInfoTableWidget.currentRow()

        self.targetRemovePushButton.setEnabled(selected_target_row >= 0)
        self.hillRemovePushButton.setEnabled(selected_hill_row >= 0)
        self.trappyCircleRemovePushButton.setEnabled(selected_circle_row >= 0)

    def update_plot(self):
        self.plot_widget.clear()
        for row in range(self.targetInfoTableWidget.rowCount()):
            x = float(self.targetInfoTableWidget.item(row, 1).text())
            y = float(self.targetInfoTableWidget.item(row, 2).text())
            self.plot_widget.plot([x], [y], pen=None, symbol='o', symbolSize=5, symbolBrush=QColor(255, 0, 0))
        for row in range(self.trappyCircleInfoTableWidget.rowCount()):
            x = float(self.trappyCircleInfoTableWidget.item(row, 1).text())
            y = float(self.trappyCircleInfoTableWidget.item(row, 2).text())
            radius = float(self.trappyCircleInfoTableWidget.item(row, 3).text())
            ellipse = EllipseROI(pos=(x - radius, y - radius), size=(2 * radius, 2 * radius))
            ellipse.setPen(mkPen(color=QColor(0, 0, 255)))
            self.plot_widget.addItem(ellipse)
        self.plot_widget.replot()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
