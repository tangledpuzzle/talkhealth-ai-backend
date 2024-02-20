import json
import os

def delete_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

def organize_outlook(index):
    user_list = []
    for file in os.listdir('./temp'):
        if not file.endswith(".json"):
            continue
        filepath = os.path.join('./temp', file)
        try:
            with open(filepath, "r", encoding= 'utf-8') as f:
                user_data = json.load(f)
                user_list.append(user_data)
        except Exception as e:
            pass
    
    with open(f"./result/{index}.json", "w", encoding= "utf-8") as f:
        json.dump(user_list, f, indent= 4)

    delete_files('./temp')

        

        