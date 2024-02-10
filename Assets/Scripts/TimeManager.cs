using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TimeManager : MonoBehaviour
{
    [Range(0, 24)]
    public float simulatedHour = 0;
    [Range(0, 24)]
    public float sunrise;
    [Range(0, 24)]
    public float sunset;
    public float accTime = 1;
    private bool dayTime = false;
    public bool isDayTime(){
        return dayTime;
    }

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
        simulatedHour += Time.deltaTime * accTime/3600;
        if(dayTime == false && (simulatedHour > sunrise && simulatedHour < sunset))
        {
            dayTime = true;
        }
        else if(dayTime == true && (simulatedHour < sunrise || simulatedHour > sunset))
        {
            dayTime = false;
        }

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
