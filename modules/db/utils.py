import os
import datetime
import glob


def parse_saga_episode(saga_episode):
    # Split the saga_episode string on the delimiter "à"
    parts = saga_episode.split("à")
    if len(parts) == 2:
        # Convert the parts to integers and return as a tuple
        return int(parts[0].strip()), int(parts[1].strip())
    else:
        raise ValueError("Invalid saga_episode format")
    
def get_daily_db_file(testing=False):
    # Define the directory
    top_level_dir = os.path.join(os.path.dirname(__file__), '..', '..')
    db_dir = os.path.join(top_level_dir, 'modules', 'data', 'db', 'dumps')

    # Ensure the directory exists
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    today_str = datetime.datetime.now().strftime("%Y%m%d")
    prefix = "TEST_" if testing else ""
    db_file = os.path.join(db_dir, f'{prefix}db_{today_str}.db')

    if not os.path.exists(db_file):
        # Check for the most recent previous day's file
        list_of_files = glob.glob(os.path.join(db_dir, f'{prefix}db_*.db'))
        if list_of_files:
            latest_file = max(list_of_files, key=os.path.getctime)
            # Copy the latest file to create today's file
            with open(latest_file, 'rb') as src, open(db_file, 'wb') as dst:
                dst.write(src.read())
        else:
            # Create a new database file for today if no previous files exist
            open(db_file, 'w').close()

    return db_file