from os import getenv

BOT_TOKEN = getenv("BOT_TOKEN")
BOT_OWNER = getenv("BOT_OWNER")
HOST = "https://%s.herokuapp.com" % getenv("HEROKU_APP_NAME")
