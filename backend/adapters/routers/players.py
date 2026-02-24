from fastapi import APIRouter
from entities.DTO import PlayerHistory
from usecases.faceit_finder import FaceitFinder
from adapters.statistics.players import PlayerStatistics

router = APIRouter(prefix="/players", tags=["Players"])


@router.get(path="/statistics", response_model=PlayerHistory)
def get_player_stats(nickname: str):
    player_id = FaceitFinder.find_id_by_name(nickname)
    data = FaceitFinder.find_stat_by_id(player_id)
    player_stats = PlayerStatistics.get_player_history(data, nickname, player_id)
    return player_stats
