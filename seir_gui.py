#!/usr/bin/env python3
import sys
import os
import string
import random
import argparse

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from seir import SEIR

class Window(QMainWindow):
    def __init__(self, plots_saving_dir):
        super().__init__()

        self.title = "SEIR MODEL DEMOSTRATION"
        self.top = 200
        self.left = 200
        self.width = 1000
        self.height = 560
        self.plots_saving_dir = plots_saving_dir 
        self.init_window()

    def init_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.parameters_title = QLabel(self)
        self.parameters_title.setGeometry(750, 20, 200, 60)
        self.parameters_title.setText("PARAMETERS")
        self.parameters_title.setStyleSheet("font: 30pt")

        self.susceptibles_field = QLineEdit(self)
        self.susceptibles_field.setValidator(QIntValidator())
        self.susceptibles_field.setFont(QFont("Arial",20))
        self.susceptibles_field.move(850, 100)
        self.susceptibles_field.setText('0')
        self.susceptibles_title = QLabel(self)
        self.susceptibles_title.setGeometry(750, 100, 90, 30)
        self.susceptibles_title.setText("Susceptibles")


        self.exposed_field = QLineEdit(self)
        self.exposed_field.setValidator(QIntValidator())
        self.exposed_field.setFont(QFont("Arial",20))
        self.exposed_field.move(850, 140)
        self.exposed_field.setText('0')
        self.exposed_title = QLabel(self)
        self.exposed_title.setGeometry(750, 140, 90, 30)
        self.exposed_title.setText("Exposeds")

        self.infected_field = QLineEdit(self)
        self.infected_field.setValidator(QIntValidator())
        self.infected_field.setFont(QFont("Arial",20))
        self.infected_field.move(850, 180)
        self.infected_field.setText('0')
        self.infecteds_title = QLabel(self)
        self.infecteds_title.setGeometry(750, 180, 90, 30)
        self.infecteds_title.setText("Infecteds")

        self.recovered_field = QLineEdit(self)
        self.recovered_field.setValidator(QIntValidator())
        self.recovered_field.setFont(QFont("Arial",20))
        self.recovered_field.move(850, 220)
        self.recovered_field.setText('0')
        self.recovereds_title = QLabel(self)
        self.recovereds_title.setGeometry(750, 220, 90, 30)
        self.recovereds_title.setText("Recovereds")

        self.beta_field = QLineEdit(self)
        self.beta_field.setValidator(QDoubleValidator(0.99,99.99,2))
        self.beta_field.setMaxLength(4)
        self.beta_field.setFont(QFont("Arial",20))
        self.beta_field.move(850, 280)
        self.beta_field.setText('0')
        self.beta_title = QLabel(self)
        self.beta_title.setGeometry(750, 280, 90, 30)
        self.beta_title.setText("Beta")

        self.gamma_field = QLineEdit(self)
        self.gamma_field.setValidator(QDoubleValidator(0.99,99.99,2))
        self.gamma_field.setMaxLength(4)
        self.gamma_field.setFont(QFont("Arial",20))
        self.gamma_field.move(850, 320)
        self.gamma_field.setText('0')
        self.gamma_title = QLabel(self)
        self.gamma_title.setGeometry(750, 320, 90, 30)
        self.gamma_title.setText("Gamma")

        self.sigma_field = QLineEdit(self)
        self.sigma_field.setValidator(QDoubleValidator(0.99,99.99,2))
        self.sigma_field.setMaxLength(4)
        self.sigma_field.setFont(QFont("Arial",20))
        self.sigma_field.move(850, 360)
        self.sigma_field.setText('0')
        self.sigma_title = QLabel(self)
        self.sigma_title.setGeometry(750, 360, 90, 30)
        self.sigma_title.setText("Sigma")

        self.day_field = QLineEdit(self)
        self.day_field.setValidator(QIntValidator())
        self.day_field.setMaxLength(4)
        self.day_field.setFont(QFont("Arial",20))
        self.day_field.move(850, 400)
        self.day_field.setText('0')
        self.day_title = QLabel(self)
        self.day_title.setGeometry(750, 400, 90, 30)
        self.day_title.setText("Day")

        self.plot_btn = QPushButton('Plot', self)
        self.plot_btn.move(800, 460)
        self.plot_btn.resize(100, 40)
        self.plot_btn.clicked.connect(self.plot)

        self.plot_label = QLabel(self)
        self.plot_label.setGeometry(20, 20, 640, 480)
        self.show()

    def plot(self):
        seir_model = SEIR(float(self.susceptibles_field.text())
                         ,float(self.exposed_field.text()) 
                         ,float(self.infected_field.text())
                         ,float(self.recovered_field.text())
                         ,float(self.beta_field.text())
                         ,float(self.gamma_field.text())
                         ,float(self.sigma_field.text())
                         ,int(self.day_field.text()))
        seir_model.solve()
        self.plot_saving_path = os.path.join(self.plots_saving_dir, self.random_string() + '.png')
        seir_model.draw(self.plot_saving_path)
        self.plot_label.setPixmap(QPixmap(self.plot_saving_path))

    @staticmethod
    def random_string(length=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))
    
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", type=str, default="/tmp", help="Path to store generated plots.")
    return parser.parse_args()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    args = parse_arguments()
    window = Window(args.output)
    sys.exit(app.exec_())
