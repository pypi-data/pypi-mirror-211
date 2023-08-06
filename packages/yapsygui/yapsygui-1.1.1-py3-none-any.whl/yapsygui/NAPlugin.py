import abc
import json

from qtpy.QtWidgets import QMainWindow

from . import NetworkRequest
from .APlugin import APlugin
from qtpy import QtNetwork


BAD_CONNECTION = "Error, remote host seems down."


class NAPlugin(APlugin, NetworkRequest):

    def __init__(self, text: str, icon: str, shortcut: str, tip: str):
        NetworkRequest.__init__(self)
        APlugin.__init__(self, text, icon, shortcut, tip)
        self.reply = None
        self.service = None
        self.netaccess = QtNetwork.QNetworkAccessManager()

    def handleUploadProgress(self, sent, total):
        self.onRequestProgress(sent, total)

    def clearRequest(self):
        self.multiPart.deleteLater()
        self.reply.deleteLater()
        self.reply = None

    def handleFinished(self):
        reply = self.reply.readAll()
        try:
            reply = json.loads(str(reply, "utf-8"))
            self.onRequestResponse(reply, self.service.api)
        except json.decoder.JSONDecodeError:
            self.onRequestError(reply, "bad-json")
        finally:
            self.clearRequest()

    def handleError(self):
        self.onRequestError(self.reply.errorString(), self.reply.error())

    def runRemoteTask(self, file, service):
        self.service = service
        self.uploadFile(file, self.service.resource())

    def slot(self, context: QMainWindow):
        pass

    @abc.abstractmethod
    def onRequestResponse(self, reply, api):
        raise NotImplementedError

    @abc.abstractmethod
    def onRequestProgress(self, sent, total):
        raise NotImplementedError

    @abc.abstractmethod
    def onRequestError(self, message, error):
        raise NotImplementedError



