from src.app import App
from src.download_handler import DownloadHandler
from src.logger import Logger
from src.utils import Theme

logger = Logger("9GAG Downloader")
downloader = DownloadHandler(logger)
theme = Theme()
app = App(downloader=downloader, theme=theme, logger=logger)


def main():
    app.mainloop()


if __name__ == '__main__':
    main()
