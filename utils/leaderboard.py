"""Utilities for leaderboard management and display."""
import json
import os
from dataclasses import dataclass, asdict
from dacite import from_dict
from colorama import Style, Fore, init


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

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
            for _level, scores_obj in leaderboard_data.items():
                scores = scores_obj.get("scores", {})
                levels[_level] = LevelLeaderboard(_level, scores)
        return cls(levels)


    @classmethod
    def leaderboard_from_json(cls, json_data: str) -> "LevelLeaderboardData":
        data = json.loads(json_data)
        levels = {}
        for level_name, level_obj in data.get("levels", {}).items():
            scores = level_obj.get("scores", {})
            levels[level_name] = LevelLeaderboard(level_name, scores)
        return cls(levels)


    def leaderboard_to_json(self) -> str:
        """Convert all level leaderboard data to JSON."""
        return json.dumps(asdict(self), indent=2)



def showleaderboard(filename: str, name: str = None) -> LevelLeaderboardData:
    """Load the leaderboard from a JSON file and print top 10 for each level."""
    _filename = f"{filename}.json"
    current_player = name or input("Enter your name: ").strip() or None

    try:
        with open(_filename, "r") as f:
            json_data = f.read()
        leaderboard = LevelLeaderboardData.leaderboard_from_json(json_data)
    except FileNotFoundError:
        leaderboard = LevelLeaderboardData()

    if not leaderboard.levels:
        return leaderboard

    for level_name, level in leaderboard.levels.items():
        if isinstance(level, dict):
            level = LevelLeaderboard(level_name, level)
            leaderboard.levels[level_name] = level
            formatted_level = level_name.replace("_", " ").upper()
            print(f"\n{formatted_level} Leaderboard Top 10")
            print("-" * 40)

            sorted_scores = sorted(level.scores.items(), key=lambda x: x[1])
            for rank, (user, moves) in enumerate(sorted_scores[:10], start=1):
                suffix = (f"{Style.BRIGHT} (you){Style.RESET_ALL}" if current_player and user == current_player else "")
                print(f"{rank}: {user} - {moves} moves{suffix}")

            print(Style.BRIGHT + Fore.GREEN + "-" * 40)
        
        clear()
        return leaderboard




def updateleaderboard(filename: str, move_count: int, name: str = None):
    """Update leaderboard for a level."""
    json_filename = f"{filename}.json"
    level_name = filename

    players_name = name or input("Enter your name: ").strip()
    if not players_name:
        print("Invalid player name.")
        return

    leaderboard = showleaderboard(filename)
    if level_name not in leaderboard.levels:
        leaderboard.levels[level_name] = LevelLeaderboard(level_name, {})

    # Update score
    leaderboard.levels[level_name].scores[players_name] = move_count
    # Save 
    with open(json_filename, "w") as f:
        f.write(leaderboard.leaderboard_to_json())

    clear()
    print(f"{Fore.GREEN}{Style.BRIGHT}Congratulations! {players_name}")

