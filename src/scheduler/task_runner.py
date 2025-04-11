import random
import schedule
import time
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.utils.config_loader import load_setting
from src.core.git_actions import commit_quote , get_repo




def generate_random_num():
    lower_range = 2
    upper_range = 10
    return random.randint(lower_range,upper_range)

def generate_random_times(num_times, min_minutes=1, max_minutes=15):
    """Generate random minutes within a time range."""
    return sorted(random.sample(range(min_minutes, max_minutes + 1), num_times))

# def task():
#     # commit quote
#     pass



def schedule_tasks(start_hour=18, num_times=4):
    """Schedule tasks at random times within a 6-hour window."""
    # Generate random minutes
    random_minutes = generate_random_times(num_times)
    print(f"Tasks will run at these minute marks after {start_hour}:55: {random_minutes}")
    
    # Calculate actual times
    start_time = datetime.now().replace(hour=start_hour, minute=55, second=0, microsecond=0)
    
    # If start time is in the past, use tomorrow
    if start_time < datetime.now():
        start_time = start_time + timedelta(days=1)
    
    # Schedule each task
    for minutes in random_minutes:
        task_time = start_time + timedelta(minutes=minutes)
        task_time_str = task_time.strftime("%H:%M")
        
        # Schedule the task
        schedule.every().day.at(task_time_str).do(commit_quote, get_repo())
        print(f"Task scheduled for {task_time_str}")

if __name__ == "__main__":
    # Set the start hour (e.g., 9 for 9:00 AM)
    start_hour = 18
    
    # Schedule 3 random times
    schedule_tasks(start_hour, 4)
    
    # Keep the script running to execute scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)