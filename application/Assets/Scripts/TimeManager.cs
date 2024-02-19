using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TimeManager : MonoBehaviour
{
    [Range(0, 24)]
    public float simulatedHour = 0;
    private float simulationTime;
    public float getSimulationTime()
    {
        return simulationTime;
    }

    public float accTime = 1;

    private List<Schedule> scheduleScripts = new List<Schedule>();

    // Start is called before the first frame update
    void Start()
    {
        // Trouve tous les objets ayant le script Schedule attaché
        Schedule[] scriptsArray = FindObjectsOfType<Schedule>();
        scheduleScripts.AddRange(scriptsArray);
    }

    // Update is called once per frame
    void Update()
    {
        simulationTime += Time.deltaTime * accTime/3600;
        simulatedHour += Time.deltaTime * accTime/3600;
        if (simulatedHour >= 24)
        {
            //go to midnight
            simulatedHour = 0;

            //compute the new schedules
            foreach(Schedule schedule in scheduleScripts)
            {
                schedule.GenerateTodaySteps();
            }
        }
    }
}
