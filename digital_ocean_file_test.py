from boto3 import session
from botocore.client import Config
import json

ACCESS_ID = 'DO00YD8PQZ9D7JNEZ97J'
SECRET_KEY = 'uFyI3fQ2KEJbd4ndU/LoNmlI/xcUZyyvs9RQ2qnd0hg'
user = "test"
file = None

# Initiate session
session = session.Session()
client = session.client('s3',
                        region_name='nyc3',
                        endpoint_url='https://nyc3.digitaloceanspaces.com',
                        aws_access_key_id=ACCESS_ID,
                        aws_secret_access_key=SECRET_KEY)

# only want to upload the file when the user first creates their account,
# after that all do is read and write to the file

def upload():
# Upload a file to your Space
    client.upload_file('test.json', 'habitum-user-data', 'user_data/test.json')
# end if

def bucket_list():
    # returns a list of all the files in the bucket
    response = client.list_objects(Bucket='habitum-user-data')
    for obj in response['Contents']:
        print(obj['Key'])
# end function   

# return the user information so we can manipulate it
def locate_user(user):
    folder_list = []
    response = client.list_objects(Bucket="habitum-user-data")
    for folder in response['Contents']:
        name = folder["Key"]
        folder_list.append(name)
    # next folder
    print(folder_list)

# Thank you can check against all the use of data stored in the bucket and once you take that you check against username and password that creates that file name
locate_user(user)
# upload()
