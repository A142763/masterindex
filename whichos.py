# A kindof silly script to determine the operating system and drives
# then walk the drives and create a file with the file path and sha256 hash
# of only files of a certain type (in this case, office files)
# jump over files that are open or have permission denied or contain invalid characters in the path
# I'm using this to create a file database for a file migration
# Jimmy James 

import hashlib
import platform
import psutil
import os

def get_operating_system():
    system = platform.system()
    if system == "Windows":
        return "Windows"
    elif system == "Darwin":
        return "macOS"
    elif system == "Linux":
        return "Linux"
    else:
        return "Unknown"

def get_drives():
    drives = []
    partitions = psutil.disk_partitions(all=True)
    for partition in partitions:
        if partition.device not in drives and 'cdrom' not in partition.opts:
            drives.append(partition.device)
    return drives


if __name__ == "__main__":
    operating_system = get_operating_system()
    #print(f"Operating System: {operating_system}")
    # drive_list = get_drives()
    
    # I'm hard-coding the drive list for now as I don't want the destination drive to be included in the search 
    drive_list = ['C:\\', 'D:\\', 'E:\\', 'G:\\', 'H:\\', 'I:\\']
     
    output_file = "J:\\Office Library\\filedb.txt"

    with open(output_file, "w", encoding='utf-8') as outfile:
        for drive in drive_list:
            print(f"Drive: {drive}") 
            for directory, subdirectories, files in os.walk(drive):
                for filename in files:
                    #if filename.endswith(".pdf") or filename.endswith(".PDF"):
                    if any(filename.lower().endswith(ext) for ext in [".xls", ".xlsx", ".ppt", ".pptx", ".doc", ".docx"]):
                        try:
                            with open(os.path.join(directory, filename), "rb") as file:
                                try:
                                    file_contents = file.read()
                                    output_string = f"{os.path.join(directory, filename)}\t{hashlib.sha256(file_contents).hexdigest()}\n"
                                    outfile.write(output_string)

                                except PermissionError:
                                    # Skip the file if permission is denied
                                    print(f"Permission denied for file: {file}. Skipping...")
                                    continue

                        except OSError as e:
                            # Handle the OSError: [Errno 22] Invalid argument exception
                            if e.errno == 22:
                                print(f"Invalid argument for file: {file}. Skipping...")
                            else:
                                print(f"Error occurred while copying file: {file}. {str(e)}")
