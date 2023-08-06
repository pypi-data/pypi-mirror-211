import requests
import os
import fnmatch


def upload_file(presigned_url, presigned_fields, file_path):
    with open(file_path, "rb") as file:
        files = {"file": (file.name, file)}
        response = requests.post(presigned_url, data=presigned_fields, files=files)
        if response.status_code == 204:
            return True
            # print("File uploaded successfully.")
        else:
            print("File upload failed.")
            return False


def get_files_by_extensions(root_dir, extensions):
    matches = []
    for root, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            for extension in extensions:
                if fnmatch.fnmatch(filename, f"*.{extension}"):
                    matches.append(
                        os.path.relpath(os.path.join(root, filename), start=root_dir)
                    )
                    break
    return matches