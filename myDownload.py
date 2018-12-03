#!/usr/bin/env python3


from PyQt5.QtCore import QDir, QFile, QFileInfo, QIODevice, QUrl
from PyQt5.QtWidgets import (QApplication, QDialog, QDialogButtonBox,
        QHBoxLayout, QLabel, QLineEdit, QMessageBox, QProgressDialog,
        QPushButton, QVBoxLayout, QAction, QMainWindow, QTextEdit)
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest


class HttpWindow(QMainWindow):
    def __init__(self, parent=None):
        super(HttpWindow, self).__init__(parent)
        self.title = "OraDocs by littleT"
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 400

        self.docRoot = "https://oradocs-corp.documents.us2.oraclecloud.com/documents/"
        self.url = QUrl()
        self.qnam = QNetworkAccessManager()
        self.reply = None
        self.outFile = None
        self.httpGetId = 0
        self.httpRequestAborted = False

#        self.setGeometry(10, 10, 600, 400)
#        self.urlLineEdit = QLineEdit('https://www.qt.io', self)
#        self.urlLineEdit.setGeometry(12, 40, 590, 20)
#        urlLabel = QLabel("&URL:")
#        urlLabel.setBuddy(self.urlLineEdit)
#        self.statusLabel = QLabel(
#                "Please enter the URL of a file you want to download.", self)
#        self.statusLabel.setWordWrap(True)
#        self.statusLabel.setGeometry(12, 10, 590, 19)

        # self.downloadButton = QPushButton("Download", self)
        # self.downloadButton.setDefault(True)
        # self.downloadButton.move(10, 350)
        # self.downloadButton.clicked.connect(self.onDownloadClick)

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.statusBar().showMessage('Starting ...')
        # for the menu first create some actions to be added like
        # File - Exit action
        exitAction = QAction(QIcon('exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(self.close)
        # File - open
        openAction = QAction(QIcon(''), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Opens a file')
        openAction.triggered.connect(self.openCall)
        # the help actions
        helpAction = QAction(QIcon(''), 'Help', self)
        helpAction.triggered.connect(self.openHelp)
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)
        helpMenu = mainMenu.addMenu('&Help')
        helpMenu.addAction(helpAction)

        self.urlLineEdit = QLineEdit(self)
        self.urlLineEdit.setGeometry(5, 250, 590, 20)
        self.urlLineEdit.setText(self.docRoot)

        self.downloadButton = QPushButton('Click Me', self)
        self.downloadButton.move(10, 275)
        self.downloadButton.clicked.connect(self.onDownloadClick)

        self.quitButton = QPushButton("Quit", self)
        self.quitButton.setAutoDefault(False)
        self.quitButton.clicked.connect(self.close)
        self.quitButton.move(120, 275)

        self.logOutput = QTextEdit(self)
        self.logOutput.setReadOnly(True)
        # self.logOutput.setLineWrapMode(QTextEdit.NoWrap)
        self.logOutput.setGeometry(5, 320, 590, 60)

        self.statusBar().showMessage('waiting for click ...')

    def openCall(self):
        QMessageBox.information(self, "Info",
                                "File Open Menu, work in progress")

    def openHelp(self):
        QMessageBox.information(self, "Info",
                                "Help Menu, work in progress")

    def onDownloadClick(self):
        self.url = QUrl(self.docRoot)
        self.logOutput.insertPlainText("onclick before startReq -> url %s\n"
                                       % self.url.toString())
        # start the request
        self.startRequest(self.url)
        self.logOutput.insertPlainText("onclick after startReq -> url %s\n"
                                       % self.url.toString())
        # do we need authorization
        self.qnam.authenticationRequired.connect(
                self.slotAuthenticationRequired)
        # do we go ssl errors
        self.qnam.sslErrors.connect(self.sslErrors)

    def httpFinished(self):
        self.logOutput.insertPlainText("httpFinished ...\n")
        self.logOutput.moveCursor(QTextCursor.End)
        if self.httpRequestAborted:
            # if self.outFile is not None:
            #    self.outFile.close()
            #    self.outFile.remove()
            #    self.outFile = None
            self.logOutput.insertPlainText("httpFinished, httpReqAbr ...\n")
            self.logOutput.moveCursor(QTextCursor.End)
            self.reply.deleteLater()
            # self.outFile.flush()
            # self.outFile.close()
            return

        # maybe updating progress or so
        # self.progressDialog.hide()
        # self.outFile.flush()
        # self.outFile.close()

        # check for redirection
        redirectionTarget = self.reply.attribute(
            QNetworkRequest.RedirectionTargetAttribute)

        if self.reply.error():
            # are we got an error
            # self.outFile.remove()
            QMessageBox.information(self, "HTTP", "Download failed %s"
                                    % self.reply.errorString)
        elif redirectionTarget is not None:
            # self.logOutput.insertPlainText("httpFinished, redirect from %s\n"
            #                                % str(self.url))
            self.logOutput.moveCursor(QTextCursor.End)
            # do we got redirected
            newUrl = self.url.resolved(redirectionTarget)
            self.logOutput.insertPlainText("httpFinished, redirect \n")
            #                               % newUrl.toString())
            self.logOutput.moveCursor(QTextCursor.End)

            #ret = QMessageBox.question(self, "HTTP", "Redirect to %s." %
            #                           newUrl.toString(),
            #                           QMessageBox.Yes | QMessageBox.No)
            #if ret == QMessageBox.Yes:
            #    # if we saied yes to redirect set the new URL to redirected one
            #    self.url = newUrl
            #    # the reply needs to be nothing
            #    self.reply = None
            #    # self.outFile.open(QIODevice.WriteOnly)
            #    # self.outFile.resize(0)
            #    # and start over
            #    self.startRequest(self.url)
            #    return
            # the new url is the redirected one
            self.url = newUrl
            # the reply needs to be nothing
            self.reply = None
            # and start over
            self.startRequest(self.url)
            return
        else:
            # fileName = QFileInfo(QUrl(self.urlLineEdit.text()).path()).fileName()
            # self.statusLabel.setText("Downloaded %s to %s." % (fileName, QDir.currentPath()))
            # self.statusLabel.setText("Done")
            self.statusBar().showMessage("Done")

        self.reply.deleteLater()
        self.reply = None
        # self.outFile = None

    def startRequest(self, url):
        self.logOutput.insertPlainText("startRequest ...\n")
        self.logOutput.moveCursor(QTextCursor.End)
        # get the requested page
        self.reply = self.qnam.get(QNetworkRequest(url))
        # if we are finished
        self.reply.finished.connect(self.httpFinished)
        # are we ready to read the stuff
        # self.reply.readyRead.connect(self.httpReadyRead)
        # downloading
        # self.reply.downloadProgress.connect(self.updateDataReadProgress)

    def slotAuthenticationRequired(self, authenticator):
        import os
        from PyQt5 import uic
        self.logOutput.insertPlainText("Authentication ...\n")
        self.logOutput.moveCursor(QTextCursor.End)

        self.logOutput.moveCursor(QTextCursor.End)
        self.logOutput.insertPlainText(str(authenticator))

        ui = os.path.join(os.path.dirname(__file__), 'authenticationdialog.ui')
        self.logOutput.moveCursor(QTextCursor.End)
        self.logOutput.insertPlainText(str(ui))

        dlg = uic.loadUi(ui)
        dlg.adjustSize()
        dlg.siteDescription.setText("%s at %s" % (authenticator.realm(), self.url.host()))

        dlg.userEdit.setText(self.url.userName())
        dlg.passwordEdit.setText(self.url.password())

        if dlg.exec_() == QDialog.Accepted:
            authenticator.setUser(dlg.userEdit.text())
            authenticator.setPassword(dlg.passwordEdit.text())

    def sslErrors(self, reply, errors):
        errorString = ", ".join([str(error.errorString()) for error in errors])

        ret = QMessageBox.warning(self, "HTTP Example",
                "One or more SSL errors has occurred: %s" % errorString,
                QMessageBox.Ignore | QMessageBox.Abort)

        if ret == QMessageBox.Ignore:
            self.reply.ignoreSslErrors()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    httpWin = HttpWindow()
    httpWin.show()
    sys.exit(app.exec_())
