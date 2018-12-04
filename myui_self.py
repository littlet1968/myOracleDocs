#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import  (pyqtSlot, QUrl, QMetaObject, QRect, Qt,
                           QCoreApplication)
from PyQt5.QtWidgets import (QWidget, QMainWindow, QApplication, QVBoxLayout,
                             QHBoxLayout, QListView, QLineEdit, QPushButton,
                             QProgressBar, QTextBrowser, QMenu, QMenuBar,
                             QStatusBar, QAction, QSizePolicy, QLayout,
                             QMessageBox)
from PyQt5.QtGui import  QIcon, QTextCursor
# from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # give the bay a name
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 400)
        # set the resize policy?
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)

        # create the menu
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 590, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        # create a vertical layout
        self.verticalDocsLayoutWidget = QWidget(MainWindow)
        self.verticalDocsLayoutWidget.setGeometry(
            QRect(5, 25, 180, 590))
        self.verticalDocsLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalDocsLayout = QVBoxLayout(self.verticalDocsLayoutWidget)
        self.verticalDocsLayout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        #self.verticalDocsLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalDocsLayout.setObjectName("verticalDocsLayout")

        # and put a listView in it to show the oracle documents
        self.listDocsView = QListView(self.verticalDocsLayoutWidget)
        self.listDocsView.setObjectName("listDocsView")
        self.listDocsView.setSizePolicy(sizePolicy)


        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        # self.pushButton_3.setText(_translate("MainWindow", "Download"))
        # self.pushButton.setText(_translate("MainWindow", "Quit"))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menuHelp.setTitle(_translate("MainWindow", "&Help"))
        self.actionOpen.setText(_translate("MainWindow", "&Open"))
        self.actionExit.setText(_translate("MainWindow", "&Exit"))


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._connections()

    def _connections(self):
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionOpen.triggered.connect(self.action_open)

    @pyqtSlot()
    def action_close(self):
        print("closing")
        self.quit()

    @pyqtSlot()
    def action_open(self):
        print("open")
        QMessageBox.information(self, "File Open", "work in progress")


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    httpWin = AppWindow()
    httpWin.show()
    sys.exit(app.exec_())
