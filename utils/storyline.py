import os
import colorama
from utils.parser import parse_level
from colorama import Fore, Back, Style

colorama.init(autoreset=True)

def get_season_from_path(path):
    parts = os.path.normpath(path).split(os.sep)

    for part in parts:
        if part.lower() in ("spring", "summer", "fall"):
            return part.lower()
    return

def storyline(path):
    mission_brief = (
        # f"{Style.BRIGHT}Mission Brief:",
        # "Laro’s grandmother is gravely ill.",
        # "To save her, you must help Laro collect the rare mushrooms",
        # "needed to make the legendary 𝐌𝐈𝐆𝐇𝐓𝐘 𝐂𝐎𝐍𝐂𝐎𝐂𝐓𝐈𝐎𝐍.",
        # "",
        )

    storylines = {
        "spring": (
            # f"{Fore.MAGENTA}Welcome to the Spring Season! The Beginning of the Journey", 
            # "After setting off from his Lola’s humble bahay-kubo, Laro",
            # "arrives at the Springlands of Kalikasan . The first realm in",
            # "his journey toward crafting the Mighty Concoction. The air here",
            # "is fresh and full of life, but danger hides beneath its life.",
            # "",
            ),

        "summer": (
            # f"{Fore.MAGENTA}Welcome to the Summer Season! The Trial of Heat",
            # "After surviving the gentle bloom of Spring, Laro now steps",
            # "into the scorching Sunfields of Kalikasan. A vast, blazing ",
            # "realm where the earth cracks under the relentless heat of the",
            # "sun. The once-cool breeze has turned into waves of warmth, and ",
            # "every step tests his endurance.",
            # "",
            ),

        "fall": (
            # f"{Fore.MAGENTA}Welcome to the Fall Season! The Whisper of Change",
            # "After enduring the scorching trials of Summer, Laro ",
            # "now dives into the Amber Woods of Kalikasan. A realm",
            # "cloaked in golden leaves and drifting winds. The once-vibrant",
            # "land of life and fire has grown quiet, its warmth fading into a ",
            # "",
            ),
        }

    season = get_season_from_path(path)

    if season in storylines:
        selected_storyline = storylines[season] + mission_brief
    return selected_storyline
        