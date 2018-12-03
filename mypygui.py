#!/usr/bin/env python3
# https://data-flair.training/blogs/python-pyqt5-tutorial/
# https://likegeeks.com/pyqt5-tutorial/#Install-PyQt5-designer
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PyQt5.QtWidgets import QLineEdit, QAction, QMessageBox, QTextEdit
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtNetwork import QNetworkReply


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "OraDocs by littleT"
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 400
        self.initUI()

        self.url = QUrl()
        self.qnam = QNetworkAccessManager()
        self.reply = None
        self.outFile = None
        self.httpGetId = 0
        self.httpRequestAborted = False

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
        openAction.triggered.connect(self.openCall())
        # the help actions
        helpAction = QAction(QIcon(''), 'Help', self)
        helpAction.triggered.connect(self.openHelp)
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)
        helpMenu = mainMenu.addMenu('&Help')
        helpMenu.addAction(helpAction)

        self.logOutput = QTextEdit(self)
        self.logOutput.setReadOnly(True)
        # self.logOutput.setLineWrapMode(QTextEdit.NoWrap)
        self.logOutput.setGeometry(5, 200, 590, 60)

        self.statusBar().showMessage('waiting for click ...')
        self.urlLineEdit = QLineEdit(self)
        # self.textbox.move(5, 300)
        # self.textbox.resize(590, 20)
        self.urlLineEdit.setGeometry(5, 325, 590, 20)

        self.button = QPushButton('Click Me', self)
        self.button.move(10, 350)
        self.button.clicked.connect(self.doRequest)


    def doRequest(self):
        self.root = "https://oradocs-corp.documents.us2.oraclecloud.com/documents/"
        # url = "https://www.google.com"
        self.url = QUrl(self.root)

        self.httpRequestAborted = False
        self.startRequest(self.url)
        self.downloadFile()


        self.qnam.authenticationRequired.connect(
                self.slotAuthenticationRequired)

    def startRequest(self, url):
        self.reply = self.qnam.get(QNetworkRequest(url))
        self.reply.finished.connect(self.httpFinished)
        self.reply.readyRead.connect(self.httpReadyRead)

    def downloadFile(self):
        self.url = QUrl(self.urlLineEdit.text())
        fileInfo = QFileInfo(self.url.path())
        fileName = fileInfo.fileName()

        if not fileName:
            fileName = 'index.html'

        if QFile.exists(fileName):
            ret = QMessageBox.question(self, "HTTP",
                    "There already exists a file called %s in the current "
                    "directory. Overwrite?" % fileName,
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if ret == QMessageBox.No:
                return

            QFile.remove(fileName)

        self.outFile = QFile(fileName)
        if not self.outFile.open(QIODevice.WriteOnly):
            QMessageBox.information(self, "HTTP",
                    "Unable to save the file %s: %s." % (fileName, self.outFile.errorString()))
            self.outFile = None
            return

        self.progressDialog.setWindowTitle("HTTP")
        self.progressDialog.setLabelText("Downloading %s." % fileName)
        self.downloadButton.setEnabled(False)

        self.httpRequestAborted = False
        self.startRequest(self.url)

    def cancelDownload(self):
        self.statusLabel.setText("Download canceled.")
        self.httpRequestAborted = True
        if self.reply is not None:
            self.reply.abort()
        self.downloadButton.setEnabled(True)

    def httpFinished(self):
        if self.httpRequestAborted:
            if self.outFile is not None:
                self.outFile.close()
                self.outFile.remove()
                self.outFile = None

            self.reply.deleteLater()
            self.reply = None
            # self.progressDialog.hide()
            return

        # self.progressDialog.hide()
        self.outFile.flush()
        self.outFile.close()

        redirectionTarget = self.reply.attribute(QNetworkRequest.RedirectionTargetAttribute)

        if self.reply.error():
            self.outFile.remove()
            QMessageBox.information(self, "HTTP",
                    "Download failed: %s." % self.reply.errorString())
            self.downloadButton.setEnabled(True)
        elif redirectionTarget is not None:
            newUrl = self.url.resolved(redirectionTarget)

            ret = QMessageBox.question(self, "HTTP",
                    "Redirect to %s?" % newUrl.toString(),
                    QMessageBox.Yes | QMessageBox.No)

            if ret == QMessageBox.Yes:
                self.url = newUrl
                self.reply.deleteLater()
                self.reply = None
                self.outFile.open(QIODevice.WriteOnly)
                self.outFile.resize(0)
                self.startRequest(self.url)
                return
        else:
            fileName = QFileInfo(QUrl(self.urlLineEdit.text()).path()).fileName()
            self.statusLabel.setText("Downloaded %s to %s." % (fileName, QDir.currentPath()))

            self.downloadButton.setEnabled(True)

        self.reply.deleteLater()
        self.reply = None
        self.outFile = None

    def httpReadyRead(self):
        if self.outFile is not None:
            self.outFile.write(self.reply.readAll())

    def updateDataReadProgress(self, bytesRead, totalBytes):
        if self.httpRequestAborted:
            return

        self.progressDialog.setMaximum(totalBytes)
        self.progressDialog.setValue(bytesRead)

    def slotAuthenticationRequired(self, authenticator):
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

    def sslErrors(self, reply, errors):
        errorString = ", ".join([str(error.errorString()) for error in errors])

        ret = QMessageBox.warning(self, "HTTP Example",
                "One or more SSL errors has occurred: %s" % errorString,
                QMessageBox.Ignore | QMessageBox.Abort)

        if ret == QMessageBox.Ignore:
            self.reply.ignoreSslErrors()

    def openCall(self):
        print("Open Call")

    def openHelp(self):
        print("Open Help")

    @pyqtSlot()
    def onClick(self):
        # textboxValue = self.textbox.text()
        # QMessageBox.question(self, 'Hello World!', "Confirm: " + textboxValue,
        #                     QMessageBox.Ok, QMessageBox.Ok)
        # self.textbox.setText("...")
        myRet = self.myDocs.doRequest("https://www.google.com")
        self.logOutput.moveCursor(QTextCursor.End)
        print(myRet)
        self.logOutput.insertPlainText(myRet)

    @pyqtSlot()
    def processReq(self):
        if self.nam.bytesAvailable():
            self.logOutput.moveCursor(QTextCursor.End)
            self.logOutput.insertPlainText('We are connected\n')
            bytes_string = self.nam.readAll()

        self.nam.deleteLater()

    @pyqtSlot(QNetworkReply.NetworkError)
    def processErr(self, code):
        self.msg.critical(None, "Info", "You are not connected to the Internet.")
        print(code)

if __name__=='__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
