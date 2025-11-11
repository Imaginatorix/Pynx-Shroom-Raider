import os

LEVEL_DIRECTORY = "levels"
SEASONS = ["spring", "summer", "fall"]

def get_next_stage(season, current_stage):
    seasons = os.path.join(LEVEL_DIRECTORY, season)
    stages = sorted(os.listdir(seasons))

    if current_stage in stages:
        stage_number = stages.index(current_stage)
    else:
        stage_number = -1

    if stage_number + 1 < len(stages):
        return season, stages[stage_number + 1]
    else:
        next_season_index = SEASONS.index(season) + 1
        if next_season_index < len(SEASONS):
            next_season = SEASONS[next_season_index]
            next_stage = sorted(os.listdir(os.path.join(LEVEL_DIRECTORY, next_season)))[0]
            return next_season, next_stage
        else:
            return None, None


def shroom_level_parser(current_level_path):
    folders = os.path.normpath(current_level_path).split(os.sep)
    season = folders[-2]
    current_stage = folders[-1]
    next_season, next_stage = get_next_stage(season, current_stage)
    if not next_season or not next_stage:
        return None
    next_level_path = os.path.join(LEVEL_DIRECTORY, next_season, next_stage)
    return next_level_path

current_level = "levels/summer/stage2.txt"
next_level = shroom_level_parser(current_level)