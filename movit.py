import hashlib
import os
import shutil

# Path to input text file created by whichos.py
source_file = "J:\\Office Library\\filedb.txt"

# Path to target directory where the files will be copied
target_directory = "J:\\Office Library"

# Create the target directory if it doesn't exist
os.makedirs(target_directory, exist_ok=True)

# Read the source file line by line use utf-8 encoding as some files have non-ASCII characters
with open(source_file, "r", encoding="utf-8") as file:
    for line in file:
        # Split the line into file path and SHA256 hash using a tab character as the delimiter
        file_path, sha256_hash = line.strip().split("\t", 1)
        
        # build the destination file path
        destination_file = os.path.join(target_directory, os.path.basename(file_path))
        
        try:
            # Check if the file with the same SHA256 hash has already been copied
            if os.path.exists(destination_file):
                with open(destination_file, "rb") as f:
                    existing_hash = hashlib.sha256(f.read()).hexdigest()
                    
                # If the hashes match, skip copying the file
                if existing_hash == sha256_hash:
                    continue
            
            # Copy the file to the target directory
            shutil.copy2(file_path, target_directory)
            #print(f"Copied file: {file_path}")

        except Exception as e:
            print(f"Error copying file: {file_path} - {str(e)}")
            continue

print("Copying completed!")