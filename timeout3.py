import boto3
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

access_key_id = 'AKIAUCDYYBIBP7PDADVA'
secret_access_key = 'b+SARVfgm7tnEQCwea1zCH4cpGy8az9APM5uoS+J'


bucket_name = 'forensicks'

local_folder = 'kuiper/files/files'  # Replace with the path to your local folder

def upload_file_to_s3(local_file, bucket_name, access_key_id, secret_access_key):
    try:
       
        s3 = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

       
        s3_key = os.path.relpath(local_file, local_folder).replace("\\", "/")

      
        s3.upload_file(local_file, bucket_name, s3_key)

        print(f'Uploaded: {local_file} to s3://{bucket_name}/{s3_key}')
    except Exception as e:
        print(f"Error: {e}")

def delete_file_from_s3(local_file, bucket_name, access_key_id, secret_access_key):
    try:
        
        s3 = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

        
        s3_key = os.path.relpath(local_file, local_folder).replace("\\", "/")

       #Delete the object
        s3.delete_object(Bucket=bucket_name, Key=s3_key)

        print(f'Deleted: {local_file} from s3://{bucket_name}/{s3_key}')
    except Exception as e:
        print(f"Error: {e}")

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        upload_file_to_s3(event.src_path, bucket_name, access_key_id, secret_access_key)

    def on_deleted(self, event):
        if event.is_directory:
            return
        delete_file_from_s3(event.src_path, bucket_name, access_key_id, secret_access_key)

if __name__ == "__main__":
    upload_file_to_s3(local_folder, bucket_name, access_key_id, secret_access_key)

    observer = Observer()
    observer.schedule(MyHandler(), path=local_folder, recursive=True)
    observer.start()

    try:
        # Run the watchdog for 10 minutes (600 seconds)
        time.sleep(600)
    except KeyboardInterrupt:
        pass

    observer.stop()
    observer.join()
