import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.utils.config_loader import load_setting

setting = load_setting()

def random_commit():
    lower_range = setting['randomizer'].get('min_commits',2)
    upper_range = setting['randomizer'].get('max_commits',10)
    return random.randint(lower_range,upper_range)

def random_timeframe():
    timeframe_range = setting['randomizer'].get('timeframe_hours',6)
    min_timeframe = setting['randomizer'].get('min_delay',10)
    max_timeframe = timeframe_range*60
    n_commit = random_commit()
    commit_items = sorted([random.randint(min_timeframe,max_timeframe) for _ in range(n_commit)])
    return commit_items

