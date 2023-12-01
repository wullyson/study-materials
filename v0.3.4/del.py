import os

def delete_files_in_folder(folder_path):
    # 獲取資料夾中的所有檔案
    files = os.listdir(folder_path)

    # 逐一刪除每個檔案
    for file in files:
        file_path = os.path.join(folder_path, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

delete_files_in_folder('./data/Finish')
delete_files_in_folder('./data/Pre-Process_1')
delete_files_in_folder('./data/Pre-Process_2')
delete_files_in_folder('./data/Pre-Process_3')
delete_files_in_folder('./data/Pre-Process_4')
delete_files_in_folder('./data/Pre-Process_5')
delete_files_in_folder('./data/Pre-Process_6')