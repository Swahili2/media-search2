
import os
import pickle
import json
import urllib.parse as urlparse
from urllib.parse import parse_qs
from requests.utils import quote
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


class GoogleDriveHelper:
    def __init__(self, name=None, listener=None):
        self.__G_DRIVE_DIR_MIME_TYPE = "application/vnd.google-apps.folder"
        self.__G_DRIVE_TOKEN_FILE = "token.pickle"
        self.__OAUTH_SCOPE = ['https://www.googleapis.com/auth/drive']
        self.__service = self.authorize()
        self.path = []
    def rename_file(service, file_id, new_title):
        try:
            file = {'name': new_title}
            updated_file = service.files().patch(
                    fileId=file_id,
                    body=file,
                    fields='name').execute()
            return updated_file
        except:
            print('An error occurred')
            return None
    def authorize(self):
        # Get credentials
        credentials = None
        if os.path.exists(self.__G_DRIVE_TOKEN_FILE):
            with open(self.__G_DRIVE_TOKEN_FILE, 'rb') as f:
                credentials = pickle.load(f)
        if credentials is None or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.__OAUTH_SCOPE)
                credentials = flow.run_console(port=0)

            # Save the credentials for the next run
            with open(self.__G_DRIVE_TOKEN_FILE, 'wb') as token:
                pickle.dump(credentials, token)
        return build('drive', 'v3', credentials=credentials, cache_discovery=False)
    @staticmethod
    def getIdFromUrl(link: str):
        if "folders" in link or "file" in link:
            regex = r"https://drive\.google\.com/(drive)?/?u?/?\d?/?(mobile)?/?(file)?(folders)?/?d?/([-\w]+)[?+]?/?(w+)?"
            res = re.search(regex,link)
            if res is None:
                return "GDrive ID not found. Try sending url in different format."
            return res.group(5)
        parsed = urlparse.urlparse(link)
        return parse_qs(parsed.query)['id'][0]

    async def drive_list(self, LINKorID):
        if self.__service is None:
            return
        if 'drive.google.com' in LINKorID:
            try:
                file_id = self.getIdFromUrl(LINKorID)
                if 'GDrive ID not found.' in file_id:
                    print(file_id)
                    return
            except (KeyError, IndexError):
                print("GDrive ID could not be found in the provided link.")
                return
        else:
            file_id = LINKorID.strip()

        error = False
        print("Calculating... Please Wait!")

        try:
            drive_file = self.__service.files().get(fileId=file_id, fields="id, name, mimeType, size",
                                                   supportsTeamDrives=True).execute()
            name = drive_file['name']
            if drive_file['mimeType'] == self.__G_DRIVE_DIR_MIME_TYPE:
                typee = 'Folder'
                self.gDrive_directory(**drive_file)
            else:
                try:
                    typee = drive_file['mimeType']
                    if drive_file['name'].startswith('Copy of ')):
                        new_title = file['name'].replace('Copy of ', '')
                        rename_file(__service, file_id, new_title)
                except:
                    typee = 'File'
        
        except:
            print('An error occurred')
                self.gDrive_file(**drive_file)

        except Exception as e:
            print('\n')
            if 'HttpError' in str(e):
                h_e = str(e)
                ori = h_e
                try:
                    h_e = h_e.replace('<', '').replace('>', '')
                    h_e = h_e.split('when')
                    f = h_e[0].strip()
                    s = h_e[1].split('"')[1].split('"')[0].strip()
                    e =  f"{f}\n{s}"
                except:
                    e = ori
            print(str(e))
            error = True
    def list_drive_dir(self, file_id: str) -> list:
        query = f"'{file_id}' in parents and (name contains '*')"
        fields = 'nextPageToken, files(id, mimeType, size)'
        page_token = None
        page_size = 1000
        files = []
        while True:
            response = self.__service.files().list(supportsTeamDrives=True,
                                                  includeTeamDriveItems=True,
                                                  q=query, spaces='drive',
                                                  fields=fields, pageToken=page_token,
                                                  pageSize=page_size, corpora='allDrives',
                                                  orderBy='folder, name').execute()
            files.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return files

    def gDrive_file(self, **kwargs):
        try:
            size = int(kwargs['size'])
            if(kwargs['name'].startswith('Copy of ')):
                        new_title = file['name'].replace('Copy of ', '')
                        rename_file(__service, file_id, new_title)
        except:
            print('error')

    def gDrive_directory(self, **kwargs) -> None:
        files = self.list_drive_dir(kwargs['id'])
        if len(files) == 0:
            return
        for file_ in files:
            if file_['mimeType'] == self.__G_DRIVE_DIR_MIME_TYPE:
                self.total_folders += 1
                self.gDrive_directory(**file_)
            else:
                self.total_files += 1
                self.gDrive_file(**file_)


drv= GoogleDriveHelper(None)
