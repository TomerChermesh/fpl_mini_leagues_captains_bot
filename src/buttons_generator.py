from telegram import KeyboardButton


def create_buttons_list(buttons_titles_ls: list[str]):
    keyboard_buttons = []
    for button_title in buttons_titles_ls:
        keyboard_buttons.append([KeyboardButton(button_title)])

    return keyboard_buttons
