# Name der CSV-Datei
$csvFile = "gpu_usage_overall.csv"

# Header für die CSV-Datei
"Timestamp,Total_GPU_Usage" | Out-File $csvFile

# Überwachungsintervall in Sekunden
$monitorInterval = 10

# Pfad des GPU-Leistungsindikators für die Gesamt-GPU-Auslastung
$gpuUsageCounter = "\GPU Engine(*)\Utilization Percentage"

while ($true) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    # Erfassen der Gesamt-GPU-Auslastung
    $gpuUsage = Get-Counter -Counter $gpuUsageCounter -ErrorAction SilentlyContinue
    
    if ($gpuUsage) {
        # Es könnte mehrere Instanzen der GPU Engine geben, daher summieren wir die Auslastung
        $totalGpuUsage = ($gpuUsage.CounterSamples | Measure-Object -Property CookedValue -Sum).Sum
        
        # Schreiben der gesamten GPU-Auslastung und des Zeitstempels in die CSV-Datei
        "$timestamp,$totalGpuUsage" | Out-File $csvFile -Append
    }
    else {
        Write-Host "Fehler beim Abrufen der GPU-Auslastung."
    }

    Start-Sleep -Seconds $monitorInterval
}
