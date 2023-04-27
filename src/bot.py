import io
from typing import Union, Optional

from telegram import Update, ReplyKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

from config import get_config
from src.buttons_generator import create_buttons_list
from src.constants import actions
from src.fpl.fpl_main import FPLMain
from src.utils import messages
from src.utils.custom_exceptions import InvalidUserID
from PIL import Image, ImageDraw, ImageFont


class Bot:
    user_private_leagues_names: list[str] = []
    relevant_gameweeks: list[str] = []
    selected_league: str
    selected_gameweek: str

    def __init__(self):
        self.config = get_config()
        self.updater = Updater(token=self.config.telegram_bot_token)
        self.dispatcher = self.updater.dispatcher
        self.fpl: FPLMain = FPLMain()
        self.relevant_gameweeks: list[str] = []
        self.dispatcher.add_handler(CommandHandler("start", self.start_command))
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.message_handler))
        self.last_message: str = ''
        self.last_buttons: list[list[str]] = []

    @staticmethod
    def start_command(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=messages.get_start_message(),
                                 parse_mode=ParseMode.MARKDOWN)

    @staticmethod
    def exit(update: Update, context: CallbackContext) -> None:
        print('Bot exited.')
        start_button: list[str] = create_buttons_list([actions.START])
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=messages.GOODBYE,
                                 reply_markup=ReplyKeyboardMarkup(start_button, one_time_keyboard=True,
                                                                  resize_keyboard=True))

    @staticmethod
    def show_invalid_user_id_message(update: Update, context: CallbackContext, error_message: str) -> None:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=messages.get_invalid_message_with_last_message(
                                     messages.ENTER_TEAM_ID, str(error_message)))

    def run(self):
        print('Bot is now running...')
        self.updater.start_polling()

    def message_handler(self, update: Update, context: CallbackContext) -> None:
        answer: str = update.message.text
        if answer.isnumeric():
            try:
                self.fpl.login(answer)
            except InvalidUserID as user_id_err:
                self.show_invalid_user_id_message(update, context, str(user_id_err))
            self.show_leagues_menu(update, context)
        else:
            self.handle_non_integer_answer(update, context, answer)

    def handle_non_integer_answer(self, update: Update, context: CallbackContext, answer: str) -> None:
        if answer == actions.START:
            self.start_command(update, context)
        elif self.user_private_leagues_names and answer in self.user_private_leagues_names:
            self.show_gameweeks_menu(update, context, answer)
        elif answer == actions.GAMEWEEK_SELECTION:
            self.show_gameweeks_menu(update, context)
        elif self.relevant_gameweeks and answer in self.relevant_gameweeks:
            self.show_actions_menu(update, context, answer)
        elif answer == actions.ACTION_SELECTION:
            self.show_actions_menu(update, context)
        elif answer in actions.MAIN_ACTIONS:
            self.do_action(update, context, answer)
        elif answer == actions.LEAGUE_SELECTION:
            self.show_leagues_menu(update, context)
        elif answer == actions.EXIT:
            self.exit(update, context)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=messages.get_invalid_message_with_last_message(self.last_message))

    def show_leagues_menu(self, update: Update, context: CallbackContext) -> None:
        self.user_private_leagues_names = self.fpl.get_user_private_leagues_names()
        self.last_message = messages.get_after_login_message(self.fpl.username)
        self.last_buttons = create_buttons_list(self.user_private_leagues_names)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=self.last_message,
                                 reply_markup=ReplyKeyboardMarkup(self.last_buttons, one_time_keyboard=True,
                                                                  resize_keyboard=True))

    def show_gameweeks_menu(self, update: Update, context: CallbackContext,
                            selected_league: Optional[str] = None) -> None:
        if selected_league:
            self.selected_league = selected_league
        self.last_message = messages.SELECT_GAMEWEEK
        current_gameweek: int = self.fpl.get_current_gameweek()
        self.relevant_gameweeks = actions.get_all_relevant_gameweeks_names(current_gameweek)
        self.last_buttons = create_buttons_list(self.relevant_gameweeks)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=self.last_message,
                                 reply_markup=ReplyKeyboardMarkup(self.last_buttons, one_time_keyboard=True,
                                                                  resize_keyboard=True))

    def show_actions_menu(self, update: Update, context: CallbackContext,
                          selected_gameweek: Optional[str] = None) -> None:
        if selected_gameweek:
            self.selected_gameweek = selected_gameweek
        self.last_message = messages.SELECT_ACTION
        self.last_buttons = create_buttons_list(actions.MAIN_ACTIONS)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=self.last_message,
                                 reply_markup=ReplyKeyboardMarkup(self.last_buttons, one_time_keyboard=True,
                                                                  resize_keyboard=True))

    def show_return_to_menus_menu(self, update: Update, context: CallbackContext) -> None:
        self.last_message = messages.RETURN_TO_MENUS
        self.last_buttons = create_buttons_list(actions.get_all_return_to_menus())
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=self.last_message,
                                 reply_markup=ReplyKeyboardMarkup(self.last_buttons, one_time_keyboard=True,
                                                                  resize_keyboard=True))

    def do_action(self, update: Update, context: CallbackContext, action: str):
        action_lower: str = action.lower()
        data_dict: dict[str, Union[str, int]] = self.fpl.get_league_data_by_function(self.selected_league,
                                                                                     self.selected_gameweek,
                                                                                     action_lower)
        reply_text: str = messages.get_data_dict_as_message(self.selected_league, action,
                                                            self.selected_gameweek, data_dict)

        context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text, parse_mode=ParseMode.MARKDOWN)
        self.show_return_to_menus_menu(update, context)
