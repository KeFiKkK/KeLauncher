from PyQt5.QtCore import QThread, pyqtSignal, QSize, Qt, QSettings
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QApplication, QLabel, QLineEdit, QComboBox, QSpacerItem, QSizePolicy, QProgressBar, QPushButton, QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets

import sys
import webbrowser
import requests
import os
import json
import subprocess


import minecraft_launcher_lib
from tkinter import ttk 
from minecraft_launcher_lib._internal_types.forge_types import ForgeInstallProfile  
from minecraft_launcher_lib.utils import get_minecraft_directory, get_version_list, get_installed_versions
from minecraft_launcher_lib.forge import install_forge_version, run_forge_installer, list_forge_versions, find_forge_version, is_forge_version_valid, supports_automatic_install, forge_to_installed_version
from minecraft_launcher_lib.install import install_minecraft_version, install_libraries
from minecraft_launcher_lib.command import get_minecraft_command
from random_username.generate import generate_username
from uuid import uuid1


from subprocess import call
from sys import argv, exit


CLIENT_ID = "1"
REDIRECT_URL = "https://authserver.ely.by."

minecraft_directory = get_minecraft_directory().replace('minecraft', 'minecraft')

class LaunchThread(QThread):
    launch_setup_signal = pyqtSignal(str, str)
    progress_update_signal = pyqtSignal(int, int, str)
    state_update_signal = pyqtSignal(bool)

    
    version_id = ''
    username = ''
    password = ''

    progress = 0
    progress_max = 0
    progress_label = ''

    def __init__(self):
        super().__init__()
        self.launch_setup_signal.connect(self.launch_setup)

    def launch_setup(self, version_id, username):
        self.version_id = version_id
        self.username = username
    
    def update_progress_label(self, value):
        self.progress_label = value
        self.progress_update_signal.emit(self.progress, self.progress_max, self.progress_label)
    def update_progress(self, value):
        self.progress = value
        self.progress_update_signal.emit(self.progress, self.progress_max, self.progress_label)
    def update_progress_max(self, value):
        self.progress_max = value
        self.progress_update_signal.emit(self.progress, self.progress_max, self.progress_label)

    def run(self):

        self.state_update_signal.emit(True)

        install_minecraft_version(versionid=self.version_id, minecraft_directory=minecraft_directory, callback={ 'setStatus': self.update_progress_label, 'setProgress': self.update_progress, 'setMax': self.update_progress_max })
        

        if self.username == '':
            self.username = generate_username()[0]
            
            
            
        #Login
        
                

        
        
        
        options = {
            'username': self.username,
            'uuid': str(uuid1()),
            'token': ''
        }

        command = get_minecraft_command(version=self.version_id, minecraft_directory=minecraft_directory, options=options)
        subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        

        
        self.setFixedSize(QSize(784, 526))
        self.centralwidget = QWidget(self)
        self.setStyleSheet("background-color: rgba(80, 80, 80, 0);")
        


        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("kell.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(self, icon,)
        
        self.logo = QLabel(self.centralwidget)
        self.logo.setText('Hyperlink tag <a href="https://kelauncher.ulcraft.com/">click to open to view</a>')
        self.logo.setGeometry(QtCore.QRect(120, 60, 551, 81))
        self.logo.setPixmap(QtGui.QPixmap("C:\Program Files\KeLauncher/kelauncher2.png"))
        self.logo.setScaledContents(True)
        self.logo.setOpenExternalLinks(True)  # Make it a hyperlink 
        self.logo.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.logo.setStyleSheet("         color: red;\n"
"         font: bold 16px;\n"
"         background: transparent;\n"
"         border: none;\n"
"         margin: 0px;\n"
"         padding: 0px;\n"
"")
        
        
        
        self.username = QLineEdit(self.centralwidget)
        self.username.setPlaceholderText('                           Никнейм')
        self.username.setGeometry(QtCore.QRect(110, 240, 211, 21))
        font = QtGui.QFont()
        font.setFamily("Minecraft Rus")
        font.setBold(True)
        font.setWeight(75)
        self.username.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 8pt \"MS Shell Dlg 2\";\n"
"background-color: rgb(33,33,33);\n"
"border-radius: 10px")
        

        self.load_settings()
        

    
       

        self.version_select = QComboBox(self.centralwidget)
        for version in get_version_list():
            self.version_select.addItem(version['id'])
        for version in get_installed_versions (minecraft_directory):
            self.version_select.addItem(version['id'])
        self.version_select.setGeometry(QtCore.QRect(110, 280, 211, 21))
        font = QtGui.QFont()
        font.setFamily("Minecraft Rus")
        font.setBold(True)
        font.setWeight(75)
        self.version_select.setStyleSheet("color: rgb(256, 256, 256);\n"
"alternate-background-color: rgb(33,33,33);\n"
"background-color: rgb(33,33,33);\n"
"border-top-left-radius : 10px;\n"
"border-top-right-radius : 10px;\n"
"border-bottom-left-radius:10px;\n"
"border-bottom-right-radius : 10px;\n"
"")
        
    

        self.load_settingss()


        self.progress_spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        
        self.start_progress_label = QLabel(self.centralwidget)
        self.start_progress_label.setText('')
        self.start_progress_label.setVisible(False)
        font = QtGui.QFont()
        font.setFamily("Minecraft Rus")
        font.setBold(True)
        font.setWeight(75)

        self.start_progress = QProgressBar(self.centralwidget)
        self.start_progress.setProperty('value', 24)
        self.start_progress.setVisible(False)
        self.start_progress.setFormat("                                                                                                                                   %p% ")
        self.start_progress.setGeometry(QtCore.QRect(-10, 0, 801, 20))
        self.start_progress.setStyleSheet("\n"
"\n"
"QProgressBar{\n"
"    background-color: rgb(150, 150, 150);\n"
"    border-radius: 10px; \n"
"    \n"
"    \n"
"    color: rgb(33,33,33);\n"
"    \n"
"    \n"
"    \n"
"    \n"
"    \n"
"    \n"
"    font: 10pt \"Minecraft Ten\";\n"
"}\n"
"\n"
"QProgressBar::chunk{\n"
"    \n"
"    \n"
"    \n"
"    \n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0     rgba(128, 128, 128, 255), stop:1 rgba(185, 185, 185, 255));\n"
"    border-radius :10px;\n"
"}  \n"
"")
        self.start_progress.setMinimumSize(QtCore.QSize(321, 20))
        font = QtGui.QFont()
        font.setFamily("Minecraft Rus")
        font.setBold(True)
        font.setWeight(75)

        
        

        
        

        
        
        self.start_button = QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(140, 330, 141, 71))
        font = QtGui.QFont()
        font.setFamily("Minecraft Rus")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.start_button.setFont(font)
        self.start_button.setFont(font)
        self.start_button.setStyleSheet("color: rgb(229,228,226);\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(33,33,33, 255));\n"
"border-radius: 15px\n"
"\n"
"\n"
"")
        self.start_button.setText('Играть')
        self.start_button.clicked.connect(self.launch_game)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(60, 470, 41, 41))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:\Program Files\KeLauncher\Folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(25, 25))
        self.pushButton.setFont(font)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(33, 33, 33, 255));\n"
"border-radius: 20px\n"
"")
        self.pushButton.clicked.connect(self.open_folder)

        self.username.textChanged.connect(self.save_settings)
        
    
        
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 470, 41, 41))
        font = QtGui.QFont()
        font.setFamily("Minecraft Rus")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(33, 33, 33, 255));\n"
"border-radius: 20px\n"
"")
        self.pushButton_2.setText("")
        self.pushButton_2.clicked.connect(lambda: webbrowser.open('https://discord.gg/Dpvt6R9sPZ'))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:\Program Files\KeLauncher/discord.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_2.setObjectName("pushButton_2")
        
        
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(90, 210, 261, 231))
        self.listWidget.setStyleSheet("background-color: rgba(108,105,96, 125);\n"
"border-radius: 20px")
        self.listWidget.setObjectName("listWidget")
        
        
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(350, 500, 101, 16))
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);\n"
"\n"
"         background: transparent;\n"
"         border: none;\n"
"         margin: 0px;\n"
"         padding: 0px;")
        self.label_4.setObjectName("label_4")
        self.label_4.setText("ⓒ 2024 KeLauncher")


        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(700, 500, 61, 16))
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
"\n"
"         background: transparent;\n"
"         border: none;\n"
"         margin: 0px;\n"
"         padding: 0px;")
        self.label_3.setObjectName("label_3")
        self.label_3.setText("ALPHA v1.6")
        
        
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(400, 220, 301, 221))
        self.textBrowser.setStyleSheet("         color: red;\n"
"         font: bold 16px;\n"
"         background: transparent;\n"
"         border: none;\n"
"         margin: 0px;\n"
"         padding: 0px;\n"
"color: rgb(176, 176, 176);")
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:16px; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">KeLauncher - это любительский проект <br />связаный для вашей удобной игры и разработаный <br />специально без рекламы!<br />Разработчиками являються Top-Hat Entertainment и</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">главным из них KeFiK__ соответственно он все и создал!</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-weight:400;\"><br /></p></body></html>")
        


        
        
        
        

        self.launch_thread = LaunchThread()
        self.launch_thread.state_update_signal.connect(self.state_update)
        self.launch_thread.progress_update_signal.connect(self.update_progress)

        self.setCentralWidget(self.centralwidget)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(-10, -20, 811, 561))
        self.label_2.setStyleSheet("border-radius: 10px")
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("C:\Program Files\KeLauncher/fon3.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_2.raise_()
        self.logo.raise_()
        self.pushButton.raise_()
        self.textBrowser.raise_()
        self.pushButton_2.raise_()
        self.listWidget.raise_()
        self.start_button.raise_()
        self.version_select.raise_()
        self.start_progress.raise_()
        self.label_4.raise_()
        self.label_3.raise_()
        self.username.raise_()



    
    def state_update(self, value):
        self.start_button.setDisabled(value)
        self.start_progress_label.setVisible(value)
        self.start_progress.setVisible(value)
    def update_progress(self, progress, max_progress, label):
        self.start_progress.setValue(progress)
        self.start_progress.setMaximum(max_progress)
        self.start_progress_label.setText(label) 
    def launch_game(self):
        self.launch_thread.launch_setup_signal.emit(self.version_select.currentText(), self.username.text())
        self.launch_thread.start()
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "KeLauncher"))


    def load_settings(self):
        settings = QSettings("MyApp", "KeLauncher")
        saved_username = settings.value("username", "")
        self.username.setText(saved_username)

    def save_settings(self):
        settings = QSettings("MyApp", "KeLauncher")
        settings.setValue("username", self.username.text())
    
    def closeEvent(self, event):
        # Сохранение значения при закрытии
        self.save_settingss()
        event.accept()

    def save_settingss(self):
        settings = QSettings("MyCompany", "MyApp")
        settings.setValue("selected_version", self.version_select.currentText())

    def load_settingss(self):
        settings = QSettings("MyCompany", "MyApp")
        selected_version = settings.value("selected_version", "")
        if selected_version:
            index = self.version_select.findText(selected_version)
            if index != -1:
                self.version_select.setCurrentIndex(index)
    

    def open_folder(self):
        
        
        appdata_roaming = os.getenv('APPDATA')  

        
        specific_folder_path = os.path.join(appdata_roaming, '.minecraft',)  

        
        if os.path.exists(specific_folder_path):
            
            os.startfile(specific_folder_path)
        else:
            print(f"Папка не найдена: {specific_folder_path}")



        self.username.raise_()

    
    


if __name__ == '__main__':
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)

    
    app = QApplication(argv)
    window = MainWindow()
    window.show()    
    exit(app.exec_())
