import os
import colorama
from utils.parser import parse_level
from colorama import Fore, Back, Style

colorama.init(autoreset=True)

def get_season_from_path(path):
    parts = os.path.normpath(path).split(os.sep)

    for part in parts:
        if part.lower() in ("spring", "summer", "fall", "winter", "temple"):
            return part.lower()
    return

def storyline(path):
    mission_brief = (
         f"{Style.BRIGHT}Mission Brief:",
         "Laro’s grandmother is gravely ill.",
         "To save her, you must help Laro collect the rare mushrooms",
         "needed to make the legendary 𝐌𝐈𝐆𝐇𝐓𝐘 𝐂𝐎𝐍𝐂𝐎𝐂𝐓𝐈𝐎𝐍.",
         "",
        )

    storylines = {
        "spring": (
            f"{Fore.GREEN}Welcome to the Spring Season! The Beginning of the Journey", 
            "Laro arrives at the Springlands of Kalikasan .",
            ),

        "summer": (
            f"{Fore.MAGENTA}Welcome to the Summer Season! The Trial of Heat",
            "Laro now steps into the scorching Sunfields of Kalikasan.",
            "",
            ),

        "fall": (
            f"{Fore.BLUE}Welcome to the Fall Season! The Whisper of Change",
            "Laro now dives into the Amber Woods of Kalikasan.",
            "",
            ),

        "winter": (
            f"{Fore.CYAN}Welcome to the Winter Season! The cold never bothered Laro anyway.",
            "Laro now steps into the Frosted Kalikasan. It might be caused by someone...",
            "",),

        "temple": (
            f"{Fore.RED}{Style.BRIGHT}Welcome to the Final Stage: THE TEMPLE!",
            "Laro now ascends to a sacred temple",
            ),

        }

    season = get_season_from_path(path)

    if season in storylines:
        selected_storyline = storylines[season] + mission_brief
    return selected_storyline
        