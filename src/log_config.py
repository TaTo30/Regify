def log_config():
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
          "baseFormatter": {
            "format": "%(asctime)s %(levelname)s %(module)s %(message)s"
          }
        },
        "handlers": {
          "consoleHandler": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "baseFormatter",
            "stream": "ext://sys.stdout"
          }
        },
        "root": {
          "level": "DEBUG",
          "handlers": [
            "consoleHandler"
          ]
        }
    }
  