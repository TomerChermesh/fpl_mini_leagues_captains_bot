from src.bot import Bot


def app_run():
    bot: Bot = Bot()
    bot.run()


if __name__ == '__main__':
    app_run()
