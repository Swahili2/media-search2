from __future__ import print_function
import httplib2
import os.path
import json

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

def get_credentials():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds
    
def rename_file(service, file_id, new_title):
    try:
        file = {'title': new_title}
        updated_file = service.files().patch(
                fileId=file_id,
                body=file,
                fields='title').execute()
        return updated_file
    except:
        print('An error occurred')
        return None

def list_files_in_folder(service, folder_id):
    files = []
    page_token = None
    
    while True:
        try:
            param = {}
            if page_token:
                param['pageToken'] = page_token
            children = service.children().list(folderId=folder_id, **param).execute()
            for child in children.get('items', []):
                files.append(child['id'])
            page_token = children.get('nextPageToken')
            if not page_token:
                break
        except:
            print('An error occurred')
            break
    return files
    
def main():
    creds = get_credentials()
    http = creds.authorize(httplib2.Http())
    service = build('drive', 'v3', credentials=creds)
    for fileid in list_files_in_folder(service, '0BwaM3xCs0Uh4NXd4OU9kb3pjRlk'):
        try:
            file = service.files().get(fileId=fileid).execute()
            if(file['title'].startswith('Copy of ')):
                new_title = file['title'].replace('Copy of ', '')
                rename_file(service, fileid, new_title)
        except:
            print('An error occurred')
