# -----------------
#
# This script creates visualizations for CPU and memory usage over time, 
# using pandas and matplotlib. It generates two linked subplots in one figure: 
# one for CPU usage and another for memory usage, each plotting data for different processes. 
# Each process is represented as a separate line on the charts, with legends for identification. 
# 
# -----------------

import pandas as pd
import matplotlib.pyplot as plt

csv_file = 'resource_usage.csv'

df = pd.read_csv(csv_file)

df['timestamp'] = pd.to_datetime(df['timestamp'])

# create subplots for cpu and memory usage
fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# cpu usage for each process
for name, group in df.groupby('name'):
    axs[0].plot(group['timestamp'], group['cpu_percent'], label=name)

axs[0].set_title('cpu usage')
axs[0].set_ylabel('total cpu usage (%)')
axs[0].legend()

# memory usage for each process
for name, group in df.groupby('name'):
    axs[1].plot(group['timestamp'], group['memory_percent'], label=name)

axs[1].set_title('memory usage')
axs[1].set_ylabel('total memory usage (%)')
axs[1].set_xlabel('time')
axs[1].legend()

# adjust date and time formatting
plt.tight_layout()
plt.savefig('results/memory-cpu-performance.png')
plt.show()

