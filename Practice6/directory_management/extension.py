import os

path = "project"

for file in os.listdir(path):
    if file.endswith(".txt"):
        print(file)