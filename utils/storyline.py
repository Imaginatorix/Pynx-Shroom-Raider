import os
import colorama
from utils.parser import parse_level
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

# == GET THE STORYLINE OF THE CURRENT SEASON == 
def get_season_from_path(path):
    parts = os.path.normpath(path).split(os.sep)

    for part in parts:
        if part.lower() in ("spring", "summer", "fall", "winter", "temple"):
            return part.lower()
    return


# == STORYLINES OF LEVEL SEASON == 
def storyline(path):
    # == STORYLINES == 
    storylines = {

        # == SPRING SEASON == 
        "spring": (
            f"{Fore.GREEN}Welcome to the Spring Season! The Beginning of the Journey", 
            "Laro arrives at the Springlands of Kalikasan .",
            "",
            ),

        # == SUMMER SEASON == 
        "summer": (
            f"{Fore.MAGENTA}Welcome to the Summer Season! The Trial of Heat",
            "Laro now steps into the scorching Sunfields of Kalikasan.",
            "",
            ),

        # == FALL SEASON == 
        "fall": (
            f"{Fore.BLUE}Welcome to the Fall Season! The Whisper of Change",
            "Laro now dives into the Amber Woods of Kalikasan.",
            "",
            ),

        # == WINTER SEASON == 
        "winter": (
            f"{Fore.CYAN}Welcome to the Winter Season! The cold never bothered Laro anyway.",
            "Laro now steps into the Frosted Kalikasan. It might be caused by someone...",
            "",),

        # == FINAL STAGE : TEMPLE  == 
        "temple": (
            f"{Fore.RED}{Style.BRIGHT}Welcome to the Final Stage: THE TEMPLE!",
            "Laro now ascends to a sacred temple",
            ),

        }

    season = get_season_from_path(path)
    if season in storylines:
        selected_storyline = storylines[season]
    return selected_storyline
        