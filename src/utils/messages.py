from typing import Final, Union

DESCRIPTION: Final[str] = "⚽ Here you can get your mini-league's captaincy & chips easily.\n\n⚽ I'm working only " \
                          "with mini-leagues with 50 managers at most so if your mini-league is bigger that that, " \
                          "you will get the data only for the top 50 teams at your table"
FPL_MINI_LEAGUES_BOT: Final[str] = 'FPL mini-leagues bot'
HELLO: Final[str] = f"*Hello! It's {FPL_MINI_LEAGUES_BOT}* 🦁"
API: Final[str] = "⚽ In order to get your FPL data I'm using the official api. Read more in this guide:\n " \
                  "https://medium.com/@frenzelts/fantasy-premier-league-api-endpoints-a-detailed-guide-acbd5598eb19"
START_COMMAND: Final[str] = f"/start -> Start using {FPL_MINI_LEAGUES_BOT}"
HELP_COMMAND: Final[str] = "/help -> This message"
ABOUT_COMMAND: Final[str] = f"/about -> Read about {FPL_MINI_LEAGUES_BOT}"

ENTER_TEAM_ID: Final[str] = "Now, please enter your FPL team ID 🙏🏼"
GOODBYE: Final[str] = "Thank you! Hope to see you next time 👋🏼"
INVALID_ANSWER: Final[str] = "Invalid answer 😣"
RETURN_TO_MENUS: Final[str] = "Please select a menu to return to or exit 🙏🏼"
SELECT_GAMEWEEK: Final[str] = "Please select a gameweek to get info about 🙏🏼"
SELECT_ACTION: Final[str] = "Please select one of the following actions 🎯"


def get_invalid_message_with_last_message(last_message: str, invalid_text: str = INVALID_ANSWER) -> str:
    return f'{invalid_text}\n\n{last_message}'


def get_about_message() -> str:
    return f'*About {FPL_MINI_LEAGUES_BOT}* 🦁\n\n{DESCRIPTION}!\n\n{API}'


def get_help_message() -> str:
    return f'The following commands are available:\n\n' \
           f'{START_COMMAND}\n' \
           f'{ABOUT_COMMAND}\n' \
           f'{HELP_COMMAND}'


def get_start_message() -> str:
    return f'{HELLO}\n\n{DESCRIPTION}\n\n{ENTER_TEAM_ID}'


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
