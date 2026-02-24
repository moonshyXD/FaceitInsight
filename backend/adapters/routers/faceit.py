from fastapi import APIRouter
from usecases.faceit_finder import FaceitFinder


router = APIRouter(prefix="/faceit", tags=["Faceit"])


@router.get("/data/{nickname}")
def get_player_data(nickname: str):
    player_id = FaceitFinder.find_id_by_name(nickname)
    data = FaceitFinder.find_data_by_id(player_id)
    return data


@router.get("/stats/{nickname}")
def get_player_all_stats(nickname: str):
    player_id = FaceitFinder.find_id_by_name(nickname)
    data = FaceitFinder.find_stat_by_id(player_id)
    return data


@router.get("/history/{nickname}")
def get_player_20_stats(nickname: str):
    player_id = FaceitFinder.find_id_by_name(nickname)
    data = FaceitFinder.find_20_last_matches(player_id)
    return data
