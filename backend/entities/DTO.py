from dataclasses import dataclass


@dataclass(frozen=True)
class MatchStats:
    map_name: str
    score: str
    kills: int
    deaths: int
    kd_ratio: float
    hs_percent: int
    result: bool
    date: str
    double_kills: float
    triple_kills: float
    quadro_kills: float
    penta_kills: float


@dataclass(frozen=True)
class PlayerHistory:
    nickname: str
    player_id: str
    matches: list[MatchStats]
    avg_kd: float
    avg_kills: float
    winrate: int
    hs_percent: float
    double_kills: float
    triple_kills: float
    quadro_kills: float
    penta_kills: float
