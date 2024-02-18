import pandas as pd
import matplotlib.pyplot as plt

# Daten aus der CSV-Datei lesen
df = pd.read_csv('smart_home_db.simulation_data.csv')

# Gruppieren und eine fortlaufende Zahl pro Stunde generieren
hour_mapping = df.groupby('time_of_day').cumcount()

# Linien-Diagramm für die Lichtintensität
plt.figure(figsize=(10, 5))
plt.plot(df['time_of_day'] + (hour_mapping / (hour_mapping.max() + 1)), df['total_light_intensity'], 
         label='Lichtintensität', color='blue')
plt.xlabel('Stunde des Tages')
plt.ylabel('Lichtintensität')
plt.title('Lichtintensität über den Tag')
plt.legend()
plt.grid(True)
plt.xticks(df['time_of_day'].unique())  # Die x-Achse beschriften
plt.savefig('lichtintensitaet.png')
plt.close()

# Linien-Diagramm für den Energieverbrauch
plt.figure(figsize=(10, 5))
plt.plot(df['time_of_day'] + (hour_mapping / (hour_mapping.max() + 1)), df['total_energy_consumption'], 
         label='Energieverbrauch', color='green')
plt.xlabel('Stunde des Tages')
plt.ylabel('Energieverbrauch')
plt.title('Energieverbrauch über den Tag')
plt.legend()
plt.grid(True)
plt.xticks(df['time_of_day'].unique())  # Die x-Achse beschriften
plt.savefig('energieverbrauch.png')
plt.close()