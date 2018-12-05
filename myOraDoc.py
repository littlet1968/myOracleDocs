#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import  (pyqtSlot, QUrl, QMetaObject, Qt,
                           QCoreApplication)
# from PyQt5.QtWidgets import (QWidget, QMainWindow, QApplication, QVBoxLayout,
#                             QHBoxLayout, QListView, QLineEdit, QPushButton,
#                             QProgressBar, QTextBrowser, QMenu, QMenuBar,
#                             QStatusBar, QAction, QSizePolicy, QLayout,
#                             QMessageBox)
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import (QMainWindow, QApplication, QMessageBox, QDialog)
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest

# import the UI
from mainGUI import Ui_MainWindow


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.docRoot = "https://oradocs-corp.documents.us2.oraclecloud.com/documents/"
        self.url = QUrl()
        self.qnam = QNetworkAccessManager()
        self.reply = None
        self.outFile = None
        self.httpGetId = 0
        self.httpRequestAborted = False
        self.gotToken = False

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.ui.setupUi.MainWindow.setTitle("OraDocs")
        self._connections()

    def _connections(self):
        self.ui.logOutput.insertPlainText(
            "Setting up actions for all menus and such .")
        self.ui.action_Exit.triggered.connect(self.close)
        self.ui.action_Open.triggered.connect(self.action_open)
        self.ui.action_Save.triggered.connect(self.action_save)
        self.ui.action_SyncAll.triggered.connect(self.action_syncAll)
        self.ui.action_SyncConnect.triggered.connect(self.action_syncConnect)
        self.ui.logOutput.insertPlainText(
            ".. done\n")

    def startRequest(self, url):
        # just some debugging to see were we are
        self.ui.logOutput.insertPlainText("startRequest ...\n")
        # get the URL
        self.ui.logOutput.insertPlainText("get page ...\n")
        self.reply = self.qnam.get(QNetworkRequest(url))

        # not sure if here correct or better somwhere else
        # do we need authorization
        self.qnam.authenticationRequired.connect(
            self.slotAuthenticationRequired)
        # do we got ssl errors
        self.qnam.sslErrors.connect(self.sslErrors)

        # after loading the page do some hadling of the output via the pyslot
        self.reply.finished.connect(self.httpFinished)
        # we should be able to read the stuff
        self.ui.logOutput.insertPlainText("before httpReady ...\n")
        self.reply.readyRead.connect(self.httpReadyRead)
        # not sure if the return is needed
        return

    def httpFinished(self):
        # just some debugging
        self.ui.logOutput.insertPlainText("httpFinished start ...\n")

        # check for redirection
        redirectionTarget = self.reply.attribute(
            QNetworkRequest.RedirectionTargetAttribute)
        # check for reply results
        if self.reply.error():
            # looks like we got an error
            # self.outFile.remove()
            QMessageBox.information(self, "HTTP", "Download failed %s"
                                    % self.reply.errorString)
        elif redirectionTarget is not None:
            # we got redirected
            # output where we are going to
            self.ui.logOutput.insertPlainText("redirect -> %s\n" %
                                              str(redirectionTarget))
            self.ui.logOutput.moveCursor(QTextCursor.End)
            # our new URL is that one
            newUrl = self.url.resolved(redirectionTarget)
            # debug
            self.ui.logOutput.insertPlainText("new URL -> %s\n" %
                                              newUrl.toString())
            self.ui.logOutput.moveCursor(QTextCursor.End)

            # the new url is the redirected one
            self.url = newUrl
            # the reply needs to be nothing
            self.reply = None
            # and start over
            self.startRequest(self.url)
            return
        else:
            # do normal processing
            self.ui.logOutput.insertPlainText("no-redirect -> %s \n" %
                                              self.url.toString())
            self.ui.logOutput.moveCursor(QTextCursor.End)
            self.ui.logOutput.insertPlainText(str(self.reply.header(QNetworkRequest.rawHeader)))
            # as the last actions in here

        self.reply.deleteLater()
        self.reply = None

    def httpReadyRead(self):
        # if self.outFile is not None:
        #    self.outFile.write(self.reply.readAll())
        self.ui.logOutput.insertPlainText("http Ready\n")
        self.ui.logOutput.moveCursor(QTextCursor.End)
        myData = self.reply.readAll()
        # self.ui.logOutput.insertPlainText(str(myData, 'utf-8'))

    def AuthenticationRequired(self, authenticator):
        import os
        from PyQt5 import uic
        ui = os.path.join(os.path.dirname(__file__), 'authenticationdialog.ui')
        dlg = uic.loadUi(ui)
        dlg.adjustSize()
        dlg.siteDescription.setText("%s at %s" % (authenticator.realm(), self.url.host()))
        dlg.userEdit.setText(self.url.userName())
        dlg.passwordEdit.setText(self.url.password())
        if dlg.exec_() == QDialog.Accepted:
            authenticator.setUser(dlg.userEdit.text())
            authenticator.setPassword(dlg.passwordEdit.text())


    @pyqtSlot()
    def action_close(self):
        # print("closing")
        self.quit()

    @pyqtSlot()
    def action_open(self):
        # print("open")
        QMessageBox.information(self, "File Open", "work in progress")

    @pyqtSlot()
    def action_save(self):
        # print("open")
        QMessageBox.information(self, "File Save", "work in progress")

    @pyqtSlot()
    def action_syncAll(self):
        QMessageBox.information(self, "Sync ALl", "work in progress")

    @pyqtSlot()
    # we are starting the the connection actions
    def action_syncConnect(self):
        # just some debugging
        self.ui.logOutput.insertPlainText("syncConnect ...\n")
        # we start with the root URL
        self.url = QUrl(self.docRoot)
        # start the request
        self.startRequest(self.url)
        # not sure if here correct or better in httpFinished
        # do we need authorization
        self.qnam.authenticationRequired.connect(
            self.slotAuthenticationRequired)
        # do we got ssl errors
        self.qnam.sslErrors.connect(self.sslErrors)

        # just some debugging
        self.ui.logOutput.insertPlainText("syncConnect - after start Request\n")

        # QMessageBox.information(self, "Sync Connect", "work in progress")

    @pyqtSlot()
    def slotAuthenticationRequired(self, authenticator):
        # import os
        QMessageBox.information(self, "Authentication", "work in progress")

    def sslErrors(self, reply, errors):
        QMessageBox.information(self, "SSL error", "work in progress")


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    httpWin = AppWindow()
    httpWin.show()
    sys.exit(app.exec_())
