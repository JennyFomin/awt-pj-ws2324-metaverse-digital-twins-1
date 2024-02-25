# -----------------
# 
# This PowerShell script is designed to monitor and log the overall GPU usage on a system over time. 
# It works by querying a specific performance counter, which measures the utilization percentage of the GPU. 
# The script captures the total GPU usage at defined intervals.
# 
# The script aggregates the GPU usage by summing up the utilization percentages of all 
# instances of the GPU Engine, which is necessary because a system may have multiple GPU engines. 
# 
# -----------------


$csvFile = "results/gpu_usage_overall.csv"

# csv header
"Timestamp,Total_GPU_Usage" | Out-File $csvFile

$monitorInterval = 10

$gpuUsageCounter = "\GPU Engine(*)\Utilization Percentage"

while ($true) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    # capture total gpu utalization 
    $gpuUsage = Get-Counter -Counter $gpuUsageCounter -ErrorAction SilentlyContinue
    
    if ($gpuUsage) {
        # sum of gpu instances because may have multiple gpu engines
        $totalGpuUsage = ($gpuUsage.CounterSamples | Measure-Object -Property CookedValue -Sum).Sum
        
        "$timestamp,$totalGpuUsage" | Out-File $csvFile -Append
    }
    else {
        Write-Host "Fehler beim Abrufen der GPU-Auslastung."
    }

    Start-Sleep -Seconds $monitorInterval
}
