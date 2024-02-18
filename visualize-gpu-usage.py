import pandas as pd
import matplotlib.pyplot as plt

# Daten aus der CSV-Datei lesen
df = pd.read_csv('gpu_usage_overall.csv')

# Konvertiere 'Timestamp' in datetime-Objekt
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Linien-Diagramm erstellen
plt.figure(figsize=(10, 6))
plt.plot(df['Timestamp'], df['Total_GPU_Usage'], marker='o', linestyle='-')
plt.title('GPU-Nutzung über die Zeit')
plt.xlabel('Zeit')
plt.ylabel('Total GPU Nutzung')
plt.grid(True)

# Datum- und Uhrzeitformatierung auf der x-Achse verbessern
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('gpu-performance.png')
# Diagramm anzeigen
plt.show()
