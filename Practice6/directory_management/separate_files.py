import os

path = "project"

for item in os.listdir(path):
    full_path = os.path.join(path, item)

    if os.path.isdir(full_path):
        print("Folder:", item)
    else:
        print("File:", item)