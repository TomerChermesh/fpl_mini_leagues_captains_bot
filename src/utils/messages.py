from typing import Final, Union

START_MESSAGE: Final[str] = "*Hi! It's FPL Mini-Leagues Bot* 🦁⚽🏆\n\nHere you can get your mini-league's captaincy " \
                            "& chips easily.\n\nI'm working only with mini-leagues with 50 managers at most so if " \
                            "your mini-league is bigger that that, you will get the lists only for the first 50 " \
                            "teams at your table"

ENTER_TEAM_ID: Final[str] = "Now, please enter you FPL team ID 🙏🏼"
GOODBYE: Final[str] = "Thank you! Hope to see you next time 👋🏼"
INVALID_ANSWER: Final[str] = "Invalid answer 😣"
RETURN_TO_MENUS: Final[str] = "Please select a menu to return to or exit 🙏🏼"
SELECT_GAMEWEEK: Final[str] = "Please select a gameweek to get info about 🙏🏼"
SELECT_ACTION: Final[str] = "Please select one of the following actions 🙏🏼"


def get_invalid_message_with_last_message(last_message: str, invalid_text: str = INVALID_ANSWER) -> str:
    return f'{invalid_text}\n\n{last_message}'


def get_start_message() -> str:
    return f'{START_MESSAGE}!\n\n{ENTER_TEAM_ID}'


def get_after_login_message(user_name: str) -> str:
    return f'Welcome {user_name}!\nPlease choose one your leagues:'


def get_data_dict_as_message(selected_league: str, action: str, gameweek_number: str,
                             data_dict: dict[str, Union[int, str]]) -> str:
    action_subject: str = action.split(' ')[1]
    data_dict_message: str = f'*{selected_league} {action_subject} - {gameweek_number}:*\n'
    for item in data_dict.keys():
        data_dict_message += f'\n{item} - {data_dict[item]}'

    data_dict_message += '\n\n🦁⚽🏆'
    return data_dict_message
