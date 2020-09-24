from PyQt5 import QtCore, QtGui, QtWidgets



class ModalWind(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ModalWind, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowSystemMenuHint)
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowTitle("Модальное окно")
        self.resize(200, 50)
        butt_hide = QtWidgets.QPushButton('Закрыть модальное окно')
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(butt_hide)
        self.setLayout(vbox)
        butt_hide.clicked.connect(self.close)


class MainWind(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWind, self).__init__(parent)
        self.setWindowTitle("Главное окно")
        self.resize(200, 100)
        butt_show = QtWidgets.QPushButton('Показать модальное окно')
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(butt_show)
        self.setLayout(vbox)
        butt_show.clicked.connect(self.on_show)

    def on_show(self):
        win = ModalWind(self)
        win.show()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWind()
    window.show()
    sys.exit(app.exec_())