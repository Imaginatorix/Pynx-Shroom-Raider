import os

SEASONS = ["spring", "summer", "fall"]
PROGRESS_FILE = "progress.txt"


def progress():
    if not os.path.exists(PROGRESS_FILE):
        return SEASONS[0], "stage1.txt"  
    with open(PROGRESS_FILE, "r") as file:
        season, stage = file.read().strip().split(",")
    return season, stage


def save_progress(season, stage):
    with open(PROGRESS_FILE, "w") as f:
        f.write(f"{season},{stage}")


def get_next_stage(season, current_stage):
    stage_files = sorted(os.listdir(os.path.join("levels", season)))
    if current_stage in stage_files:
        stage_number = stage_files.index(current_stage)
    else:
        stage_number = -1

 
    if stage_number + 1 < len(stage_files):
    
        return season, stage_files[stage_number + 1]
    else:
        
        next_season_stage = SEASONS.index(season) + 1
        if next_season_stage < len(SEASONS):
            next_season = SEASONS[next_season_stage]
            next_stage = sorted(os.listdir(os.path.join("levels", next_season)))[0]
            return next_season, next_stage
        else:
            return SEASONS[0], "stage1.txt"  

    return get_next_stage(season, current_stage)