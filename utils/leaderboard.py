"""Utilities for leaderboard management and display."""

import json
from dataclasses import dataclass, asdict
from dacite import from_dict
from colorama import Style, Fore, init


init(autoreset=True)
@dataclass
class LevelLeaderboard:
    """Represents a leaderboard for a level."""
    level_stage: str
    scores: dict


@dataclass
class LevelLeaderboardData:
    """Holds leaderboard data for levels."""
    levels: dict

    def __init__(self, levels: dict = None):
        self.levels = levels or {}

    @classmethod
    def initial_data(cls, leaderboard_data: dict = None) -> "LevelLeaderboardData":
        """Load levels from a dictionary of level scores."""
        levels = {}
        if leaderboard_data:
            for _level, scores in leaderboard_data.items():
                levels[_level] = LevelLeaderboard(_level, scores)
        return cls(levels)

    @classmethod
    def leaderboard_from_json(cls, json_data: str) -> "LevelLeaderboardData":
        """Load LevelLeaderboardData from a JSON string using dacite."""
        data = json.loads(json_data)
        return from_dict(cls, data)

    def leaderboard_to_json(self) -> str:
        """Convert all level leaderboard data to JSON."""
        return json.dumps(asdict(self), indent=2)


def showleaderboard(filename: str, current_player: str = None) -> LevelLeaderboardData:
    """Load the leaderboard from a JSON file and print top 10 for each level."""
    try:
        with open(filename, "r") as f:
            json_data = f.read()
        leaderboard = LevelLeaderboardData.leaderboard_from_json(json_data)
    except FileNotFoundError:
        leaderboard = LevelLeaderboardData()


    if not leaderboard.levels:
        return leaderboard

    for level_name, level in leaderboard.levels.items():
        # Format 
        formatted_level = level_name.replace("_", " ").upper()
        print(f"\n{formatted_level} Leaderboard Top 10")
        print("-" * 40)

        sorted_scores = sorted(level.scores.items(), key=lambda x: x[1])
        # Print 
        for rank, (user, moves) in enumerate(sorted_scores[:10], start=1):
            suffix = f"{Style.BRIGHT} (you){Style.RESET_ALL}" if user == current_player else ""
            print(f"{rank}: {user} - {moves} moves{suffix}")
        print(Style.BRIGHT + Fore.GREEN + "-" * 40)

    return leaderboard


def updateleaderboard(filename: str, move_count: int, level_name: str, players_name: str):
    leaderboard = showleaderboard(filename)
    if level_name not in leaderboard.levels:
        leaderboard.levels[level_name] = LevelLeaderboard(level_name, {})

    current_score = leaderboard.levels[level_name].scores.get(players_name, float('inf'))
    if move_count < current_score:
        leaderboard.levels[level_name].scores[players_name] = move_count
        with open(filename, "w") as f:
            f.write(leaderboard.leaderboard_to_json())
    else:
        return