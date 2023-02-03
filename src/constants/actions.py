from typing import Final


ACTION_SELECTION: Final[str] = 'Action Selection'
GAMEWEEK_SELECTION: Final[str] = 'Gameweek Selection'
LEAGUE_SELECTION: Final[str] = 'League Selection'
MAIN_ACTIONS: Final[list[str]] = ['Get Captains', 'Get Chips']
CURRENT_GAMEWEEK: Final[int] = 22

MENUS: Final[list[str]] = [ACTION_SELECTION, GAMEWEEK_SELECTION, LEAGUE_SELECTION]


def get_menus_with_exit() -> list[str]:
    menus_with_exit: list[str] = MENUS.copy()
    menus_with_exit.append('Exit')
    return menus_with_exit


def all_valid_string_messages(user_leagues_names: list[str]) -> list[str]:
    all_return_to_menus: list[str] = get_all_return_to_menus()
    gameweeks: list[str] = get_all_relevant_gameweeks_names()
    return user_leagues_names + MAIN_ACTIONS + gameweeks + all_return_to_menus


def get_all_relevant_gameweeks_names() -> list[str]:
    return [f'GW{gw_num + 1}' for gw_num in range(CURRENT_GAMEWEEK)]


def get_all_return_to_menus() -> list[str]:
    return get_menus_with_exit()