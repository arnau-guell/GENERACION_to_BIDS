############################################
########  DICOM TRANSFER TO MACHINE ########
########      PENLab Mar 2026       ########
############################################

import os
import json
import subprocess
import re
import paramiko
import getpass
import stat

# These functions generate and modify the meta.json file that stores the session paths
root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

json_meta = os.path.join(root_dir, "output", "meta.json")

def meta_create():
    '''This function creates an empty meta.json file in the output folder'''
    if os.path.isfile(json_meta) == False:
        empty_dict = {
                      "local_user": "",
                      "local_dicom": "",
                      "dicom": "",
                      "dicom_list": "",
                      "bids": "",
                      "bids_ws": "",
                      "heuristic": "",
                      }
        with open(json_meta, 'a') as file:
            json.dump(empty_dict, file)
            

def meta_func(var, msg, msg2="", ispath=True):
    '''This function collects, updates and returns all the user-inputed data needed
    for the conversion to BIDS. This data is stored in outputs/meta.json'''    
    with open(json_meta, 'r') as file:
        data = json.load(file)
    edit_data = False
    if var not in data:
        data[var] = ""
    if data[var] != "":
        value_ok = False
        while value_ok == False:
            value_check = input("Is this {}?:\n{}\n(Y/N) ".format(msg, data[var])).upper()
            if value_check == 'Y':
                value_ok = True
            elif value_check == 'N':
                data[var] = input(r"Please, enter {}{}: ".format(msg, msg2))
                if ispath == True:
                    data[var] = os.path.normpath(data[var]).strip(" '") # remove '' from string
                edit_data = True
                value_ok = True
            else:
                print("Please, enter a valid response.")
    else:
        data[var] = os.path.normpath(input(r"Please, enter {}{}: ".format(msg, msg2)).strip(" '"))
        edit_data = True
    if edit_data == True:
        with open(json_meta, 'w') as file:
            json.dump(data, file)
    return data[var]

# Function to list folders in a given directory
def list_folders_sftp(sftp, path):
    """Return a list of folder (subjects) names in the given remote directory."""
    try:
        entries = sftp.listdir_attr(path)
    except FileNotFoundError:
        print(f"Error: The path '{path}' does not exist.")
        return []

    return [entry.filename for entry in entries if stat.S_ISDIR(entry.st_mode)]

def get_local_ip():
    # get IP address from SSH
    try:
        local_ip = os.environ.get("SSH_CLIENT").split()[0]
        return local_ip
    except:
        print("ERROR: No ssh connection detected.")
        return

def copy_files(dicom_list, local_username, local_dicoms_dir, dicoms_dir, local_ip):
    dicom_list = sorted(dicom_list)
    print(f"These subs will be copied: {dicom_list}")
    for dicom_sub in dicom_list:
        sep_dicompath = '\\' if '\\' in local_dicoms_dir and '/' not in local_dicoms_dir else '/'
        dicom_path = local_dicoms_dir.rstrip(sep_dicompath) + sep_dicompath + dicom_sub
        print(f"INFO: Copying sub {dicom_sub} from {local_dicoms_dir} to {dicoms_dir}")
        subprocess.run([
                            "rsync", "-avh", "--progress", "--partial", "--checksum",
                            f"{local_username}@{local_ip}:{dicom_path}",
                            f"{dicoms_dir}"
                        ])

def main():
    # Input paths
    meta_create()
    local_username = meta_func("local_user", "your user name in the local machine")     # User name on the local machine
    password = getpass.getpass("Please, enter your local machine user password: ")
    local_dicoms_dir = meta_func("local_dicom", "the path to the DICOMs folder in the local disk")  # Path to DICOM directories in the local disk
    dicoms_dir = meta_func("dicom", "the path to the temporary workspace DICOMs folder")  # Path to DICOM directories
    temp_bids_dir = meta_func("bids_ws", "the path to the temporary workspace BIDS folder")  # Path to local BIDS directory
    bids_dir = meta_func("bids", "the path to the archive BIDS folder")  # Path to shared BIDS directory

    local_ip = get_local_ip()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(local_ip, username=local_username, password=password)

    sftp = ssh.open_sftp()

    subs_in_disk = list_folders_sftp(sftp, local_dicoms_dir)

    sftp.close()
    ssh.close()

    todo_dicoms = {
                sub for sub in subs_in_disk
                if sub not in dicoms_dir
                and re.sub(r'[^a-zA-Z0-9]', '', sub) not in bids_dir
                and re.sub(r'[^a-zA-Z0-9]', '', sub) not in temp_bids_dir
                }
    
    copy_files(todo_dicoms, local_username, local_dicoms_dir, dicoms_dir, local_ip)

if __name__ == '__main__':
    main()