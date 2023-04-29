import json
import threading
from typing import Union, Any
from urllib import request

from src.fpl.fpl_user import FPLUser


class FPLFunctions:
    _instance = None
    _lock: threading.Lock = threading.Lock()
    logged_in_user: FPLUser
    elements: dict
    captains: dict[str, int]
    vice_captains: dict[str, int]
    chips: dict[str, int]
    scores: dict[str, int]
    user_leagues_dict: dict

    def __init__(self):
        raise RuntimeError("Call getInstance method instead")

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = cls.__new__(cls)
                    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
                    page = request.urlopen(url)
                    cls._instance.data = json.load(page)
                    cls._instance.elements = cls._instance.data["elements"]
                    cls._instance.captains = {}
                    cls._instance.vice_captains = {}
                    cls._instance.chips = {}
                    cls._instance.logged_in_user = None
                    cls._instance.user_leagues_dict = {}
                    return cls._instance
        else:
            return cls._instance

    def connect(self, manager_id) -> None:
        try:
            self.logged_in_user = FPLUser(manager_id)
            self.user_leagues_dict = self.logged_in_user.leagues[4:]
        except IOError as ex:
            raise IOError(str(ex))

    @staticmethod
    def get_player_first_name(player: dict[str, Any]) -> str:
        player_first_name = player["first_name"]
        return player_first_name

    @staticmethod
    def get_player_last_name(player: dict[str, Any]) -> str:
        player_last_name = player["second_name"]
        return player_last_name

    @staticmethod
    def get_league(league_id: int) -> dict[str, Any]:
        url = f'https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings'
        page = request.urlopen(url)
        return json.load(page)

    @staticmethod
    def get_fpl_team_picks_by_gw(team_id: int, gw_number: int) -> dict[str, Any]:
        url = f'https://fantasy.premierleague.com/api/entry/{team_id}/event/{gw_number}/picks/'
        page = request.urlopen(url)
        return json.load(page)

    @staticmethod
    def get_fpl_team_history(team_id: int) -> dict[str, Any]:
        url = f'https://fantasy.premierleague.com/api/entry/{team_id}/history/'
        page = request.urlopen(url)
        return json.load(page)

    def get_player(self, player_id: int) -> dict[str, Any]:
        for player in self.elements:
            if player["id"] == player_id:
                return player

    def get_player_name(self, player_id: int) -> str:
        player = self.get_player(player_id)
        player_name = self.get_player_last_name(player)

        if player_name[0].islower():
            player_name = self.get_player_first_name(player)

        return player_name

    def get_fpl_team_captain(self, team_id: int, gw_number: int) -> str:
        gw_team_data = {}
        captain_name: str = ''

        gw_team_data.update(self.get_fpl_team_picks_by_gw(team_id, gw_number))

        for player_picked in gw_team_data["picks"]:
            player_id = player_picked["element"]
            is_captain = player_picked["is_captain"]
            multiplier = player_picked['multiplier']

            if is_captain:
                captain_name = self.get_player_name(player_id)
                if multiplier == 3:
                    captain_name += ' (Triple)'

        return captain_name

    def get_fpl_team_vice_captain(self, team_id: int, gw_number: int) -> str:
        gw_team_data = {}
        captain_name: str = ''
        vice_captain_name: str = ''

        gw_team_data.update(self.get_fpl_team_picks_by_gw(team_id, gw_number))

        for player_picked in gw_team_data["picks"]:
            player_id = player_picked["element"]
            is_captain = player_picked["is_captain"]
            is_vice_captain = player_picked["is_vice_captain"]
            multiplier = player_picked['multiplier']

            if is_captain:
                captain_name = self.get_player_name(player_id)
                if multiplier == 3:
                    captain_name += ' (Triple)'
            elif is_vice_captain:
                vice_captain_name = self.get_player_name(player_id)

        full_vice_captain_record: str = f'{captain_name} ({vice_captain_name})'

        return full_vice_captain_record

    def get_captains(self, league_name: str, gw_number: int) -> dict[str, Union[str, int]]:
        self.captains = {}
        league_id: int = [league['id'] for league in self.user_leagues_dict if league['name'] == league_name][0]
        data = self.get_league(league_id)

        for team in data["standings"]["results"]:
            captain = self.get_fpl_team_captain(team["entry"], gw_number)
            self.count_captain(captain)

        sorted_captains: dict[str, int] = dict(sorted(self.captains.items(), key=lambda item: item[1], reverse=True))
        return sorted_captains

    def get_captains_with_vices(self, league_name: str, gw_number: int) -> dict[str, Union[str, int]]:
        self.vice_captains = {}
        league_id: int = [league['id'] for league in self.user_leagues_dict if league['name'] == league_name][0]
        data = self.get_league(league_id)

        for team in data["standings"]["results"]:
            vice_captain = self.get_fpl_team_vice_captain(team["entry"], gw_number)
            self.count_vice_captain(vice_captain)

        sorted_vice_captains: dict[str, int] = dict(sorted(self.vice_captains.items(), key=lambda item: item[1],
                                                      reverse=True))
        return sorted_vice_captains

    def get_chips(self, league_name: str, gw_number: int) -> dict[str, Union[str, int]]:
        self.chips = {}
        league_id: int = [league['id'] for league in self.user_leagues_dict if league['name'] == league_name][0]
        data = self.get_league(league_id)

        for team in data["standings"]["results"]:
            chip = self.get_fpl_team_picks_by_gw(team["entry"], gw_number)['active_chip']
            if chip:
                self.count_chips(chip)

        sorted_chips: dict[str, int] = dict(sorted(self.chips.items(), key=lambda item: item[1], reverse=True))
        return sorted_chips

    def get_gameweek_winners(self, league_name: str, gw_number: int) -> dict[str, Union[str, int]]:
        self.scores = {}
        league_id: int = [league['id'] for league in self.user_leagues_dict if league['name'] == league_name][0]
        data = self.get_league(league_id)

        for team in data["standings"]["results"]:
            self.scores[f'{team["entry_name"]} ({team["player_name"]})'] = \
                self.get_gameweek_points(team['entry'], gw_number)

        sorted_scores: dict[str, int] = dict(sorted(self.scores.items(), key=lambda item: item[1], reverse=True))
        gw_podium: dict[str, int] = dict(zip(list(sorted_scores.keys())[:3], list(sorted_scores.values())[:3]))
        return gw_podium

    def get_gameweek_points(self, team_id: int, gw_number: int) -> int:
        this_season_team_history: list[dict[str, int]] = self.get_fpl_team_history(team_id)['current']
        gw_points: int = list(filter(lambda x: x['event'] == gw_number, this_season_team_history))[0]['points']
        return gw_points

    def count_captain(self, captain: str) -> None:
        if captain not in self.captains:
            self.captains[captain] = 1
        else:
            self.captains[captain] += 1

    def count_vice_captain(self, vice_captain: str) -> None:
        if vice_captain not in self.vice_captains:
            self.vice_captains[vice_captain] = 1
        else:
            self.vice_captains[vice_captain] += 1

    def count_chips(self, chip: str) -> None:
        if chip not in self.chips:
            self.chips[chip] = 1
        else:
            self.chips[chip] += 1

    def get_manager_info(self) -> FPLUser:
        return self.logged_in_user

    def get_current_gameweek(self) -> int:
        user: FPLUser = self.get_manager_info()
        return user.current_gameweek
