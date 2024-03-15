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
        foreach (Collider collider in colliders)
        {
            Schedule schedule = collider.GetComponent<Schedule>();
            if (schedule != null)
            {
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
        turnOffTest = on;
        lightsOn = on;
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
        bool personPresent = IsPersonAwake();
        bool dayTime = false;
        if(mqttController.total_light_intensity>intensityThreshold)
        {
            dayTime = true;
        }
        if (!dayTime && personPresent && !lightsOn)
        {
            ToggleLights(true);
        }
        else if (!dayTime && !personPresent && turnOffTest)
        {
            if(bestVigilance()>Random.Range(0,1))
            {
                ToggleLights(false);
            }
            turnOffTest = false;
        }

        //Eteinte automatique des lumières
        //if(previousDayTime != dayTime && dayTime && connectedSensor)
        //{
        //    ToggleLights(false);
        //}

        //Eteindre/allumer la lumière lorsque le jour se lève ou que la nuit tombe
        if(previousDayTime != dayTime && personPresent){

            //Cas 1 : le jour se lève, la personne peut potentiellement éteindre la lumière
            if(dayTime && bestVigilance()>Random.Range(0,1))
            {
                ToggleLights(false);
            }
            //Cas 2 : la nuit tombe, la personne allume directement la lumière
            else
            {
                ToggleLights(true);
            }
            previousDayTime = dayTime;
        }
    }
}
