import sys

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
URL = "https://web.whatsapp.com/"


def main(app):
    window = QMainWindow()
    view = QWebEngineView()

    wa_profile = QWebEngineProfile("fridayProfile")
    wa_profile.setHttpUserAgent(USER_AGENT)

    wa_page = QWebEnginePage(wa_profile)

    view.setPage(wa_page)
    view.load(QUrl(URL))

    window.setCentralWidget(view)

    window.show()
    app.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main(app)
