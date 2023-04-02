import json
from urllib import request

import numpy as np

from src.utils.custom_exceptions import InvalidUserID


class FPLUser:
    def __init__(self, manager_id):
        self.user_fullname = ''
        self.user_overall_pts = np.nan
        self.user_overall_rank = np.nan
        self.user_leagues = []
        self.current_gameweek: int = np.nan
        try:
            self.login(manager_id)
        except Exception:
            raise InvalidUserID("Invalid user ID or this user doesn't exist")

    def login(self, manager_id) -> None:
        url = f'https://fantasy.premierleague.com/api/entry/{manager_id}/'
        page = request.urlopen(url)
        data = json.load(page)
        self.user_fullname = f'{data["player_first_name"]} {data["player_last_name"]}'
        self.user_overall_pts = data['summary_overall_points']
        self.user_overall_rank = data['summary_overall_rank']
        self.user_leagues = data['leagues']['classic']
        self.current_gameweek = data['current_event']
