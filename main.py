import regedit
import sys
import logging

from http_server import app

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s %(levelname)s %(module)s %(message)s",
    handlers= [
        # logging.FileHandler("app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

if __name__ == "__main__":
    regedit.bind_menu()
    app.run()
    