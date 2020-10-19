from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
import numpy as np
from options import get_args


class input_unit(QWidget):
    def __init__(self, opt):
        super().__init__()
        self.m = opt.m
        self.n = opt.n
        self.initUi()

    def initUi(self):
        self.layout = QGridLayout()
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.layout.setSpacing(1)
        self.setLayout(self.layout)

        state = np.array([i + 1 for i in range(self.m * self.n)])
        state[self.m * self.n - 1] = 0
        if self.m == 3 and self.n == 3:
            state = np.array([2, 1, 3, 8, 0, 4, 7, 6, 5])
        self.label_list = []
        for i in range(self.m * self.n):
            input_label = QTextEdit()
            if state[i]:
                input_label.setText(str(state[i]))
            else:
                input_label.setText('')

            input_label.setEnabled(False)
            input_label.setStyleSheet("background:transparent;")
            input_label.setAlignment(QtCore.Qt.AlignCenter)
            self.label_list.append(input_label)
        for i in range(self.m * self.n):
            self.layout.addWidget(self.label_list[i], i // self.n, i % self.n)
        # self.show()

    def set_m_n(self, state):
        for i in range(self.m * self.n):
            self.label_list[i].clear()
            self.layout.removeWidget(self.label_list[i])
        self.m, self.n = state.shape
        state = state.reshape(-1)
        for i in range(self.m * self.n):
            input_label = QTextEdit()
            if state[i]:
                input_label.setText(str(state[i]))
            else:
                input_label.setText('')
            input_label.setEnabled(False)
            input_label.setStyleSheet("background:transparent;")
            input_label.setAlignment(QtCore.Qt.AlignCenter)
            self.label_list.append(input_label)
        for i in range(self.m * self.n):
            self.layout.addWidget(self.label_list[i], i // self.n, i % self.n)

    def get_state(self):
        state = []
        for i in range(self.m * self.n):
            if self.label_list[i].toPlainText().isdigit():
                state.append(int(self.label_list[i].toPlainText()))
            elif self.label_list[i].toPlainText() == '':
                state.append(0)
            else:
                return None
        state = np.array(state).reshape((self.m, self.n))
        if self.check_valid(state):
            return state
        return None

    def check_valid(self, state):
        standard_state = np.array([i + 1 for i in range(self.m * self.n)])
        standard_state[self.m * self.n - 1] = 0
        state = state.reshape(-1)
        for i in standard_state:
            if not i in state:
                return False
        return True

    def set_state(self, state):
        state = state.reshape(-1)
        for i in range(self.m * self.n):
            if state[i]:
                self.label_list[i].setText(str(state[i]))
            else:
                self.label_list[i].setText('')
            self.label_list[i].setAlignment(QtCore.Qt.AlignCenter)

    def enable_input(self):
        for i in range(self.m * self.n):
            self.label_list[i].setEnabled(True)

    def disable_input(self):
        for i in range(self.m * self.n):
            self.label_list[i].setEnabled(False)

    def set_size(self, width, height):
        dw = width // self.m
        dh = height // self.n
        for i in range(self.m * self.n):
            self.label_list[i].setBaseSize(dw, dh)
            if len(self.label_list[i].toPlainText()) > 1:
                self.label_list[i].setFontPointSize(dw * 0.2)
            else:
                self.label_list[i].setFontPointSize(dw * 0.2)
        self.setBaseSize(width, height)


if __name__ == "__main__":
    app = QApplication([])
    args = get_args()
    opt = args.parse_args()
    u = input_unit(opt)
    print(u.get_state())
    app.exec_()
