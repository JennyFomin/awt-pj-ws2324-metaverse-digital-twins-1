# -----------------
# 
# This Python script is designed to monitor and log the resource usage of specified processes 
# on a system over time. 
# It utilizes the psutil library to access process information and system resource utilization, 
# such as CPU and memory percentages. 
# The script is configured to track specific processes, identified by their names at a defined interval.  
# 
# -----------------

import psutil
import csv
import time
from datetime import datetime

# Configuration
output_csv = 'resource_usage.csv'  
monitor_interval = 20  
process_names = ['Unity3d', 'python3', 'mosquitto'] 

def find_processes_by_name(names):
    matched_processes = []
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] in names:
            matched_processes.append(proc)
    return matched_processes

def write_to_csv(filename, data):
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['timestamp', 'pid', 'name', 'memory_percent', 'cpu_percent']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        for entry in data:
            writer.writerow({'timestamp': datetime.now(), 'pid': entry['pid'], 'name': entry['name'],
                             'memory_percent': entry['memory_percent'], 'cpu_percent': entry['cpu_percent']})

def main():
    while True:
        matched_processes = find_processes_by_name(process_names)
        stats = []
        for proc in matched_processes:
            try:
                # get cpu and memory utalization of the process
                cpu_percent = proc.cpu_percent()
                memory_percent = proc.memory_percent()
                stats.append({
                    'pid': proc.pid,
                    'name': proc.name(),
                    'memory_percent': memory_percent,
                    'cpu_percent': cpu_percent
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass  
            
        write_to_csv(output_csv, stats)
        time.sleep(monitor_interval)

if __name__ == '__main__':
    main()
