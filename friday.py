import sys

from PySide6.QtCore import Qt, QUrl, Slot
from PySide6.QtWebEngineCore import (
    QWebEngineNotification,
    QWebEnginePage,
    QWebEnginePermission,
    QWebEngineProfile,
    qWebEngineChromiumVersion,
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow

CHROMIUM_VERSION = qWebEngineChromiumVersion()
USER_AGENT = f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{CHROMIUM_VERSION} Safari/537.36"
URL = QUrl("https://web.whatsapp.com/")


class WhatsAppPage(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)
        self.initial_setup()
        self.permissionRequested.connect(self.accept_permission)
        self.profile().setNotificationPresenter(self.receive_notifications)

    def receive_notifications(self, n: QWebEngineNotification):
        print(n.title(), n.message(), n.icon())

    def initial_setup(self) -> None:
        # Initial config when loading the page (set url, useragent and enable notifications)
        self.profile().setHttpUserAgent(USER_AGENT)
        self.setUrl(URL)
        self.profile().queryPermission(
            URL, QWebEnginePermission.PermissionType.Notifications
        ).grant()

    def accept_permission(self, p: QWebEnginePermission) -> None:
        p.grant()
        print(f"Permission type {p.permissionType().name} accepted.")


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        view = QWebEngineView()
        profile = QWebEngineProfile("friday_profile")
        page = WhatsAppPage(profile, view)

        view.setPage(page)
        self.setCentralWidget(view)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    app.exec()
