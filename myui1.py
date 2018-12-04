# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(598, 297)
        MainWindow.setMinimumSize(QtCore.QSize(100, 100))
        MainWindow.setMaximumSize(QtCore.QSize(1920, 1024))
        self.mainwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainwidget.sizePolicy().hasHeightForWidth())
        self.mainwidget.setSizePolicy(sizePolicy)
        self.mainwidget.setMinimumSize(QtCore.QSize(100, 100))
        self.mainwidget.setMaximumSize(QtCore.QSize(1024, 786))
        self.mainwidget.setObjectName("mainwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.mainwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 581, 171))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.docsLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.docsLayout.setContentsMargins(0, 0, 0, 0)
        self.docsLayout.setSpacing(10)
        self.docsLayout.setObjectName("docsLayout")
        self.docsView = QtWidgets.QListView(self.verticalLayoutWidget)
        self.docsView.setMinimumSize(QtCore.QSize(90, 90))
        self.docsView.setMaximumSize(QtCore.QSize(1280, 1024))
        self.docsView.setObjectName("docsView")
        self.docsLayout.addWidget(self.docsView)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.mainwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 180, 581, 71))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.logLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.logLayout.setContentsMargins(0, 0, 0, 0)
        self.logLayout.setObjectName("logLayout")
        self.logOutput = QtWidgets.QTextBrowser(self.verticalLayoutWidget_2)
        self.logOutput.setEnabled(True)
        self.logOutput.setMinimumSize(QtCore.QSize(90, 60))
        self.logOutput.setMaximumSize(QtCore.QSize(1920, 1024))
        self.logOutput.setObjectName("logOutput")
        self.logLayout.addWidget(self.logOutput)
        MainWindow.setCentralWidget(self.mainwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 598, 22))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Sync = QtWidgets.QMenu(self.menubar)
        self.menu_Sync.setObjectName("menu_Sync")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_Open = QtWidgets.QAction(MainWindow)
        self.action_Open.setObjectName("action_Open")
        self.action_Exit = QtWidgets.QAction(MainWindow)
        self.action_Exit.setObjectName("action_Exit")
        self.action_Save = QtWidgets.QAction(MainWindow)
        self.action_Save.setObjectName("action_Save")
        self.menu_File.addAction(self.action_Open)
        self.menu_File.addAction(self.action_Save)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Exit)
        self.action_Sync = QtWidgets.QAction(MainWindow)
        self.menu_Sync.addAction(self.action_Sync)
        self.action_Sync.setObjectName("action_Sync")
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Sync.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Sync.setToolTip(_translate("MainWindow", "Sync"))
        self.menu_Sync.setTitle(_translate("MainWindow", "&Sync"))
        self.menu_Help.setToolTip(_translate("MainWindow", "Help"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.action_Open.setText(_translate("MainWindow", "&Open Config"))
        self.action_Exit.setText(_translate("MainWindow", "&Exit"))
        self.action_Save.setText(_translate("MainWindow", "&Save Config"))
