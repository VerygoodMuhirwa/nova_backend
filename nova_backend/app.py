import subprocess
import time
import random
import os

# Function to add, commit, and edit the file
def add_commit_edit(limit):
    # Add all files
    subprocess.run(['git', 'add', '.'])

    # Commit with current date in milliseconds
    current_milliseconds = int(time.time() * 1000)
    subprocess.run(['git', 'commit', '-m', f'{current_milliseconds}'])

    # Edit or create the app.txt file
    with open('app.txt', 'a+') as file:
        file.write(f'{current_milliseconds}\n')

    # Generate a random number of days in the past and commit
    random_days = random.randint(1, limit)
    past_date = int(time.time() - 86400 * random_days) * 1000  # Convert days to seconds
    subprocess.run(['git', 'commit', '--date', f'{past_date}', '-am', f'Past commit: {past_date}'])

# Number of iterations
iterations = 5000

# Loop to perform actions multiple times
for _ in range(iterations):
    add_commit_edit(iterations)