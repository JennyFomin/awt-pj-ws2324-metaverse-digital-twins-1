import pandas as pd
import matplotlib.pyplot as plt

# Pfad zur CSV-Datei
csv_file = 'resource_usage.csv'

# Daten aus der CSV-Datei lesen
df = pd.read_csv(csv_file)

# Konvertieren Sie die 'timestamp'-Spalte in ein datetime-Objekt
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Erstellen Sie separate Diagramme für CPU und Speicher
fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# CPU-Auslastung über die Zeit für jeden Prozess
for name, group in df.groupby('name'):
    axs[0].plot(group['timestamp'], group['cpu_percent'], label=name)

axs[0].set_title('CPU-Auslastung über die Zeit')
axs[0].set_ylabel('CPU-Auslastung (%)')
axs[0].legend()

# Speicherauslastung über die Zeit für jeden Prozess
for name, group in df.groupby('name'):
    axs[1].plot(group['timestamp'], group['memory_percent'], label=name)

axs[1].set_title('Speicherauslastung über die Zeit')
axs[1].set_ylabel('Speicherauslastung (%)')
axs[1].set_xlabel('Zeit')
axs[1].legend()

# Verbessern Sie die Formatierung und zeigen Sie den Plot an
plt.tight_layout()
plt.savefig('memory-cpu-performance.png')
plt.show()

