import typing
from qtpy import QtNetwork
from qtpy.QtNetwork import QNetworkRequest, QHttpMultiPart
from qtpy.QtWidgets import QMainWindow, QApplication


def findMainWindow() -> typing.Union[QMainWindow, None]:
    app = QApplication.instance()
    for widget in app.topLevelWidgets():
        if isinstance(widget, QMainWindow):
            return widget
    return None


def makeMultipart(data):
    multiPart = QtNetwork.QHttpMultiPart(QHttpMultiPart.ContentType.FormDataType)
    file_data = QtNetwork.QHttpPart()
    file_data.setHeader(QNetworkRequest.ContentDispositionHeader, 'form-data; name="image"; filename="data"')
    file_data.setHeader(QNetworkRequest.ContentTypeHeader, 'application/octet-stream')
    file_data.setBody(data)
    multiPart.append(file_data)
    return multiPart


def construct_multipart(files):
    multiPart = QtNetwork.QHttpMultiPart(QHttpMultiPart.ContentType.FormDataType)
    for key, data in files.items():
        imagePart = QtNetwork.QHttpPart()
        imagePart.setHeader(QNetworkRequest.ContentDispositionHeader,
                            'form-data; name="%s"; filename="%s"' % (key, key))
        imagePart.setHeader(QNetworkRequest.ContentTypeHeader, 'application/octet-stream')
        imagePart.setBody(data)
        multiPart.append(imagePart)
    return multiPart
