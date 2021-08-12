import datetime
import requests
from dotenv import load_dotenv
import json
import os

load_dotenv()

dry_run = os.environ.get('dry_run', "True")
artifactory_url = os.environ.get('artifactory_url')
token = os.environ.get('token')
repo_key = os.environ.get('repoKey')
path = os.environ.get('path')
lower_date = datetime.datetime.strptime(os.environ.get('lower_date'), '%Y-%m-%d').date()

if dry_run == "False":
    dry_run = False
else:
    dry_run = True


def get(get_path):
    url = artifactory_url + "/api/storage" + get_path
    headers = {"Authorization": "Bearer " + token}
    res = requests.get(url, headers=headers)
    json_data = json.loads(res.text)
    # print(json_data)
    return json_data


def delete(delete_path):
    url = artifactory_url + delete_path
    print(url)
    headers = {"Authorization": "Bearer " + token}
    res = requests.delete(url, headers=headers)
    return res


def processing(processing_path):
    # folder_size = 0
    # print("processing path is "+processing_path)
    processing_data = get(processing_path)
    # process of the deleting empty dir
    if not processing_data.get('children'): # if dir is empty than delete dir
        print(processing_path + " is empty dir")
        if dry_run is False:
            print("This folder is empty and now will be deleted \"processing_method\" " + processing_path)
            result = delete(processing_path)
            print(result)
        elif dry_run is True:
            print("DRY RUN This folder is empty and now will be deleted \"processing_method\" " + processing_path)
    # processing of all children
    for child in processing_data['children']:
        # print("processing the child "+json.dumps(child)+" from "+json.dumps(processing_data['children']))
        if child['folder']:
            # print("child "+child['uri']+" is the folder")
            child_path = processing_path + child['uri']
            # Enter in recursion
            children_of_child = processing(child_path)
            # recursion will end when this call returns something, else will enter in recursion with new processing
            # Exit from recursion when it is the last folder of branch
            # when children of child is not the folder than go next
            # this is the last folder
            if children_of_child is not None:
                if children_of_child:
                    folder_data = get(child_path)
                    folder_full_lmd = folder_data.get('lastModified')  # full last modified date
                    folder_cropped_lmd = datetime.datetime.strptime(folder_full_lmd[:10], '%Y-%m-%d').date()  # cropped last modified date
                    if folder_cropped_lmd < lower_date:
                        if dry_run is False:
                            print("This folder now will be deleted \"child_method\" "+child_path+" it`s last modified date is "+str(folder_cropped_lmd))
                            result = delete(child_path)
                            print(result)
                        elif dry_run is True:
                            print("DRY RUN This folder will be deleted \"child_method\" "+child_path+" it`s last modified date is "+str(folder_cropped_lmd))
                        else:
                            print("Folder "+child_path+" will not be deleted, it`s last modified date is "+str(folder_cropped_lmd))
        else:
            # this cild is not a folder
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
