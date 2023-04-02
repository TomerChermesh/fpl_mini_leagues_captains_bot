from typing import Union

from src.fpl.fpl_functions import FPLFunctions


class FPLMain:
    main_functions: list[str] = ['get_league_captains', 'get_league_chips']
    menus: list[str] = ['Main menu', 'Leagues menu', 'Exit']

    def __init__(self):
        self.username: str = ''
        self.fpl_functions = FPLFunctions.get_instance()

    def login(self, manager_id: str) -> None:
        self.fpl_functions.connect(manager_id)
        self.username = self.fpl_functions.logged_in_user.user_fullname

    def get_user_private_leagues_names(self) -> list[str]:
        return [league['name'] for league in self.fpl_functions.user_leagues_dict]

    def get_current_gameweek(self) -> int:
        return self.fpl_functions.get_current_gameweek()

    def get_league_data_by_function(self, league_name: str, selected_gameweek: str,
                                    action: str) -> dict[str, Union[str, int]]:
        action_subject: str = action.replace(' ', '_')
        gameweek_number: int = int(selected_gameweek[2:])
        action_to_do = getattr(self.fpl_functions, action_subject)
        data_dict: dict[str, Union[str, int]] = action_to_do(league_name, gameweek_number)
        return data_dict
