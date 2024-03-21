#!/usr/bin/python3
import os 
import shutil
import sys
import time

def sync_folders(source_folder, replica_folder, log_file):
    
    for root, dirs, files in os.walk(source_folder):
        # Determine the corresponding subfolder in the replica folder
        replica_root = root.replace(source_folder, replica_folder, 1)

        if not os.path.exists(replica_folder):
            os.makedirs(replica_folder)

        # Create replica subfolder if it doesn't exist
        if not os.path.exists(replica_root):
            os.makedirs(replica_root)

        # Sync files
        for file in files:
            source_file_path = os.path.join(root, file)
            replica_file_path = os.path.join(replica_root, file)

            if not os.path.exists(replica_file_path) or \
               (os.path.exists(replica_file_path) and os.path.getmtime(source_file_path) != os.path.getmtime(replica_file_path)):
                shutil.copy2(source_file_path, replica_file_path)
                with open(log_file, "a") as log:
                    log.write(f"Copied: {source_file_path} to {replica_file_path}\n")

        # Sync directories
        for directory in dirs:
            sync_folders(os.path.join(root, directory), os.path.join(replica_root, directory), log_file)
                  

def main_time():
    if (len(sys.argv) !=5):
        print("Utilization: ./sync_folders.py <replica_folder> <source_folder> <log_file> <interval_seconds>")
        sys.exit(1)
   
    source_folder=sys.argv[1]
    replica_folder=sys.argv[2]
    log_file=sys.argv[3]
    interval_seconds=int(sys.argv[4])

    while True:
     with open(log_file, "a") as log:
        log.write(f"Synchronization just started at {time.ctime()}\n")
     sync_folders(source_folder, replica_folder, log_file)
     with open(log_file,"a") as log:
            log.write(f"Synchronization is completed at {time.ctime()}\n")
     time.sleep(interval_seconds)

main_time()
