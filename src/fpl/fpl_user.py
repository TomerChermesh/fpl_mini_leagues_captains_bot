import json
from typing import Any
from urllib import request

from src.utils.custom_exceptions import InvalidUserID


class FPLUser:
    def __init__(self, manager_id):
        self.team_name: str = ''
        self.fullname: str = ''
        self.overall_pts: int = 0
        self.overall_rank: int = 0
        self.leagues: dict[str, Any] = {}
        self.current_gameweek: int = 0
        self.current_gameweek_points: int = 0
        self.current_gameweek_rank: int = 0
        try:
            self.login(manager_id)
        except Exception:
            raise InvalidUserID("Invalid user ID or this user doesn't exist")

    def login(self, manager_id) -> None:
        url = f'https://fantasy.premierleague.com/api/entry/{manager_id}/'
        page = request.urlopen(url)
        data = json.load(page)
        self.team_name = data['name']
        self.fullname = f'{data["player_first_name"]} {data["player_last_name"]}'
        self.overall_pts = data['summary_overall_points']
        self.overall_rank = data['summary_overall_rank']
        self.leagues = data['leagues']['classic']
        self.current_gameweek = data['current_event']
        self.current_gameweek_points = data['summary_event_points']
        self.current_gameweek_rank = data['summary_event_rank']
