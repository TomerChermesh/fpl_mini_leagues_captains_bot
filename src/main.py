from bottle import run, post

from src.bot import Bot
from src.config import get_config

config = get_config()


@post('/')
def app_run():
    bot: Bot = Bot()
    bot.run()


app_run()

if __name__ == '__main__':
    run(host='localhost', port=config.port, debug=True)
