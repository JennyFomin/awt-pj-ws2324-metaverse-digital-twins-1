using UnityEngine;

public class SunManager : MonoBehaviour
{
    private Light directionalLight;
    private TimeManager timeManager;
    Quaternion rotation;
    
    private mqttController mqttControllerScript;

    void setSunPosition()
    {
        rotation = Quaternion.Euler(timeManager.simulatedHour*360/24 - 90, 0, 0);
        transform.rotation = rotation;
    }

    void setSunIntensity()
    {
        directionalLight.intensity = mqttControllerScript.total_light_intensity;
    }
    
    void Start()
    {
        // Trouver la lumière directionnelle attachée à cet objet
        directionalLight = GetComponent<Light>();

        // Trouver le script TimeManager attaché à l'objet Clock
        GameObject clockObject = GameObject.Find("Clock");
        if (clockObject != null)
        {
            timeManager = clockObject.GetComponent<TimeManager>();
        }
        GameObject mqttControllerObject = GameObject.Find("Controller");
        if (mqttControllerObject != null)
        {
            mqttControllerScript = mqttControllerObject.GetComponent<mqttController>();
        }


        //setSunPosition();
        setSunIntensity();
    }

    void Update()
    {
        //setSunPosition();
        setSunIntensity();
    }
}
