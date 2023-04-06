import regedit
import sys
import logging
import getopt
import config
import os

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
    entry_args = sys.argv[1:] if os.path.exists(sys.argv[0]) else sys.argv
    opts, args = getopt.getopt(entry_args, "e:", ["dev"])
    for (var, value) in opts:
        if var == "--dev":
            config.develop_mode = True
        if var == "-e":
            config.proxy_mode = True
    
    if config.proxy_mode:
        print("Modo executer")
    else:
        regedit.bind_menu()
        app.run()
