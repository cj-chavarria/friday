import sys

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import (
    QWebEnginePage,
    QWebEnginePermission,
    QWebEngineProfile,
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
URL = "https://web.whatsapp.com/"


class WhatsAppPage(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)

        self.setUrl(QUrl(URL))
        self.profile().setHttpUserAgent(USER_AGENT)

        self.permissionRequested.connect(self.permission_type)

    def permission_type(self, p: QWebEnginePermission):
        print(p.permissionType())


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("friday msg")
        self.setFixedSize(800, 600)

        profile = QWebEngineProfile("friday_profile")
        view = QWebEngineView()

        page = WhatsAppPage(profile, view)
        view.setPage(page)

        self.setCentralWidget(view)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    app.exec()
