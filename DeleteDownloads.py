import os
from pathlib import Path
from googletrans import Translator
import unicodedata
import stat

def has_hidden_attribute(filepath):
    return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)

def translate_folder_name(folder_name):
    translator = Translator()
    en_folder_name = translator.translate(folder_name, dest="en")
    return str(en_folder_name.text)

def get_path_download():
    downloads = "Downloads"
    downloads_path = Path.home() / downloads

    if downloads_path.name != downloads:
        downloads_path = Path.home() / translate_folder_name(downloads_path.name)
    
    return str(downloads_path)

def get_files_from_directory(directory_path):
    files = os.listdir(directory_path)
    return files



def safe_decode(file_name):
    try:
        return file_name.encode('latin-1', errors='ignore').decode('latin-1')
    except UnicodeEncodeError:
        return ''.join(c for c in file_name if unicodedata.category(c)[0] != 'C')


def deleteFiles(files, directory_path):
    for file in files:
        decoded_file = safe_decode(file)
        if decoded_file is None:
            continue  # Skip problematic files

        print(decoded_file)

        
        old_path = os.path.join(directory_path, file)
        print("old path: ", old_path)
        if not has_hidden_attribute(old_path):
            try:
                os.unlink(old_path)
            except Exception as e:
                print(f"Error deleting file '{file}': {e}")
        else:
            print(f"File '{file}' has hidden attribute.")


downloads_path = get_path_download()

files = get_files_from_directory(downloads_path)

# Delete files
deleteFiles(files, downloads_path)
