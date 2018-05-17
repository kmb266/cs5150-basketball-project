"""
This script is responsible for updating the local data based on the
Google Drive information in this folder: https://drive.google.com/drive/u/3/folders/10XzxPdk6z5kF4-0fp-XSh_LEO6kzh1kE.

Coaching staff is expected to update this folder (and all sub-folders) with correct XML files
as they become available.
"""

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Authorizes the app with Google - requires user interaction

gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("../../mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
# Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("../../mycreds.txt")

drive = GoogleDrive(gauth)
# root_file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
# for obj in file_list:
#     print('title: %s, id: %s' % (file1['title'], file1['id']))
# xml_files = root_file_list[0]
# print(xml_files)
import os
from populate_db import fill_all_xml

def fetch_new_xml():
    print("Fetching new XML data")
    xml_folder_id = "10XzxPdk6z5kF4-0fp-XSh_LEO6kzh1kE"
    xml_file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(xml_folder_id)}).GetList()
    new_files = False
    for dir in xml_file_list:
        # print('--title: {}, id: {}'.format(dir['title'], dir['id']))
        for data_file in drive.ListFile({'q': "'{}' in parents and trashed=false".format(dir["id"])}).GetList():
            # print('----title: {}, id: {}'.format(data_file['title'], data_file['id']))
            # Download this file in the appropriate directory if it isn't already there
            filename = "../../../xml_data/{}/{}".format(dir['title'], data_file['title'])
            if not os.path.isfile(filename):
                new_files = True
                # print("------File doesn't exist, adding to database")
                # Only download the file if it's not already in the data
                file_obj = drive.CreateFile({'id': data_file["id"]})
                if not os.path.exists("../../../xml_data/{}".format(dir['title'])):
                    os.makedirs("../../../xml_data/{}".format(dir['title']))
                file_obj.GetContentFile(filename)  # Download file to proper directory

    if new_files:
        fill_all_xml()


def main():
    fetch_new_xml()


if __name__ == '__main__':
    print('called xml_downloader')
    main()




