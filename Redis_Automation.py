#!/usr/bin/python3

import os
import sys
import subprocess
from datetime import datetime
import tarfile

# Allow root user to execute.
if os.geteuid() == 0:
    print('Allow root user to execute!...')
else:
  print('Access denied!...')

# Downloading Redis server.
def down_redis():
    subprocess.run(["wget", "http://download.redis.io/releases/redis-4.0.9.tar.gz"])
    print("Redis server downloaded successfully!...")

# Extracting Redis server.
def ext_redis():
    subprocess.run(["tar", "xvzf", "redis-4.0.9.tar.gz"])
    print("Extracted Redis server successfully!...")

# Compiling Redis server.
def compile_redis():
    os.chdir("redis-4.0.9")
    subprocess.run(["sudo", "make"])
    print("Redis server compiled successfully!...")

# Run Redis server.
def run_redis():
    subprocess.run(["redis-server"])
    print("Redis server is running!...")

# Installing Redis server.
def install_redis():
    os.chdir("redis-4.0.9")
    subprocess.run(["sudo", "apt", "update"])
    print("Redis server updated successfully!...")
    subprocess.run(["sudo", "apt", "install", "-y", "redis-server"])
    print("Redis server installed successfully!...")

# Stop Redis server.
def stop_redis():
    subprocess.run(["sudo", "systemctl", "stop", "redis-server"])
    print("Redis server stopped successfully!...")

# Check status of Redis server.
def status_redis():
    subprocess.run(["sudo", "service", "redis-server", "status"])
    print("Redis server status checked successfully!...")

# Start Redis server.
def start_redis():
    subprocess.run(["sudo", "service", "redis-server", "start"])
    print("Redis server started successfully!...")

def backup_redis():
    print("Backing up Redis database...")
    # Define backup directory and file names
    backup_dir = "/home/vagrant/REDIS_BACKUP_JUN13"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = f"redis_bkp_jun14{timestamp}.rdb"
    tar_file = f"redis_backup_jun14{timestamp}.tar.gz"

    # Run the Redis save or bgsave command to create an RDB file
    method = input("Choose backup method ('save' or 'bgsave'): ").strip().lower()
    if method == "save":
        try:
            subprocess.run(["redis-cli", "SAVE"], check=True)
            print("Backup created using the SAVE command.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while executing the SAVE command: {e}")
            return
    elif method == "bgsave":
        try:
            subprocess.run(["redis-cli", "BGSAVE"], check=True)
            print("Backup created using the BGSAVE command.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while executing the BGSAVE command: {e}")
            return
    else:
        print("Invalid backup method. Choose 'save' or 'bgsave'.")
        return

    # Copy the RDB file to the backup directory
    try:
        redis_data_dir = "/var/lib/redis"  # Adjust this path as needed
        original_rdb_path = os.path.join(redis_data_dir, "dump.rdb")
        backup_rdb_path = os.path.join(backup_dir, backup_file)
        subprocess.run(["sudo", "cp", original_rdb_path, backup_rdb_path], check=True)
        print("RDB file copied successfully....")

        # Create a tar.gz file from the RDB file
        with tarfile.open(os.path.join(backup_dir, tar_file), "w:gz") as tar:
            tar.add(backup_rdb_path, arcname=backup_file)

        #Optionally remove the original RDB file from the backup directory
        os.remove(backup_rdb_path)
        print(f"Removed temporary backup file {backup_rdb_path}")

        print(f"Backup created and saved successfully as {tar_file}")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while copying the RDB file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
#calling function to be executed.
if sys.argv[1] == 'download':
    down_redis()
elif sys.argv[1] == 'extract':
    ext_redis()
elif sys.argv[1] == 'compile':
    compile_redis()
elif sys.argv[1] == 'run':
    run_redis()
elif sys.argv[1] == 'status':
    status_redis()
elif sys.argv[1] == 'install':
    install_redis()
elif sys.argv[1] == 'stop':
    stop_redis()
elif sys.argv[1] == 'start':
    start_redis()
elif sys.argv[1] == 'backup':
    backup_redis()
else:
    print('Error/help: ./system-metric.py {download|extract|compile|run|backup}\n')