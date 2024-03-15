using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SwitchLights : MonoBehaviour
{
    public List<GameObject> Lamps;
    private int population;
    private int previousPopulation;
    private bool lightsOn = false;
    private bool turnOffTest = true;
    private TimeManager timeManager;
    private mqttController mqttController;
    private bool previousDayTime = false;
    [Range(0,1)]
    private float previousBestVigilance = 0;
    public float intensityThreshold;
    

    private Collider[] PresentPeople()
    {
        return Physics.OverlapBox(transform.position, transform.localScale / 2, transform.rotation);
    }

    //Checks if Schedule script is in the room and checks if the attached person is not asleep
        private bool IsPersonAwake()
    {
        Collider[] colliders = PresentPeople();
        foreach (Collider collider in colliders)
        {
            Schedule schedule = collider.GetComponent<Schedule>();
            if (schedule != null)
            {
                if (!schedule.getIsSleeping())
                {
                    return true;
                }
            }
        }
        return false;
    }

    private float bestVigilance()
    {
        float currentBestVigilance = 0;
        Collider[] colliders = PresentPeople();

        //For each person in the room
        foreach (Collider collider in colliders)
        {
            Schedule schedule = collider.GetComponent<Schedule>();
            if (schedule != null)
            {
                //Debug.Log("Is awake : " + !schedule.getIsSleeping());
                //Debug.Log("vigilance : " + schedule.vigilance);
                //If the person is more vigilant and is awake
                if (!schedule.getIsSleeping() && schedule.vigilance>currentBestVigilance)
                {
                    currentBestVigilance = schedule.vigilance;
                }
            }
        }

        return currentBestVigilance;
    }

    // Allume ou éteint les lampes en fonction de la présence du script Schedule
    public void ToggleLights(bool on)
    {
        foreach (GameObject lamp in Lamps)
        {
            Lamp lampScript = lamp.GetComponent<Lamp>();
            if (lampScript != null)
            {
                lampScript.TurnOn = on;
            }
        }
        //declare the person in an arriving or leaving state
        turnOffTest = on;
        lightsOn = on;
        previousBestVigilance = bestVigilance();
    }

    // Start is called before the first frame update
    void Start()
    {
        // Trouver le script TimeManager attaché à l'objet Clock
        GameObject clockObject = GameObject.Find("Clock");
        if (clockObject != null)
        {
            timeManager = clockObject.GetComponent<TimeManager>();
        }

        // Trouver le script mqttController attaché à l'objet Controller
        GameObject controllerObject = GameObject.Find("Controller");
        if (controllerObject != null)
        {
            mqttController = controllerObject.GetComponent<mqttController>();
        }
    }

    // Update is called once per frame
    void Update()
    {
        //ToggleLights(false);
        bool personAwake = IsPersonAwake();
        bool dayTime = false;

        //Detect if it is day or not
        if(mqttController.total_light_intensity>intensityThreshold)
        {
            dayTime = true;
        }

        //If it's nighttime and someone is awake in the room with lights turned off, they turn them on   
        if (!dayTime && personAwake && !lightsOn)
        {
            //Debug.Log("it's nighttime and someone is awake in the room with lights turned off, they turn them on");
            ToggleLights(true);
        }

        //If it's nighttime and the person is leaving and vigilant enough, they turn the light off
        else if (!dayTime && !personAwake && turnOffTest)
        {
            //Debug.Log("it's nighttime and if the person is leaving and vigilant enough, they turn the light off");
            //Case 1 : It is a new day, the person can potentially turn the lights off
            //Debug.Log("previousBestVigilance : " + previousBestVigilance);
            //Debug.Log(Random.NextDouble());
            if(previousBestVigilance>Random.Range(0f,1f))
            {
                ToggleLights(false);
            }

            //Declare the person in a leaving state, even if they left the lamps turned on
            turnOffTest = false;
        }

        //If there is a person in the room while night is beginning/ending
        if(previousDayTime != dayTime && personAwake){

            if(dayTime && previousBestVigilance>Random.Range(0f,1f))
            {
                ToggleLights(false);
                //Debug.Log("It is a new day, the person turns the lights off");
            }
            //Cas 2 : It is a new night, the person turns the lights on
            if(!dayTime)
            {
                ToggleLights(true);
                //Debug.Log("It is a new night, the person turns the lights on");
            }
            previousDayTime = dayTime;
        
        }
        
    }
}
