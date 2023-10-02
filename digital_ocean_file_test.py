from boto3 import session
from botocore.client import Config
import json

ACCESS_ID = 'DO00YD8PQZ9D7JNEZ97J'
SECRET_KEY = 'uFyI3fQ2KEJbd4ndU/LoNmlI/xcUZyyvs9RQ2qnd0hg'
user = None

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
def locate_user():
    folder_list = []
    user_data = None
    response = client.list_objects(Bucket="habitum-user-data")
    for folder in response['Contents']:
        name = folder["Key"]
        folder_list.append(name)
    # next folder
# end function

def test_download():
    user_dict = None
    
    # downloads and replaces old data with new data
    client.download_file(Bucket="habitum-user-data", Key="test.json", Filename="/Users/ben/projects/habit-tracker/test.json" )

    to_change = input("what is your type?")

    # goes into the json file and opens it
    with open("test.json", "r", encoding="utf-8") as json_file:
        user_dict =  json.load(json_file)

    user_dict["type"] = to_change

    # update the local json file
    with open("test.json", "w", encoding="utf-8") as json_file:
        json.dump(user_dict, json_file)

    # then need to update the digital ocean information - upload into an existing file - should replace the old with the new
    client.put_object(Bucket='habitum-user-data',
                  Key='test.json',
                  Body="test.json",
                  ACL='private',
                )

test_download()


