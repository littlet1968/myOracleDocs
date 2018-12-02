#!/usr/bin/env python3


from PyQt5.QtCore import QDir, QFile, QFileInfo, QIODevice, QUrl
from PyQt5.QtWidgets import (QApplication, QDialog, QDialogButtonBox,
        QHBoxLayout, QLabel, QLineEdit, QMessageBox, QProgressDialog,
        QPushButton, QVBoxLayout, QMainWindow)
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest


class HttpWindow(QMainWindow):
    def __init__(self, parent=None):
        super(HttpWindow, self).__init__(parent)

        self.docRoot = "https://oradocs-corp.documents.us2.oraclecloud.com/documents/"
        self.url = QUrl()
        self.qnam = QNetworkAccessManager()
        self.reply = None
        self.outFile = None
        self.httpGetId = 0
        self.httpRequestAborted = False

        self.setGeometry(10, 10, 600, 400)

        self.urlLineEdit = QLineEdit('https://www.qt.io', self)
        self.urlLineEdit.setGeometry(12, 40, 590, 20)
        urlLabel = QLabel("&URL:")
        urlLabel.setBuddy(self.urlLineEdit)
        self.statusLabel = QLabel(
                "Please enter the URL of a file you want to download.", self)
        self.statusLabel.setWordWrap(True)
        self.statusLabel.setGeometry(12, 10, 590, 19)

        self.downloadButton = QPushButton("Download", self)
        self.downloadButton.setDefault(True)
        self.downloadButton.move(10, 350)
        self.downloadButton.clicked.connect(self.onDownloadClick)

        self.quitButton = QPushButton("Quit", self)
        self.quitButton.setAutoDefault(False)
        self.quitButton.move(120, 350)

    def onDownloadClick(self):
        self.url = QUrl(self.docRoot)
        # start the request
        self.startRequest(self.url)
        # do we need authorization
        self.qnam.authenticationRequired.connect(
                self.slotAuthenticationRequired)
        # do we go ssl errors
        self.qnam.sslErrors.connect(self.sslErrors)

    def httpFinished(self):
        if self.httpRequestAborted:
            # if self.outFile is not None:
            #    self.outFile.close()
            #    self.outFile.remove()
            #    self.outFile = None

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
            # do we got redirected
            newUrl = self.url.resolved(redirectionTarget)
            ret = QMessageBox.question(self, "HTTP", "Redirect to %s." %
                                       newUrl.toString(),
                                       QMessageBox.Yes | QMessageBox.No)
            if ret == QMessageBox.Yes:
                # if we saied yes to redirect set the new URL to redirected one
                self.url = newUrl
                # the reply needs to be nothing
                self.reply = None
                # self.outFile.open(QIODevice.WriteOnly)
                # self.outFile.resize(0)
                # and start over
                self.startRequest(self.url)
                return
        else:
            # fileName = QFileInfo(QUrl(self.urlLineEdit.text()).path()).fileName()
            # self.statusLabel.setText("Downloaded %s to %s." % (fileName, QDir.currentPath()))
            self.statusLabel.setText("Done")
            self.statusBar().showMessage("Done")

        self.reply.deleteLater()
        self.reply = None
        # self.outFile = None

    def startRequest(self, url):
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


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    httpWin = HttpWindow()
    httpWin.show()
    sys.exit(app.exec_())
