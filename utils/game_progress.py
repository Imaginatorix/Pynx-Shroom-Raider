import os
# == LEVEL DIRECTORY == 
LEVEL_DIRECTORY = "levels"

# == SEASONS IN LEVEL == 
SEASONS = ["spring", "summer", "fall", "winter", "temple"]


# == GET THE NEXT STAGE == 
def get_next_stage(season, current_stage):

    # Get the seasons from level directory
    seasons = os.path.join(LEVEL_DIRECTORY, season)

    # == SORTED OUT THE STAGES WITH .txt FILE ONLY == 
    stages = sorted(
    f for f in os.listdir(seasons)
    if os.path.isfile(os.path.join(seasons, f)) and f.endswith(".txt"))

    # Get the index of the current stage 
    if current_stage in stages:
        stage_number = stages.index(current_stage)
    else:
        stage_number = -1

    # Return the season and stage number of the current stage
    if stage_number + 1 < len(stages):
        return season, stages[stage_number + 1]
    
    # if no more stages left, then proceed to the next season
    else:
        # Get the index of the next season 
        next_season_index = SEASONS.index(season) + 1

        # Update the the next season
        if next_season_index < len(SEASONS):
            next_season = SEASONS[next_season_index]
            
            # == SORTED OUT THE NEXT STAGES WITH .txt FILE ONLY == 
            next_stage = sorted(
                f for f in os.listdir(os.path.join(LEVEL_DIRECTORY, next_season))
                if os.path.isfile(os.path.join(LEVEL_DIRECTORY, next_season, f))
                and f.endswith(".txt"))[0]
            return next_season, next_stage
        else:
            return None, None


# == SHROOM LEVEL PARSER == 
def shroom_level_parser_generator(current_level_path = "levels/spring/stage1.txt"):

    # Split the folder path
    folders = os.path.normpath(current_level_path).split(os.sep)
    
    # Get the current season 
    season = folders[-2]

    # Get the current stage number
    current_stage = folders[-1]

    # == GENERATE THE NEXT LEVEL == 
    while True:
        # Get the next season and next stage
        next_season, next_stage = get_next_stage(season, current_stage)

        # If there's nothing left to return - break
        if not next_season or not next_stage:
            break

        # Create the path for the next level
        next_level_path = os.path.join(LEVEL_DIRECTORY, next_season, next_stage)
        yield next_level_path

        # Then update the season and current stage
        season, current_stage = next_season, next_stage


# current = "levels/spring/stage6.txt"
# next_l = shroom_level_parser_generator(current)
# print(next(next_l))
