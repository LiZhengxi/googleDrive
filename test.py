from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload
import glob

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API

    #print ('Folder ID: %s' % folder_id) # Display the folder id
    if os.path.isfile('GoogleFolderId.txt') !=True :
        # Create a folder in google drive
        file_metadata1 = {
        'name': 'Video',
        'mimeType': 'application/vnd.google-apps.folder'
        }
        file = service.files().create(body=file_metadata1,
                                        fields='id').execute()
        folder_id = file.get('id')
        file = open("GoogleFolderId.txt", "w+")
        file.write(folder_id)
        print(folder_id)
    else:
        print('folder already create')
        f = open("GoogleFolderId.txt", "r")
        folder_id = f.read()

    # Define the path of all the videos
    path = r'C:\Users\Martin\Desktop\video'
    # Loop all the files in the folder
    for filename in os.listdir(path):
        print (filename)
        # Upload the file into the folder
        file_metadata = {'name': filename,
                         'parents': [folder_id]}
        pathComplete = path+'/'
        media = MediaFileUpload(pathComplete+ filename,
                                mimetype='video/x-msvideo')
        file = service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        print ('File ID: %s' % file.get('id'))
    print ("finish the update")

if __name__ == '__main__':
    main()