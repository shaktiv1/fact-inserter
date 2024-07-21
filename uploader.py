import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def upload_files_to_s3(bucket_name, file_paths, s3_folder='', aws_access_key=None, aws_secret_key=None):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )

    for file_path in file_paths:
        try:
            file_name = file_path.split('/')[-1]
            s3_key = f"{s3_folder}/{file_name}" if s3_folder else file_name
            s3_client.upload_file(file_path, bucket_name, s3_key)
            print(f"Uploaded {file_path} to {bucket_name}/{s3_key}")
        except FileNotFoundError:
            print(f"File {file_path} not found")
        except NoCredentialsError:
            print("Credentials not available")
        except PartialCredentialsError:
            print("Incomplete credentials provided")
        except Exception as e:
            print(f"An error occurred: {e}")

upload_files_to_s3(
    bucket_name='hs-liveops-gec',
    file_paths=['x_fact.png', 'trivia_fact.png', 'wimbledon_fact.png'],
    s3_folder='',
    aws_access_key="acess",
    aws_secret_key="secret"
)