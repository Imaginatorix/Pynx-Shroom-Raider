import colorama
import json
import os
import survey
import sys
from colorama import Fore, Style
from dacite import from_dict
from dataclasses import dataclass, asdict
from firebase_admin import credentials, db, initialize_app


if os.name == 'nt':
    import msvcrt
else:
    import termios

def clear():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def input_clear():
    if os.name == 'nt':
        while msvcrt.kbhit():
            msvcrt.getch()
    else:
        termios.tcflush(sys.stdin, termios.TCIFLUSH)



@dataclass
class RankLeaderboard:
    """Represents a rank leaderboard based on points.

    Attributes
    ----------
        scores : dict[str, int]
            Mapping of usernames to their rank points.
    """
    scores: dict[str, int]  # username -> rank points

    @classmethod
    def initial_data(cls, leaderboard_data: dict[str, int] | None):
        """Create a RankLeaderboard instance from initial dictionary data.

        Paramaters
        ----------
            leaderboard_data (dict[str, int] | None): Raw scores data.

        Returns
        -------
            RankLeaderboard: Initialized leaderboard object.
        """
        return cls(scores=leaderboard_data or {})

    def leaderboard_to_json(self) -> str:
        """Convert the leaderboard to a JSON string.

        Returns
        -------
            str: JSON-formatted leaderboard.
        """
        return json.dumps(asdict(self), indent=2)



    @classmethod
    def leaderboard_from_json(cls, json_data: str) -> "RankLeaderboard":
        """Create a RankLeaderboard instance from a JSON string.

        Paramaters
        ----------
            json_data : str
                JSON-formatted leaderboard string.

        Returns
        -------
            RankLeaderboard: Initialized leaderboard object.
        """
        data = json.loads(json_data)
        return from_dict(cls, data)


colorama.init(autoreset=True)
def rank_leaderboard(username: str, reference):
    """Display the top-ranked users in the rank leaderboard.

    Get leaderboard data from a reference (firebase), sorts it,
    and prints the top 10 users with their points. Highlights the current user.

    Paramaters
    ----------
        username : str
            Current user's username.
        reference: 
            Data reference object with a `.child().get()` method.
    """
    clear()
    leaderboard_data = reference.child("rank_leaderboard").get() or {}
    leaderboard = RankLeaderboard.initial_data(leaderboard_data)

    sorted_scores = sorted(
        leaderboard.scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    print("Highest Ranks")
    for i, (user, points) in enumerate(sorted_scores[:10], start=1):
        suffix = Style.BRIGHT + " (you)" if user == username else ""
        print(f"{i}: {user} with {points} points{suffix}")

    input_clear()
    survey.routines.select(
        "",
        options=[f"{'Return':<10}| Go back to online battle menu"],
        focus_mark="> ",
        evade_color=survey.colors.basic('yellow')
    )


@dataclass
class LevelLeaderboard:
    """Represents a leaderboard for a single level.

    Attributes
    ----------
        level_name : str 
            Name of the level.
        scores : dict[str, int] 
            Mapping of usernames to moves taken.
    """
    level_name: str
    scores: dict[str, int]  # username mapped to moves


@dataclass
class LevelLeaderboardData:
    """Holds leaderboard data for multiple levels.

    Attributes
    ----------
        levels : dict[str, LevelLeaderboard] 
            Mapping of level names to LevelLeaderboard objects.
    """
    levels: dict[str, LevelLeaderboard]

    def __init__(self, levels: dict[str, LevelLeaderboard] | None = None):
        """Initialize LevelLeaderboardData with optional levels.

        Paramaters
        ----------
            levels : dict[str, LevelLeaderboard] | None 
                Predefined level data.
        """
        self.levels = levels or {}


    @classmethod
    def initial_data(cls, leaderboard_data: dict) -> "LevelLeaderboardData":
        """Load levels from raw dictionary data.

        Paramaters
        ----------
            leaderboard_data : dict 
                initial leaderboard data.

        Returns
        -------
            LevelLeaderboardData: 
                Player completed levels
        """
        levels = {
            level_name: LevelLeaderboard(level_name, scores)
            for level_name, scores in (leaderboard_data or {}).items()
        }
        return cls(levels)

    def leaderboard_to_json(self) -> str:
        """Convert all level leaderboard data to JSON.

        Returns
        -------
            str: JSON-formatted leaderboard data.
        """
        return json.dumps(asdict(self), indent=2)

    def leaderboard_from_json(self, json_data: str) -> "LevelLeaderboardData":
        """Load LevelLeaderboardData from a JSON string.

        Paramaters
        ----------
            json_data : str
                JSON-formatted leaderboard data.

        Returns
        -------
            LevelLeaderboardData: 
                Player completed levels.
        """
        data = json.loads(json_data)
        obj = from_dict(LevelLeaderboardData, data)
        self.levels = obj.levels
        return self


def level_leaderboard(username: str, reference):
    """Display move-based leaderboards for individual levels.

    Allows the user to select a level and see the top 10 scores. Highlights
    the current user and provides navigation options.

    Paramaters
    ----------
        username : str 
            Current user's username.
        reference : str 
            Data reference object with a `.child().get()` method.
    """
    if username:
        raw_data = reference.child("level_leaderboard").get() or {}
        leaderboard_data = LevelLeaderboardData.initial_data(raw_data)

        while True:
            clear()
            options_list = list(leaderboard_data.levels.keys()) + ["Return to main menu"]
            input_clear()

            chosen_index = survey.routines.select(
                "Choose from the following levels: ",
                options=options_list,
                focus_mark="> ",
                evade_color=survey.colors.basic("yellow")
            )
            chosen_level = options_list[chosen_index]

            if chosen_level == "Return to main menu":
                break

            clear()
            level = leaderboard_data.levels[chosen_level]

            print(f"Moves Leaderboard for {chosen_level}")
            sorted_scores = sorted(level.scores.items(), key=lambda x: x[1])

            for i, (user, moves) in enumerate(sorted_scores[:10], start=1):
                suffix = Style.BRIGHT + " (you)" if user == username else ""
                print(f"{i}: {user} with {moves} moves{suffix}")

            input_clear()
            answer = survey.routines.select(
                "",
                options=["Choose Level | Check another leaderboard", "Return | Go back"],
                focus_mark="> ",
                evade_color=survey.colors.basic("yellow")
            )

            if answer == 1:
                break
    else:
        print("This is only available for logged-in users.")
        survey.routines.select(
            "",
            options=[f"{'Return':<10}| Go back to levels menu"],
            focus_mark="> ",
            evade_color=survey.colors.basic('yellow')
        )
