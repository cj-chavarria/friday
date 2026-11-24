import sys

from PySide6.QtCore import Qt, QUrl
from PySide6.QtWebEngineCore import (
    QWebEngineNotification,
    QWebEnginePage,
    QWebEnginePermission,
    QWebEngineProfile,
    qWebEngineChromiumVersion,
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon

CHROMIUM_VERSION = qWebEngineChromiumVersion()
USER_AGENT = f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{CHROMIUM_VERSION} Safari/537.36"
# URL = QUrl("https://web.whatsapp.com/")
URL = QUrl("https://www.bennish.net/web-notifications.html")


class WhatsAppPage(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)

        self.tray = QSystemTrayIcon(visible=True)
        self.tray.setToolTip("Testing")
        print(self.tray.isSystemTrayAvailable())
        print(self.tray.supportsMessages())

        self.initial_setup()
        self.permissionRequested.connect(self.accept_permission)

        self.profile().setNotificationPresenter(self.receive_notifications)

    def receive_notifications(self, n: QWebEngineNotification):
        self.tray.showMessage(str(n.title()), str(n.message()))

    def initial_setup(self) -> None:
        # Initial config when loading the page (set URL, UserAgent and enable Notifications)
        self.setUrl(URL)
        self.profile().setHttpUserAgent(USER_AGENT)
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
