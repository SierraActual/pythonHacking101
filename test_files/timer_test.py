import time
import os

def timer_warning(duration, warning_times):
    time.sleep(duration)  # Sleep for the specified duration

    # Iterate over the warning times and print the warnings
    for warning_time in warning_times:
        time_left = duration - warning_time
        time.sleep(time_left)
        print(f"Warning: {warning_time} minutes left!")

    # Final warning when 5 minutes are left
    time.sleep(5)
    print("Warning: 5 minutes left!")

if __name__ == "__main__":
    # Define the total duration of the timer in seconds (2 hours = 7200 seconds)
    total_duration = 35

    # Define the warning times in seconds (30 minutes = 1800 seconds, 20 minutes = 1200 seconds, 10 minutes = 600 seconds)
    warning_times = [30, 20, 10]

    # Start the timer in the background
    os.system(f"python -c 'import sys; import time; time.sleep({total_duration}); sys.exit(0)' &")

    # Call the timer_warning function
    timer_warning(total_duration, warning_times)
