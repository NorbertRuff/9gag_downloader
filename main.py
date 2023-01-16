from src.app import App
from src.download_handler import Downloader
from src.logger import Logger

logger = Logger("9GAG Downloader")
downloader = Downloader(logger)
app = App(downloader=downloader, logger=logger)


def main():
    app.init_ui()
    app.mainloop()


if __name__ == '__main__':
    main()
