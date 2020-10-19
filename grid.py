from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
import copy
from options import get_args
from Algorithm import *
import time
from PyQt5 import QtTest


class grid(QWidget):
    def __init__(self, opt):
        super().__init__()
        m = opt.m
        n = opt.n
        self.w_g = 0.
        # init_state = np.array([i + 1 for i in range(m * n)]).reshape((m, n))
        # init_state[m - 1, n - 1] = 0
        self.init_state, self.target_state = get_random_init(m, n, steps=opt.random_steps)
        self.img_root = opt.img_src
        self.m, self.n = m, n
        print(self.img_root)
        self.img = QImage(self.img_root)   # .scaled(width, height)
        h, w = self.img.size().height(), self.img.size().width()
        print(h, w)

        # self.sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        # self.sizePolicy.setHeightForWidth(True)
        # self.setSizePolicy(self.sizePolicy)
        self.width = w
        self.height = h
        self.scale = 1
        self.initUi()

    def set_state(self, init_state, target_state=None):
        self.init_state = init_state
        if target_state is not None:
            self.target_state = target_state
        self.adjust_img(init_state)

    def set_w_g(self, w_g):
        self.w_g = w_g

    def initUi(self):
        self.setObjectName("MainWindow")
        self.setWindowTitle("test")

        # set background img
        # palette1 = QPalette()
        # palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('img/background.png')))  # 设置背景图片


        # set window size
        desktop_screen = QDesktopWidget().screenGeometry()

        self.scale = desktop_screen.height() * 0.6 / self.height
        if desktop_screen.width() * 0.6 < self.height * self.scale:
            self.scale *= desktop_screen.width() * 0.6 / (self.height * self.scale)
        # self.move((desktop_screen.width() - self.width * self.scale) // 2,
        #           (desktop_screen.height() - self.height * self.scale) // 2)
        self.width *= self.scale
        self.height *= self.scale
        self.setBaseSize(self.width, self.height)
        # set window position


        img_list = []
        h, w = self.img.size().height() * self.scale, self.img.size().width() * self.scale
        self.img = self.img.scaled(w, h)
        dh = h // self.m
        dw = w // self.n
        for i in range(self.m * self.n):
            x = i // self.n
            y = i % self.n
            img_crop = self.img.copy(y * dw, x * dh, dw, dh)
            img_crop = QPixmap(img_crop)
            img_list.append(img_crop)
        self.img_list = img_list
        self.label_list = []
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(5)
        self.grid_layout.setContentsMargins(20, 10, 10, 10)
        # self.setLayout(self.grid_layout)
        for i in range(self.m * self.n):
            img_label = QLabel(self)
            index = self.init_state[i // self.n, i % self.n]
            if index:
                img_label.setPixmap(img_list[index - 1])
            img_label.setScaledContents(True)
            self.label_list.append(img_label)

        for i in range(self.m * self.n):
            self.grid_layout.addWidget(self.label_list[i], i // self.n, i % self.n)

        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addLayout(self.grid_layout, 0, 0)


        # self.show()
        # self.solve()

    def adjust_img(self, state):
        for i in range(self.m * self.n):
            index = state[i // self.n, i % self.n]
            if index:
                self.label_list[i].setPixmap(self.img_list[index - 1])
            else:
                self.label_list[i].clear()

    def set_m_n(self, init_state, target_state):
        for i in range(self.m * self.n):
            self.label_list[i].clear()
            self.grid_layout.removeWidget(self.label_list[i])
        self.m, self.n = init_state.shape
        self.init_state = init_state
        self.target_state = target_state
        img_list = []
        h, w = self.img.size().height(), self.img.size().width()
        dh = h // self.m
        dw = w // self.n
        for i in range(self.m * self.n):
            x = i // self.n
            y = i % self.n
            img_crop = self.img.copy(y * dw, x * dh, dw, dh)
            img_crop = QPixmap(img_crop)
            img_list.append(img_crop)
        self.img_list = img_list
        self.label_list = []

        # self.setLayout(self.grid_layout)
        for i in range(self.m * self.n):
            img_label = QLabel(self)
            index = self.init_state[i // self.n, i % self.n]
            if index:
                img_label.setPixmap(img_list[index - 1])
            img_label.setScaledContents(True)
            self.label_list.append(img_label)

        for i in range(self.m * self.n):
            self.grid_layout.addWidget(self.label_list[i], i // self.n, i % self.n)


    def solve(self):
        self.solver = solver(self.init_state, self.target_state, self.w_g)
        print(self.init_state, self.target_state)
        print('start solving ....')
        time0 = time.time()
        self.solver.solve()
        time1 = time.time()
        print("solve done! total time:", time1 - time0)
        solve_list = self.solver.solve_list
        return solve_list


if __name__ == '__main__':
    app = QApplication([])
    args = get_args()
    g = grid(args.parse_args())
    app.exec_()
