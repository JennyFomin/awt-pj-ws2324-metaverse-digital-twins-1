# -----------------
#
# This script visualizes GPU usage over time by plotting data from a CSV file 
# using pandas for data handling and matplotlib for charting. 
# Data points are marked and connected by lines, with the final chart showing the trend of GPU usage. 
# The plot provides a clear visual representation of GPU performance trends.
# 
# -----------------

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('gpu_usage_overall.csv')

df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# create diagram
plt.figure(figsize=(10, 6))
plt.plot(df['Timestamp'], df['Total_GPU_Usage'], marker='o', linestyle='-')
plt.title('gpu usage')
plt.xlabel('time')
plt.ylabel('total gpu usage')
plt.grid(True)

# adjust date and time formatting
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('results/gpu-performance.png')

