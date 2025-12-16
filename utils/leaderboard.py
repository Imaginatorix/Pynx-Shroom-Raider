"""Utilities for managing and displaying level-based leaderboards.

This module provides data structures and helper functions to:
- Track player scores per level.
- Load and save leaderboard data to JSON files.
- Display leaderboards in the terminal with highlighted current player.
- Prompt for player names and update scores.

Classes
-------
LevelLeaderboard
    Represents the leaderboard for a single level, storing player scores.

LevelLeaderboardData
    Container for all level leaderboards, with methods to load from
    JSON or initialize from a dictionary.

Functions
---------
clear()
    Clears the terminal screen.

retrieve_username(players_name: str = "") -> str
    Prompts the user for their name if not provided.

showleaderboard(filename: str, name: str = "") -> LevelLeaderboardData
    Displays the top 10 leaderboard entries for each level, highlighting
    the current player.

updateleaderboard(filename: str, move_count: int, name: str = "") -> LevelLeaderboardData
    Updates the leaderboard with a new score for a player, saves it to
    JSON, and displays the updated leaderboard.
"""

import json
import os
from dataclasses import dataclass, asdict
from colorama import Style, Fore, init


def clear():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


init(autoreset=True)


@dataclass
class LevelLeaderboard:
    """Represents a leaderboard for a level.

     Attributes
     ----------
        level_stage : str
            Name or identifier of the level.
        scores : dict
            Mapping of player names to their score/move count.
    """
    level_stage: str
    scores: dict


@dataclass
class LevelLeaderboardData:
    """Container for all level leaderboards.

    Attributes
    ----------
        levels : dict
            Mapping of level names to LevelLeaderboard instances.
    """
    levels: dict

    def __init__(self, levels: dict = {}):
        """Initialize LevelLeaderboardData with optional level data.

        Paramater:
            levels : (dict, optional)
                Dictionary of level leaderboards. Defaults to empty dict.
        """
        self.levels = levels or {}

    @classmethod
    def initial_data(cls, leaderboard_data: dict = {}) -> "LevelLeaderboardData":
        """Create LevelLeaderboardData from a dictionary of leaderboard info.

        Parameter
        ----------
            leaderboard_data : (dict, optional)
                Dictionary where keys are level names and values are
                dictionaries containing 'scores'. Defaults to None.

        Returns
        -------
            LevelLeaderboardData:
                Initialized leaderboard data object.
        """

        levels = {}
        if leaderboard_data:
            for _level, scores_obj in leaderboard_data.items():
                scores = scores_obj.get("scores", {})
                levels[_level] = LevelLeaderboard(_level, scores)
        return cls(levels)

    @classmethod
    def leaderboard_from_json(cls, json_data: str) -> "LevelLeaderboardData":
        """Load leaderboard data from a JSON string.

        Parameter
        ---------
            json_data : str
                JSON-formatted string representing leaderboard data.

        Returns
        -------
            LevelLeaderboardData:
                Loaded leaderboard data object.
        """
        data = json.loads(json_data)
        levels = {}
        for level_name, level_obj in data.get("levels", {}).items():
            scores = level_obj.get("scores", {})
            levels[level_name] = LevelLeaderboard(level_name, scores)
        return cls(levels)

    def leaderboard_to_json(self) -> str:
        """Convert all level leaderboard data to JSON.

        Returns
        -------
            str:
                JSON-formatted string of all leaderboard data.
        """
        return json.dumps(asdict(self), indent=2)


def retrieve_username(players_name: str = "") -> str:
    """Prompt the user to enter their name if not provided.

    Parameter
    ---------
        players_name : (str, optional)
            Pre-filled player name. Defaults to "".

    Returns
    -------
        str:
            Validated player name.
    """
    while not players_name:
        players_name = input("Enter your name: ").strip()
        if not players_name:
            print("Invalid player name.")
    return players_name


def showleaderboard(filename: str, name: str = "") -> LevelLeaderboardData:
    """Display the top 10 leaderboard entries for each level.

    -Loads the leaderboard from a JSON file
    -prints the formatted top 10 scores for each level
    -highlights the current player.

    Parameter
    ---------
        filename : str
            Base filename of the leaderboard (without .json extension).
        name : (str, optional)
            Player name to highlight. If empty, user is prompted.

    Returns
    -------
        LevelLeaderboardData:
            The loaded leaderboard data.
    """
    _filename = f"{filename}.json"
    current_player = retrieve_username(name)

    try:
        with open(_filename, "r") as f:
            json_data = f.read()
        leaderboard = LevelLeaderboardData.leaderboard_from_json(json_data)
    except FileNotFoundError:
        leaderboard = LevelLeaderboardData()

    if not leaderboard.levels:

        return leaderboard

    clear()
    for level_name, level in leaderboard.levels.items():
        leaderboard.levels[level_name] = level
        formatted_level = level_name.replace("/", " ").upper()
        print(f"{Style.BRIGHT}\n{formatted_level} Leaderboard Top 10")
        print(Style.BRIGHT + Fore.RED + "-" * 40)

        sorted_scores = sorted(level.scores.items(), key=lambda x: x[1])
        for rank, (user, moves) in enumerate(sorted_scores[:10], start=1):
            suffix = (f"{Style.BRIGHT}(you){Style.RESET_ALL}" if current_player and user == current_player else "")
            print(f"{rank}: {user} - {moves} moves{suffix}")

        print(Style.BRIGHT + Fore.RED + "-" * 40)

    return leaderboard


def updateleaderboard(filename: str,
                      move_count: int,
                      name: str = "") -> LevelLeaderboardData:
    """Update the leaderboard for a given level and save to JSON.

    -Loads the existing leaderboard
    -updates the score for the current player
    -saves the updated leaderboard
    -displays the new leaderboard.

    Parameter
    ---------
        filename : str
            Base filename of the leaderboard (without .json extension).
        move_count : int
            Player's move count for the level.
        name : str, optional
            Player name. If empty, user is prompted.

    Returns
    -------
        LevelLeaderboardData: Updated leaderboard data.
    """

    json_filename = f"{filename}.json"
    level_name = filename

    players_name = retrieve_username(name)

    leaderboard = showleaderboard(filename, name=players_name)
    if level_name not in leaderboard.levels:
        leaderboard.levels[level_name] = LevelLeaderboard(level_name, {})

    # Update score
    leaderboard.levels[level_name].scores[players_name] = move_count
    # Save
    with open(json_filename, "w") as f:
        f.write(leaderboard.leaderboard_to_json())

    leaderboard = showleaderboard(filename, name=players_name)
    print(f"{Fore.GREEN}{Style.BRIGHT}Congratulations, {players_name}!")

    return leaderboard
