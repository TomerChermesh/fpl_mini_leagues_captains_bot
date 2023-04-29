from typing import Final

from src.config import get_config

config = get_config()

EXIT: Final[str] = 'Exit'
START: Final[str] = 'Start'
ACTION_SELECTION: Final[str] = 'Action Selection'
GAMEWEEK_SELECTION: Final[str] = 'Gameweek Selection'
LEAGUE_SELECTION: Final[str] = 'League Selection'
GET_CAPTAINS: Final[str] = 'Get Captains'
GET_CAPTAINS_WITH_VICES: Final[str] = 'Get Captains (with Vices)'
GET_CHIPS: Final[str] = 'Get Chips'
GET_GW_WINNERS: Final[str] = 'Get Gameweek Winners'
MAIN_ACTIONS: Final[list[str]] = [GET_CAPTAINS, GET_CAPTAINS_WITH_VICES, GET_CHIPS, GET_GW_WINNERS]

MENUS: Final[list[str]] = [ACTION_SELECTION, GAMEWEEK_SELECTION, LEAGUE_SELECTION]


def get_translated_action(action: str) -> str:
    if action == GET_CAPTAINS_WITH_VICES:
        action = action.replace('(', '').replace(')', '')

    return action.lower().replace(' ', '_')


def get_menus_with_exit() -> list[str]:
    menus_with_exit: list[str] = MENUS.copy()
    menus_with_exit.append('Exit')
    return menus_with_exit


def get_all_relevant_gameweeks_names(current_gameweek: int) -> list[str]:
    return [f'GW{gw_num}' for gw_num in range(current_gameweek, 0, -1)]


def get_all_return_to_menus() -> list[str]:
    return get_menus_with_exit()
