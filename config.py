from os import getenv

BOT_TOKEN = getenv("BOT_TOKEN")
BOT_OWNER = getenv("BOT_OWNER")
BOT_NAME = getenv("BOT_NAME")
SENTRY_CONFIG = getenv("SENTRY_CONFIG")
HOST = "https://%s.herokuapp.com" % getenv("HEROKU_APP_NAME")
