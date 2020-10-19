from grid import *
from input_unit import *
import os
import PyQt5


Stylesheet = '''
#startButton{
border-radius:5px;
background-color: rgb(240,240,240);
}
#GreenProgressBar {
    min-height: 12px;
    max-height: 12px;
    border-radius: 6px;
}
#GreenProgressBar::chunk {
    border-radius: 6px;
    background-color: rgb(0,35,136);
}'''


class MainUi(QWidget):
    def __init__(self):
        super().__init__()
        self.args = get_args()
        self.opt = self.args.parse_args()
        self.w_g = 1.0
        self.initUi()

    def initUi(self):
        self.init_state, self.target = get_random_init(self.opt.m, self.opt.n, 1000)
        self.grid = grid(self.args.parse_args())
        self.input_unit = input_unit(self.args.parse_args())
        self.init_state = self.input_unit.get_state()
        self.grid.adjust_img(self.init_state)

        # set background and size
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('img/background.png')))  # set background
        self.setPalette(palette1)
        self.setWindowIcon(QIcon('img/fire.ico'))

        grid_h, grid_w = self.grid.height, self.grid.width
        desktop_screen = QDesktopWidget().screenGeometry()
        # print(grid_h * 1.2, grid_w * 1.2)
        self.move((desktop_screen.width() - grid_w * 1.2) // 2,
                  (desktop_screen.height() - grid_h * 1.2) // 2)
        self.setBaseSize(grid_w * 1.2, grid_h * 1.2)
        self.input_unit.set_state(self.init_state)
        self.input_unit.set_size(min(grid_h, grid_w) * 0.3, min(grid_w, grid_h) * 0.3)
        # add widgets

        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()
        self.setLayout(self.h_layout)


        self.h_layout.addStretch(1)
        self.h_layout.addWidget(self.grid)
        self.h_layout.addLayout(self.v_layout)
        self.h_layout.addStretch(5)

        self.progress = QProgressBar(self)
        self.progress.setObjectName('GreenProgressBar')
        self.progress.setMaximum(100)
        self.progress.setMinimum(0)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress_txt = QLabel()
        self.progress_txt.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_txt.setText('0/0')


        # button
        self.start_button = QPushButton()
        self.start_button.setText('START')
        self.start_button.setObjectName('startButton')
        self.start_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.button_33 = QRadioButton()
        self.button_33.setText('3x3 random')
        self.button_33_input = QRadioButton()
        self.button_33_input.setText('3x3 manual')
        self.button_mn = QRadioButton()
        self.button_mn.setText('mxn random')
        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(self.button_33)
        self.button_layout.addWidget(self.button_33_input)
        self.button_layout.addWidget(self.button_mn)
        self.button_widget = QWidget()
        self.button_widget.setLayout(self.button_layout)

        # input line edit
        self.input_m = QLineEdit()
        self.input_m.setText('')
        self.input_n = QLineEdit()
        self.input_n.setText('')
        self.label_m = QLabel('m:')
        self.label_n = QLabel('n:')
        self.m_layout = QHBoxLayout()
        self.n_layout = QHBoxLayout()
        self.m_layout.addWidget(self.label_m)
        self.m_layout.addWidget(self.input_m)
        self.n_layout.addWidget(self.label_n)
        self.n_layout.addWidget(self.input_n)
        self.m_widget = QWidget()
        self.m_widget.setLayout(self.m_layout)
        self.n_widget = QWidget()

        self.input_m.setEnabled(False)
        self.input_n.setEnabled(False)
        self.input_m.setText('3')
        self.input_n.setText('3')
        self.input_m.setAlignment(QtCore.Qt.AlignCenter)
        self.input_n.setAlignment(QtCore.Qt.AlignCenter)
        self.n_widget.setLayout(self.n_layout)
        self.mn_layout = QVBoxLayout()
        self.mn_layout.addWidget(self.m_widget)
        self.mn_layout.addStretch(0)
        self.mn_layout.addWidget(self.n_widget)

        # v layout
        self.v_layout.addStretch(1)
        self.v_layout.addWidget(self.button_widget)
        self.v_layout.addLayout(self.mn_layout)
        # self.v_layout.addStretch(1)
        self.v_layout.addWidget(self.start_button)
        self.v_layout.addWidget(self.input_unit)
        self.v_layout.addWidget(self.progress)
        self.v_layout.addWidget(self.progress_txt)
        self.v_layout.addStretch(1)

        self.button_33.clicked.connect(self.on_btn_33_clicked)
        self.button_33_input.clicked.connect(self.on_btn_33_input_clicked)
        self.button_mn.clicked.connect(self.on_btn_mn_clicked)
        self.start_button.clicked.connect(self.on_btn_start_clicked)


        self.show()

    def on_btn_33_clicked(self):
        self.init_state, self.target = get_random_init(3, 3, 1000)
        self.input_unit.disable_input()
        self.input_unit.set_size(self.grid.width * 0.3, self.grid.width * 0.3)
        if self.grid.m != 3 or self.grid.n != 3:
            self.grid.set_m_n(self.init_state, self.target)
            self.input_unit.set_m_n(self.init_state)
            self.input_unit.set_size(self.grid.width * 0.3, self.grid.width * 0.3)
        else:
            self.grid.set_state(self.init_state, self.target)
        self.grid.set_w_g(w_g=1.0)
        self.input_unit.set_state(self.init_state)
        self.input_m.setEnabled(False)
        self.input_n.setEnabled(False)
        self.input_m.setText('3')
        self.input_n.setText('3')

    def on_btn_33_input_clicked(self):
        self.target = np.array([1, 2, 3, 4, 5, 6, 7, 8, 0]).reshape((3, 3))
        s = np.array([2, 1, 3, 8, 0, 4, 7, 6, 5]).reshape((3, 3))
        self.init_state = s
        if self.grid.m != 3 or self.grid.n != 3:
            self.grid.set_m_n(self.init_state, self.target)
            self.input_unit.set_m_n(self.init_state)
            self.input_unit.set_size(self.grid.width * 0.3, self.grid.width * 0.3)
        else:
            self.grid.set_state(s)
        self.grid.set_w_g(w_g=1.0)
        self.input_unit.set_size(self.grid.width * 0.3, self.grid.width * 0.3)
        self.input_unit.set_state(s)
        self.input_unit.enable_input()
        self.input_m.setEnabled(False)
        self.input_n.setEnabled(False)
        self.input_m.setText('3')
        self.input_n.setText('3')

    def on_btn_mn_clicked(self):
        self.input_unit.disable_input()
        self.input_m.setEnabled(True)
        self.input_n.setEnabled(True)

    def on_btn_start_clicked(self):

        if self.button_33.isChecked():
            self.disable_btn()
            self.grid.set_state(self.init_state, self.target)
            self.grid.set_w_g(self.w_g)
            self.input_unit.set_size(self.grid.width * 0.3, self.grid.width * 0.3)
            self.input_unit.set_state(self.init_state)
            solve_list = self.grid.solve()
            print("total steps:", len(solve_list))
            self.progress_txt.setText('0/{}'.format(len(solve_list)))
            self.progress.setValue(0)
            for i, s in enumerate(solve_list):
                self.grid.adjust_img(s)
                self.input_unit.set_state(s)
                QtTest.QTest.qWait(self.opt.pause_time * 5)
                self.progress.setValue((100 * (i + 1)) // len(solve_list))
                self.progress_txt.setText('{}/{}'.format(i + 1, len(solve_list)))
            if not len(solve_list):
                QMessageBox.warning(self, 'warning', 'solve failed!', QMessageBox.Cancel)
                self.enable_btn()
                return
            self.enable_btn()
            self.button_33.setChecked(True)

        elif self.button_33_input.isChecked():
            self.disable_btn()
            self.input_unit.disable_input()
            s = self.input_unit.get_state()
            if s is None:
                QMessageBox.warning(self, 'warning',  'invalid input!', QMessageBox.Cancel)
                self.enable_btn()
                return
            self.init_state = s
            if not self.is_sovable_33(s, self.target):
                QMessageBox.warning(self, 'warning',  'insolvable input!', QMessageBox.Cancel)
                self.enable_btn()
                return

            self.grid.set_state(self.init_state, self.target)
            self.grid.set_w_g(self.w_g)
            self.input_unit.set_size(self.grid.width * 0.3, self.grid.width * 0.3)
            self.input_unit.set_state(self.init_state)
            solve_list = self.grid.solve()
            print("total steps:", len(solve_list))
            self.progress_txt.setText('0/{}'.format(len(solve_list)))
            self.progress.setValue(0)
            for i, s in enumerate(solve_list):
                self.grid.adjust_img(s)
                self.input_unit.set_state(s)
                QtTest.QTest.qWait(self.opt.pause_time * 5)
                self.progress.setValue((100 * (i + 1)) // len(solve_list))
                self.progress_txt.setText('{}/{}'.format(i + 1, len(solve_list)))
            if not len(solve_list):
                QMessageBox.warning(self, 'warning', 'solve failed!', QMessageBox.Cancel)
                self.enable_btn()
                self.input_unit.enable_input()
                return
            self.input_unit.enable_input()
            self.enable_btn()
            self.button_33_input.setChecked(True)

        elif self.button_mn.isChecked():
            self.disable_btn()
            m = self.input_m.text()
            n = self.input_n.text()
            self.input_m.setEnabled(False)
            self.input_n.setEnabled(False)
            if not (m.isdigit() and n.isdigit()):
                QMessageBox.warning(self, 'warning', 'invalid input!', QMessageBox.Cancel)
                self.enable_btn()
                return
            m = int(m)
            n = int(n)
            if m * n > 40:
                QMessageBox.warning(self, 'warning', 'too large m, n!', QMessageBox.Cancel)
                self.enable_btn()
                self.input_m.setEnabled(True)
                self.input_n.setEnabled(True)
                return
            self.init_state, self.target = get_random_init(m, n, 1000)

            if m >= 6 or n >= 6:
                self.init_state, self.target = get_random_init(m, n, min(m * n * 8, 200))
            self.grid.set_m_n(self.init_state, self.target)
            self.grid.set_w_g(0)
            self.input_unit.set_m_n(self.init_state)
            QtTest.QTest.qWait(50)
            self.input_unit.set_size(self.grid.width * 0.3, self.grid.width * 0.3)
            self.input_unit.set_state(self.init_state)
            QtTest.QTest.qWait(100)
            solve_list = self.grid.solve()
            print("total steps:", len(solve_list))
            self.progress_txt.setText('0/{}'.format(len(solve_list)))
            self.progress.setValue(0)
            for i, s in enumerate(solve_list):
                self.grid.adjust_img(s)
                self.input_unit.set_state(s)
                QtTest.QTest.qWait(self.opt.pause_time * 100 // len(solve_list))
                self.progress.setValue((100 * (i + 1)) // len(solve_list))
                self.progress_txt.setText('{}/{}'.format(i + 1, len(solve_list)))
            if not len(solve_list):
                QMessageBox.warning(self, 'warning', 'solve failed!', QMessageBox.Cancel)

            self.enable_btn()
            self.button_mn.setChecked(True)
            self.input_m.setEnabled(True)
            self.input_n.setEnabled(True)

    def enable_btn(self):
        self.start_button.setEnabled(True)
        self.button_33.setCheckable(True)
        self.button_mn.setCheckable(True)
        self.button_33_input.setCheckable(True)
        self.button_33.setEnabled(True)
        self.button_33_input.setEnabled(True)
        self.button_mn.setEnabled(True)

    def disable_btn(self):
        self.start_button.setEnabled(False)
        self.button_33.setCheckable(False)
        self.button_mn.setCheckable(False)
        self.button_33_input.setCheckable(False)
        self.button_33.setEnabled(False)
        self.button_33_input.setEnabled(False)
        self.button_mn.setEnabled(False)

    @staticmethod
    def is_sovable_33(ini, tar):
        init_inversion = 0
        target_inversion = 0
        init_state = ini.reshape(-1).tolist()
        init_state.remove(0)
        target_state = tar.reshape(-1).tolist()
        target_state.remove(0)
        print(init_state, target_state, len(init_state))
        for i in range(len(init_state)):
            for j in range(len(target_state) - i):
                if init_state[i] > init_state[i + j]:
                    init_inversion += 1
                if target_state[i] > target_state[i + j]:
                    target_inversion += 1
        print(target_inversion, init_inversion)
        if init_inversion % 2 == target_inversion % 2:
            return True
        else:
            return False

if __name__ == '__main__':
    app = QApplication([])
    app.setStyleSheet(Stylesheet)
    args = get_args()
    main_window = MainUi()

    app.exec_()
