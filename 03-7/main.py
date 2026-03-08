import os
import shutil

# folder where files will be organized
path = os.getcwd()

folders = {
    "Images": [".png", ".jpg", ".jpeg", ".gif"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Code": [".py", ".html", ".css", ".js"],
    "Archives": [".zip", ".rar"],
    "Videos": [".mp4", ".mkv"]
}

for file in os.listdir(path):
    file_path = os.path.join(path, file)

    if os.path.isfile(file_path):
        ext = os.path.splitext(file)[1].lower()

        for folder, extensions in folders.items():
            if ext in extensions:
                folder_path = os.path.join(path, folder)

                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                shutil.move(file_path, os.path.join(folder_path, file))
                print(f"Moved {file} -> {folder}")
                break