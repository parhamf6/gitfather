import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.core.randomizer import random_timeframe

times = random_timeframe()
print("Commit will be made at these random times (in minutes):", times)