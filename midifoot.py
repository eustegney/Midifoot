from PyQt5.QtWidgets import QApplication, QWidget, QGroupBox, QComboBox, \
                            QPushButton, QLabel, QSlider, QLCDNumber, \
                            QTableWidget, QAction, QLineEdit, QAbstractItemView, \
                            QTableWidgetItem, QStyleFactory, QMessageBox, QVBoxLayout, \
                            QFrame, QDialogButtonBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QRect, Qt
from sys import argv, exit
from pygame import midi
import configparser
import pygame


# global options
EXIT_FLAG = False
INI_NAME = 'midifoot.ini'
CONFIG = configparser.ConfigParser
MIDI_DEV_LIST = []
GAMEPAD_DEV_LIST = []
MIDI_DEV = midi.Output  # MIDI instance
GAMEPAD_DEV = 0  # index of Joystick
CURRENT_PRESET_ID = '0'
REFRESH_RATE = 20
NOTE_TRIGGERS = []



class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.assign_actions()
        self.fill_ui()
        self.PbPresetSave.setDisabled(True)
        self.show()
        self.timeloop()

    def init_ui(self):
        """Initialize user interface"""
        app.setStyle(QStyleFactory.create('Fusion'))  # "Windows", "WindowsXP", "Fusion"
        self.setWindowTitle('MidiFoot')
        self.setWindowIcon(QIcon('web.png'))
        self.setFixedSize(361, 372)

        # groupbox 'Preset'
        self.groupBox1 = QGroupBox(self)
        self.groupBox1.setGeometry(QRect(10, -8, 221, 89))

        self.CbPreset = QComboBox(self.groupBox1)
        self.CbPreset.setGeometry(QRect(10, 28, 201, 22))

        self.PbPresetSave = QPushButton(self.groupBox1)
        self.PbPresetSave.setGeometry(QRect(80, 58, 61, 23))
        self.PbPresetSave.setText('save')

        self.PbPresetNew = QPushButton(self.groupBox1)
        self.PbPresetNew.setGeometry(QRect(10, 58, 61, 23))
        self.PbPresetNew.setText('new')

        self.PbPresetDel = QPushButton(self.groupBox1)
        self.PbPresetDel.setGeometry(QRect(150, 58, 61, 23))
        self.PbPresetDel.setText('delete')

        # groupbox 'Options'
        self.groupBox2 = QGroupBox(self)
        self.groupBox2.setGeometry(QRect(10, 72, 341, 109))

        self.CbGamepad = QComboBox(self.groupBox2)
        self.CbGamepad.setGeometry(QRect(10, 28, 151, 22))

        self.label1 = QLabel(self.groupBox2)
        self.label1.setGeometry(QRect(10, 58, 61, 16))
        self.label1.setText('Gamepad in')

        self.CbMidiOut = QComboBox(self.groupBox2)
        self.CbMidiOut.setGeometry(QRect(180, 28, 151, 22))

        self.label2 = QLabel(self.groupBox2)
        self.label2.setGeometry(QRect(290, 58, 47, 13))
        self.label2.setText('MIDI out')

        self.label3 = QLabel(self.groupBox2)
        self.label3.setGeometry(QRect(10, 78, 81, 16))
        self.label3.setText('Refresh rate, ms')

        self.HsRefreshRate = QSlider(self.groupBox2)
        self.HsRefreshRate.setGeometry(QRect(100, 78, 181, 22))
        self.HsRefreshRate.setOrientation(Qt.Horizontal)
        self.HsRefreshRate.setMinimum(0)
        self.HsRefreshRate.setMaximum(1000)

        self.LnRefreshRate = QLCDNumber(self.groupBox2)
        self.LnRefreshRate.setGeometry(QRect(290, 78, 41, 21))

        # key_list table
        self.CvKeyList = QTableWidget(self)
        self.CvKeyList.setGeometry(QRect(10, 190, 341, 141))
        self.CvKeyList.setColumnCount(6)
        self.CvKeyList.verticalHeader().setVisible(False)
        self.CvKeyList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.CvKeyList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.CvKeyList.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.CvKeyList.horizontalHeader().setAutoFillBackground(True)
        self.CvKeyList.setAlternatingRowColors(True)
        self.CvKeyList.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.CvKeyList.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.PbKeyNew = QPushButton(self)
        self.PbKeyNew.setGeometry(QRect(10, 340, 61, 23))
        self.PbKeyNew.setText('new')

        self.PbKeyDel = QPushButton(self)
        self.PbKeyDel.setGeometry(QRect(80, 340, 61, 23))
        self.PbKeyDel.setText('delete')

        self.LeActionMonitor = QLineEdit(self)
        self.LeActionMonitor.setGeometry(QRect(240, 10, 111, 71))
        self.LeActionMonitor.setReadOnly(True)
        self.LeActionMonitor.setFocusPolicy(Qt.NoFocus)

        self.LbLogo = QLabel(self)
        self.LbLogo.setPixmap(QPixmap('LXWlogo.png'))
        self.LbLogo.move(225, 335)

    def assign_actions(self):
        # exit program event
        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

        self.CbMidiOut.currentIndexChanged[int].connect(self.mididev_change)
        self.CbGamepad.currentIndexChanged[int].connect(self.gamepad_change)
        self.CbPreset.currentIndexChanged[int].connect(self.preset_change)
        self.HsRefreshRate.valueChanged[int].connect(self.refresh_rate_change)
        self.PbPresetSave.clicked.connect(self.save_preset)
        self.CvKeyList.itemChanged.connect(self.changes_saved)
        self.CvKeyList.doubleClicked.connect(self.input_button_form)
        self.PbKeyNew.clicked.connect(self.input_button_form)

    def input_button_form(self):
        """Show form for input new button parameters and return values

        """
        input_window = NewControlWindow(self)
        input_window.show()


    def fill_ui(self):
        global INI_NAME, CONFIG, GAMEPAD_DEV_LIST, MIDI_DEV_LIST, REFRESH_RATE

        self.gamepad_load()
        for element in GAMEPAD_DEV_LIST:  # fill combobox CbGamepad
            self.CbGamepad.addItem(element[1])

        self.mididev_load()
        for element in MIDI_DEV_LIST:  # fill combobox CbMidiOut
            self.CbMidiOut.addItem(element[1])

        self.ini_get_config(INI_NAME)
        for section in CONFIG.sections():  # fill combobox CbPreset
            self.CbPreset.addItem(CONFIG.get(section, 'preset_name'))

        self.fill_key_list()

    def set_preset_devices(self):
        """ When user choose another preset in combobox CbPreset

        this sub trying to find and assign devices from ini file
        to current device states

        """
        global CONFIG, CURRENT_PRESET_ID

        config_midi_device = CONFIG.get(CURRENT_PRESET_ID, 'midi_out')  # check and set config's midi device
        for index in range(0, self.CbMidiOut.count()):

            if self.CbMidiOut.itemText(index) == config_midi_device:
                self.CbMidiOut.setCurrentIndex(index)

        config_gamepad_device = CONFIG.get(CURRENT_PRESET_ID, 'gamepad_in')  # check and set config's joystick device
        for index in range(0, self.CbGamepad.count()):
            if self.CbGamepad.itemText(index) == config_gamepad_device:
                self.CbGamepad.setCurrentIndex(index)

    def preset_change(self, cur_id):
        """When user change preset in combobox CbPreset

        sub write preset name to global CURRENT_PRESET_NAME
        and call set_preset_devices()

        """

        global CONFIG, CURRENT_PRESET_ID

        CURRENT_PRESET_ID = str(cur_id)
        self.set_preset_devices()
        self.refresh_rate_change(int(CONFIG.get(CURRENT_PRESET_ID, 'refresh_rate')))
        self.fill_key_list()

    def refresh_rate_change(self, curindex):
        global REFRESH_RATE

        REFRESH_RATE = curindex
        self.LnRefreshRate.display(REFRESH_RATE)
        self.HsRefreshRate.setValue(REFRESH_RATE)

        self.changes_saved(True)

    def action_monitor_write(self, message: str = ''):
        self.LeActionMonitor.setText(message)

    def fill_key_list(self):
        global CONFIG, CURRENT_PRESET_ID, NOTE_TRIGGERS
        button_list = []
        self.CvKeyList.clear()
        NOTE_TRIGGERS.clear()

        preset_items =  CONFIG.items(CURRENT_PRESET_ID)
        for key, value in preset_items:
            if key[0:6] == 'button':
                button_list_parser = [element.strip("'[]") for element in value.split(", ")]
                button_list.append(button_list_parser)

        self.CvKeyList.setRowCount(len(button_list))        # строки в таблице
        for i_row in range(0, len(button_list)):
            NOTE_TRIGGERS.append(False)
            for i_column in range(0, len(button_list[i_row])):
                self.CvKeyList.setItem(i_row, i_column, QTableWidgetItem(button_list[i_row][i_column]))

        self.CvKeyList.setHorizontalHeaderLabels(["ID        ", "Key     ", "Type      ", "Function                     ", "Msg     ", "Cnl      "])
        self.CvKeyList.resizeColumnsToContents()
        self.CvKeyList.resizeRowsToContents()

    def timeloop(self):
        """
        Main background loop
        check events in Joystick stack and print it to MIDI
        ends when flag 'done' is true
        """
        global GAMEPAD_DEV, MIDI_DEV, EXIT_FLAG, CONFIG, CURRENT_PRESET_ID, REFRESH_RATE
        clock = pygame.time.Clock()

        while not EXIT_FLAG:

            pygame.joystick.Joystick(GAMEPAD_DEV).init()

            for event in pygame.event.get():  # User did something.
                if event.type == pygame.JOYBUTTONDOWN:
                    button = event.button
                    self.action_monitor_write('button ' + str(button))
                    # цикл проверки забиндена ли кнопка и выдача сигнала
                    for index in range(0, self.CvKeyList.rowCount()):
                        if self.CvKeyList.item(index, 1).text() == str(button):  # если кнопка забиндена
                            # проверяем функцию кнопки и отправляем миди команду
                            if self.CvKeyList.item(index, 3).text() == 'program_change': #  program_change
                                MIDI_DEV.set_instrument(int(self.CvKeyList.item(index, 4).text()))
                                self.action_monitor_write('program_change ' + self.CvKeyList.item(index, 4).text())
                            elif self.CvKeyList.item(index, 3).text() == 'control_change':
                                MIDI_DEV.note_on(int(self.CvKeyList.item(index, 4).text()), 127)
                                self.action_monitor_write('note_on ' + self.CvKeyList.item(index, 4).text())
                            elif self.CvKeyList.item(index, 3).text() == 'note_trigger':
                                if NOTE_TRIGGERS[index]:
                                    MIDI_DEV.note_off(int(self.CvKeyList.item(index, 4).text()))
                                    self.action_monitor_write('note_off ' + self.CvKeyList.item(index, 4).text())
                                else:
                                    MIDI_DEV.note_on(int(self.CvKeyList.item(index, 4).text()), 127)
                                    self.action_monitor_write('note_on ' + self.CvKeyList.item(index, 4).text())
                                NOTE_TRIGGERS[index] = not NOTE_TRIGGERS[index]

                elif event.type == pygame.JOYBUTTONUP:
                    button = event.button
                    # цикл проверки забиндена ли кнопка и выдача сигнала
                    for index in range(0, self.CvKeyList.rowCount()):
                        if self.CvKeyList.item(index, 1).text() == str(button):  # если кнопка забиндена
                            if self.CvKeyList.item(index, 3) == 'control_change':
                                MIDI_DEV.note_off(int(self.CvKeyList.item(index, 4).text()))
                                self.action_monitor_write('note_off ' + self.CvKeyList.item(index, 4).text())
                            else:
                                self.action_monitor_write()

            clock.tick(REFRESH_RATE)  # refresh rate delay
        self.dying()

    def closeEvent(self, event):
        """Event when user press X to close
        EXIT_FLAG: flag to exit timeloop()
        """
        global EXIT_FLAG

        if self.PbPresetSave.isEnabled():
            reply = QMessageBox.question(self, 'Exit', 'Save changes?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.save_preset()

        EXIT_FLAG = True
        event.accept()

    def dying(self, closemidi: bool = True):
        if closemidi:
            MIDI_DEV.close()
        pygame.quit()
        exit()

    def save_preset(self):
        """Save the config object to file

        Delete BUTTON keys from section CURRENT_PRESET_ID
        and write current parameters

        """
        global CONFIG, CURRENT_PRESET_ID, INI_NAME, MIDI_DEV_LIST, \
               GAMEPAD_DEV_LIST, GAMEPAD_DEV, REFRESH_RATE

        #CONFIG.remove_section(CURRENT_PRESET_ID)
        #CONFIG.add_section(CURRENT_PRESET_ID)

        preset_items = CONFIG.items(CURRENT_PRESET_ID)
        for key, value in preset_items:
            if key[0:6] == 'button':
                CONFIG.remove_option(CURRENT_PRESET_ID, key)



        CONFIG.set(CURRENT_PRESET_ID, 'preset_name', self.CbPreset.currentText())
        CONFIG.set(CURRENT_PRESET_ID, 'midi_out', self.CbMidiOut.currentText())
        CONFIG.set(CURRENT_PRESET_ID, 'gamepad_in', self.CbGamepad.currentText())
        CONFIG.set(CURRENT_PRESET_ID, 'refresh_rate', str(REFRESH_RATE))
        for i_row in range(self.CvKeyList.rowCount()):
            button_row_name = 'button'+str(i_row+1)
            button_row_text = '[' + self.CvKeyList.item(i_row,0).text() + \
                              ', ' + self.CvKeyList.item(i_row,1).text() + \
                              ', \'' + self.CvKeyList.item(i_row, 2).text() + \
                              '\', \'' + self.CvKeyList.item(i_row, 3).text() + \
                              '\', ' + self.CvKeyList.item(i_row, 4).text() + \
                              ', ' + self.CvKeyList.item(i_row,5).text() + ']'
            CONFIG.set(CURRENT_PRESET_ID, button_row_name, button_row_text)

        with open(INI_NAME, "w") as config_file:
            CONFIG.write(config_file)

        self.changes_saved(False)

    def ini_get_config(self, path):
        """Returns the config object

        :arg -- path - path (optional) and name of ini file

        """
        global CONFIG

        CONFIG = configparser.ConfigParser()
        if CONFIG.read(path):
            CONFIG.read(path)
        else:
            ini_not_found = QMessageBox.warning(self, 'Error', 'INI file not found')
            self.dying()

    def gamepad_load(self):
        """Gamepad devices initializing

        :returns global GAMEPAD_DEV_LIST[[id, 'name1'], [id, 'name2'] ... ]
        or [0, 'Gamepad not found']

        """
        global GAMEPAD_DEV_LIST

        pygame.init()

        gamepad_count = pygame.joystick.get_count()  # Get count of joysticks
        if gamepad_count > 0:
            for gamepad_port in range(0, gamepad_count):
                gamepad = pygame.joystick.Joystick(gamepad_port)
                GAMEPAD_DEV_LIST.append([gamepad.get_id(), gamepad.get_name()])
        else:
            gamepad_not_found = QMessageBox.warning(self,'Error', 'Gamepad not found')
            self.dying(False)

    def mididev_load(self):
        """MIDI devices initializing

        :returns global midi_dev_list[[port, 'name1'], [port, 'name2] ... ]
        or [0, 'Midi device not found']

        """
        global MIDI_DEV_LIST
        pygame.midi.init()

        midi_count = midi.get_count()
        flag = False

        if midi_count > 0:
            for midi_dev_port in range(0, midi_count - 1):
                midi_dev_info = midi.get_device_info(midi_dev_port)
                midi_dev_name = midi_dev_info[1].decode('utf-8')
                if midi_dev_info[3] == 1:  # если устройство вывода
                    MIDI_DEV_LIST.append([midi_dev_port, midi_dev_name])
                    flag = True
            if not flag:  # если нет устройства вывода
                midi_not_found = QMessageBox.warning(self, 'Error', 'MIDI device not found')
                self.dying()

    def mididev_change(self, curindex):
        """
        Assign chosen MIDI instance to midi_dev
        :param curindex: index of current device in midi_dev_list
        """
        global MIDI_DEV, MIDI_DEV_LIST
        MIDI_DEV = midi.Output(int(MIDI_DEV_LIST[curindex][0]))
        self.changes_saved(True)

    def gamepad_change(self, curindex):
        """
        Assign chosen Joystick id to gamepad_dev
        Reinitialize current gamepad
        :param curindex: index of current device in gamepad_dev_list
        """
        global GAMEPAD_DEV
        pygame.joystick.Joystick(curindex).init()  # new device
        pygame.joystick.Joystick(GAMEPAD_DEV).quit()  # old device
        GAMEPAD_DEV = curindex  # old = new

        self.changes_saved(True)

    def changes_saved(self, flag: bool = True):
        if flag:
            self.PbPresetSave.setEnabled(True)
        else:
            self.PbPresetSave.setDisabled(True)


class NewControlWindow(QWidget):

    def __init__(self, parent=None):
        print("init...")
        super(NewControlWindow, self).__init__(parent)

        self.init_ui()
        self.setup_defaults()
        self.assign_actions()
        self.fill_ui()


    def init_ui(self):
        self.setWindowFlags(Qt.Dialog | Qt.WindowSystemMenuHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("New control")
        self.setFixedSize(281, 252)
        self.verticalLayoutWidget = QWidget(self)
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 261, 231))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.GbMain = QGroupBox(self.verticalLayoutWidget)
        self.GbMain.setObjectName("GbMain")
        #self.GbMain.setGeometry(QRect(10, 10, 261, 231))

        self.LbControlNum = QLabel(self.GbMain)
        self.LbControlNum.setGeometry(QRect(10, 30, 51, 20))
        self.LbControlNum.setObjectName("LbControlNum")
        self.LbControlNum.setText("Control №")

        self.CbControlNum = QComboBox(self.GbMain)
        self.CbControlNum.setGeometry(QRect(85, 30, 161, 20))
        self.CbControlNum.setCurrentText("")
        self.CbControlNum.setFrame(True)
        self.CbControlNum.setObjectName("CbControlNum")

        self.LbHint = QLabel(self.GbMain)
        self.LbHint.setGeometry(QRect(40, 50, 186, 13))
        self.LbHint.setObjectName("LbHint")
        self.LbHint.setText("Press button or move axe to choose")

        self.line = QFrame(self.GbMain)
        self.line.setGeometry(QRect(10, 70, 239, 3))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")

        self.LbType = QLabel(self.GbMain)
        self.LbType.setGeometry(QRect(10, 80, 24, 20))
        self.LbType.setObjectName("LbType")
        self.LbType.setText("Type")

        self.LbFunction = QLabel(self.GbMain)
        self.LbFunction.setGeometry(QRect(10, 110, 41, 20))
        self.LbFunction.setObjectName("LbFunction")
        self.LbFunction.setText("Function")

        self.LbCommand = QLabel(self.GbMain)
        self.LbCommand.setGeometry(QRect(10, 140, 47, 20))
        self.LbCommand.setObjectName("LbCommand")
        self.LbCommand.setText("Command")

        self.LbPort = QLabel(self.GbMain)
        self.LbPort.setGeometry(QRect(10, 170, 20, 20))
        self.LbPort.setObjectName("LbPort")
        self.LbPort.setText("Port")

        self.LeType = QLineEdit(self.GbMain)
        self.LeType.setEnabled(False)
        self.LeType.setGeometry(QRect(80, 80, 171, 20))
        self.LeType.setObjectName("LeType")

        self.CbFunction = QComboBox(self.GbMain)
        self.CbFunction.setGeometry(QRect(80, 110, 171, 20))
        self.CbFunction.setObjectName("CbFunction")

        self.LeCommand = QLineEdit(self.GbMain)
        self.LeCommand.setGeometry(QRect(80, 140, 81, 20))
        self.LeCommand.setInputMethodHints(Qt.ImhDigitsOnly)
        self.LeCommand.setInputMask("")
        self.LeCommand.setText("")
        self.LeCommand.setObjectName("LeCommand")

        self.LePort = QLineEdit(self.GbMain)
        self.LePort.setGeometry(QRect(80, 170, 81, 20))
        self.LePort.setInputMethodHints(Qt.ImhDigitsOnly)
        self.LePort.setObjectName("LePort")

        self.LbCommandHint = QLabel(self.GbMain)
        self.LbCommandHint.setGeometry(QRect(180, 140, 47, 13))
        self.LbCommandHint.setObjectName("LbCommandHint")
        self.LbCommandHint.setText("0...127")

        self.LbPortHint = QLabel(self.GbMain)
        self.LbPortHint.setGeometry(QRect(180, 170, 47, 13))
        self.LbPortHint.setObjectName("LbPortHint")
        self.LbPortHint.setText("0...127")

        self.verticalLayout.addWidget(self.GbMain)

        self.BbOkCancel = QDialogButtonBox(self.verticalLayoutWidget)
        self.BbOkCancel.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Save)
        self.BbOkCancel.setObjectName("BbOkCancel")

        self.verticalLayout.addWidget(self.BbOkCancel)


    def setup_defaults(self):
        pass
    def assign_actions(self):
        pass
    def fill_ui(self):
        pass
    def on_close(self, choice):
        pass

if __name__ == '__main__':

    app = QApplication(argv)
    ex = MainWindow()
    #exit(app.exec_())