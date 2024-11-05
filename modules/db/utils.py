import os
import datetime
import glob
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv

load_dotenv()

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
    db_dir = os.path.join(top_level_dir, 'modules', 'db', 'dumps')

    # Ensure the directory exists
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    today_str = datetime.datetime.now().strftime("%Y%m%d")
    prefix = "TEST_" if testing else ""
    db_file = os.path.join(db_dir, f'{prefix}db_{today_str}.db')

    # Get AWS credentials and region from environment variables
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_region = os.environ.get('AWS_REGION')

    if not aws_access_key_id or not aws_secret_access_key or not aws_region:
        raise RuntimeError("AWS credentials or region not found in environment variables")

    s3_bucket_name = 'sisooyin-db-files'
    s3_prefix = f'{prefix}db_'
    s3 = boto3.client('s3', 
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      region_name=aws_region)

    if not os.path.exists(db_file):
        # Check for the most recent previous day's file in the local directory
        list_of_files = glob.glob(os.path.join(db_dir, f'{prefix}db_*.db'))
        if list_of_files:
            latest_file = max(list_of_files, key=os.path.getctime)
            # Copy the latest file to create today's file
            with open(latest_file, 'rb') as src, open(db_file, 'wb') as dst:
                dst.write(src.read())
        else:
            # Check the S3 bucket for the most recent previous day's file
            try:
                response = s3.list_objects_v2(Bucket=s3_bucket_name, Prefix=s3_prefix)
                if 'Contents' in response:
                    s3_files = [obj['Key'] for obj in response['Contents'] if obj['Key'].endswith('.db')]
                    if s3_files:
                        latest_s3_file = max(s3_files, key=lambda x: x.split('_')[-1].split('.')[0])
                        s3.download_file(s3_bucket_name, latest_s3_file, db_file)
                    else:
                        # Create a new database file for today if no previous files exist
                        open(db_file, 'w').close()
                else:
                    # Create a new database file for today if no previous files exist
                    open(db_file, 'w').close()
            except (NoCredentialsError, PartialCredentialsError) as e:
                raise RuntimeError("S3 credentials not found or incomplete") from e
            except Exception as e:
                raise RuntimeError("Error accessing S3 bucket") from e

    # Upload the local file to the S3 bucket
    try:
        s3.upload_file(db_file, s3_bucket_name, f'{s3_prefix}{today_str}.db')
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise RuntimeError("S3 credentials not found or incomplete") from e
    except Exception as e:
        raise RuntimeError("Error uploading file to S3 bucket") from e

    return db_file