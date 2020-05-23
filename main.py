import datetime
import requests
from dotenv import load_dotenv
import json
import os

load_dotenv()
dry_run = bool(os.getenv('dry_run', False))
artifactory_url = os.getenv('artifactory_url')
token = os.getenv('token')
repo_key = os.getenv('repoKey')
path = os.getenv('path')
lower_date = datetime.datetime.strptime(os.getenv('lower_date'), '%Y-%m-%d').date()


def get(get_path):
    url = artifactory_url + "/api/storage" + get_path
    headers = {"Authorization": "Bearer " + token}
    res = requests.get(url, headers=headers)
    json_data = json.loads(res.text)
    return json_data


def delete(delete_path):
    url = artifactory_url + delete_path
    print(url)
    headers = {"Authorization": "Bearer " + token}
    res = requests.delete(url, headers=headers)
    return res


def processing(processing_path):
    folder_size = 0
    processing_data = get(processing_path)
    if not processing_data.get('children'):
        print(processing_path + " is empty dir")
        if dry_run is True:
            print("This folder now will be deleted \"processing_method\" " + processing_path)
            result = delete(processing_path)
            print(result)
        elif dry_run is False:
            print("DRY RUN This folder will be deleted \"processing_method\" " + processing_path)
    for i in processing_data['children']:
        if i['folder']:
            child_path = processing_path + i['uri']
            children = processing(child_path)
            if children is not None:
                if children:
                    folder_data = get(child_path)
                    folder_full_lmd = folder_data.get('lastModified')  # full last modified date
                    folder_cropped_lmd = datetime.datetime.strptime(folder_full_lmd[:10], '%Y-%m-%d').date()  # cropped last modified date
                    if folder_cropped_lmd < lower_date:
                        if dry_run is True:
                            print("This folder now will be deleted \"child_method\" "+child_path+" it`s last modified date is "+str(folder_cropped_lmd))
                            result = delete(child_path)
                            print(result)
                        elif dry_run is False:
                            print("DRY RUN This folder will be deleted \"child_method\" "+child_path+" it`s last modified date is "+str(folder_cropped_lmd))
                        else:
                            print("Folder "+child_path+" will not be deleted, iit`s last modified date is "+str(folder_cropped_lmd))
        else:
            end_folder = True
            return end_folder
            # child_method = processing_method + i['uri']
            # file_info = get(child_method)
            # folder_size += int(file_info['size'])
    # if folder_size is not 0:
    #     print(processing_data['path']+" is folder")
    #     print("Folder size is " + str(folder_size))
    #     print(processing_data['lastModified'])


if __name__ == "__main__":
    method_parent = "/"+repo_key+"/"+path
    processing(method_parent)
