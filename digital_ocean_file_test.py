from boto3 import session
import boto3
from botocore.client import Config
import json
# import streamlit as st

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

def upload(filename):
# Upload a file to your Space
# idealy should wipe the existing file --- 
    s3 = boto3.resource('s3')
    s3.Bucket('habitum-user-data').upload_file(Filename = filename, Key = filename)

# end if

def test_download(filename):
    
    user_dict = None
    path = f'/Users/ben/projects/habit-tracker/{filename}'
    path = str(path)
   
    
    # downloads and replaces old data with new data
    client.download_file('habitum-user-data', filename, path)
    
    # client.download_file(Bucket="habitum-user-data", Key="test.json", Filename="/Users/ben/projects/habit-tracker/test.json" )

    # goes into the json file and opens it
    with open(filename, "r", encoding="utf-8") as json_file:
        user_dict = json.load(json_file)
        print(user_dict)

    to_change = input("what is your type?")
    user_dict["type"] = to_change

    # update the local json file
    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(user_dict, json_file)

    # then need to update the digital ocean information - upload into an existing file - should replace the old with the new
    upload(filename)
# end function

def demo():
    flag = None
    username = input("What is your username: ")
    filename = None
    if username == "":
        flag = False
    else:
        flag = True
    # end if
    
    if flag == True:
        filename = f"{username}.json"
         # now type string instead of nonetype
        # filename = str(filename)
        test_download(filename)
    # end if    
# end function

demo()

# if you want to use steamlit need so store the information in the session state
# Invalid type for parameter Key, value: None, type: <class 'NoneType'>, valid types: <class 'str'>

    
    

