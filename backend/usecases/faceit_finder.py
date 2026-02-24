from decouple import config
from entities.errors import FaceitError
from usecases.consts import (
    FIND_DATA_BY_ID_URL,
    FIND_ID_BY_NAME_URL,
    FIND_STAT_CS2_URL,
    FIND_20_LAST_MATCHES,
)
import requests


class FaceitFinder:
    HEADERS = {"Authorization": f"Bearer {config('API_KEY')}"}

    @staticmethod
    def find_id_by_name(nickname: str) -> str:
        URL = FIND_ID_BY_NAME_URL + f"{nickname}"
        response = requests.get(URL, headers=FaceitFinder.HEADERS)
        if response.status_code == 200:
            data = response.json()
            return data.get("player_id")
        else:
            raise FaceitError(f"Не получилось найти ID игрока по имени: {nickname}")

    @staticmethod
    def find_data_by_id(player_id: str) -> dict:
        URL = FIND_DATA_BY_ID_URL + f"{player_id}"
        response = requests.get(URL, headers=FaceitFinder.HEADERS)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise FaceitError(
                f"Не получилось найти общие данные игрока по ID: {player_id}"
            )

    @staticmethod
    def find_stat_by_id(player_id: str):
        URL = FIND_DATA_BY_ID_URL + f"{player_id}" + FIND_STAT_CS2_URL
        response = requests.get(URL, headers=FaceitFinder.HEADERS)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise FaceitError(
                f"Ошибка {response.status_code} для ID: {player_id}. {response.text}"
            )

    @staticmethod
    def find_20_last_matches(player_id: int):
        URL = FIND_DATA_BY_ID_URL + f"{player_id}" + FIND_20_LAST_MATCHES
        response = requests.get(URL, headers=FaceitFinder.HEADERS)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise FaceitError(
                f"Ошибка {response.status_code} для поиска последних 20 матчей для ID: {player_id}. {response.text}"
            )
