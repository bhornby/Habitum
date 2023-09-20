from boto3 import session
from botocore.client import Config

ACCESS_ID = 'DO00YD8PQZ9D7JNEZ97J'
SECRET_KEY = 'uFyI3fQ2KEJbd4ndU/LoNmlI/xcUZyyvs9RQ2qnd0hg'

# Initiate session
session = session.Session()
client = session.client('s3',
                        region_name='nyc3',
                        endpoint_url='https://nyc3.digitaloceanspaces.com',
                        aws_access_key_id=ACCESS_ID,
                        aws_secret_access_key=SECRET_KEY)

# Upload a file to your Space
client.upload_file('beninformation.json', 'habitum-user-data', 'user_data/ben_information.json')