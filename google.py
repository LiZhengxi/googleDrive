from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload
import time
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
                r'/home/pi/move/google/credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)



    while 1 :
        try:
            service = build('drive', 'v3', credentials=creds)
            i=1
        except  Exception:
            print("not network")
            i=0
        if (i==1):
        # Call the Drive v3 API
        #print ('Folder ID: %s' % folder_id) # Display the folder id
            if os.path.isfile(r"/home/pi/move/google/GoogleFolderId.txt") !=True :
                # Create a folder in google drive
                file_metadata1 = {
                'name': 'Video',
                'mimeType': 'application/vnd.google-apps.folder'
                }
                file = service.files().create(body=file_metadata1,
                                                fields='id').execute()
                folder_id = file.get('id')
                file = open(r"/home/pi/move/google/GoogleFolderId.txt", "w+")
                file.write(folder_id)
                print(folder_id)
            else:
                print('folder already create')
                f = open(r"/home/pi/move/google/GoogleFolderId.txt", "r")
                folder_id = f.read()
            q = "'{}' in parents".format(folder_id)
            # Get the google drive file list
            results = service.files().list(
                pageSize=1000, q=q , fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])
            listFile = []
            if not items:
                print('No files found.')
            else :
                for item in items:
                    listFile.append(u'{0}'.format(item['name']))

            # Define the path of all the videos
            path = r'/home/pi/move/video'
            # Loop all the files in the folder

            for filename in os.listdir(path):
                if filename not in listFile :
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
            time.sleep(3600)
        else:
            time.sleep(1)


if __name__ == '__main__':
    
  
    main()