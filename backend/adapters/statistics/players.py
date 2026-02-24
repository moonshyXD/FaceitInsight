from entities.DTO import PlayerHistory, MatchStats


class PlayerStatistics:
    @classmethod
    def get_player_history(
        cls, json_data: dict, nickname: str, player_id: str
    ) -> PlayerHistory:
        items = json_data.get("items", [])
        if not items:
            return cls._create_empty_player(nickname, player_id)

        clean_matches = []
        totals = {
            "kills": 0,
            "kd": 0.0,
            "wins": 0,
            "hs_percent": 0,
            "double": 0,
            "triple": 0,
            "quadro": 0,
            "penta": 0,
        }

        for item in items:
            match = cls._create_match_stats(item)
            clean_matches.append(match)

            totals["kills"] += match.kills
            totals["kd"] += match.kd_ratio
            totals["hs_percent"] += match.hs_percent
            totals["double"] += match.double_kills
            totals["triple"] += match.triple_kills
            totals["quadro"] += match.quadro_kills
            totals["penta"] += match.penta_kills
            if match.result:
                totals["wins"] += 1

        totals["count"] = len(clean_matches)
        totals["clean_matches"] = clean_matches
        player = cls._create_player(nickname, player_id, totals)
        return player

    @staticmethod
    def _create_match_stats(item: dict) -> MatchStats:
        stats = item.get("stats", {})
        return MatchStats(
            map_name=stats.get("Map", "Unknown"),
            score=stats.get("Score", "0 / 0"),
            result=(stats.get("Result") == "1"),
            date=item.get("match_finished_at", 0),
            kills=int(stats.get("Kills", 0)),
            deaths=int(stats.get("Deaths", 0)),
            kd_ratio=float(stats.get("K/D Ratio", 0.0)),
            hs_percent=int(stats.get("Headshots %", 0)),
            double_kills=int(stats.get("Double Kills", 0)),
            triple_kills=int(stats.get("Triple Kills", 0)),
            quadro_kills=int(stats.get("Quadro Kills", 0)),
            penta_kills=int(stats.get("Penta Kills", 0)),
        )

    @staticmethod
    def _create_empty_player(nickname: str, player_id: str) -> PlayerHistory:
        return PlayerHistory(
            nickname=nickname,
            player_id=player_id,
            matches=[],
            avg_kd=0.0,
            avg_kills=0.0,
            winrate=0,
            hs_percent=0,
            double_kills=0.0,
            triple_kills=0.0,
            quadro_kills=0.0,
            penta_kills=0.0,
        )

    @staticmethod
    def _create_player(nickname: str, player_id: str, totals: dict):
        return PlayerHistory(
            nickname=nickname,
            player_id=player_id,
            matches=totals["clean_matches"],
            avg_kd=round(totals["kd"] / totals["count"], 2),
            avg_kills=round(totals["kills"] / totals["count"], 1),
            winrate=int((totals["wins"] / totals["count"]) * 100),
            hs_percent=int(totals["hs_percent"] / totals["count"]),
            double_kills=round(totals["double"] / totals["count"], 2),
            triple_kills=round(totals["triple"] / totals["count"], 2),
            quadro_kills=round(totals["quadro"] / totals["count"], 2),
            penta_kills=round(totals["penta"] / totals["count"], 2),
        )
