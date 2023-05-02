import regedit
import sys
import logging
import getopt
import config
import os
import proxy
import logging.config
import json
import ui
import log_config

from http_server import app

def config_main_logger():
    try: 
        logging.config.dictConfig(log_config.log_config())
        logger = logging.getLogger(__name__)
        logger.info("Starting application")
    except Exception as e:
        print(e)
        print("logger couldn't be configured")

if __name__ == "__main__":
    print(sys.executable)
    entry_args = sys.argv[1:] if os.path.exists(sys.argv[0]) else sys.argv
    opts, args = getopt.getopt(entry_args, "e:", ["dev"])
    for (var, value) in opts:
        if var == "--dev":
            config.develop_mode = True
        if var == "-e":
            config.proxy_mode = True
    
    if config.proxy_mode:
        command_id = [opt for opt in opts if opt[0] == '-e'][0][1]
        item_path = args[0]
        proxy.execute(command_id, item_path)
    else:
        config_main_logger()
        regedit.bind_menu()
        app = ui.UI()
        app.title("Regify")
        app.mainloop()
        # app.run(port=9776)
