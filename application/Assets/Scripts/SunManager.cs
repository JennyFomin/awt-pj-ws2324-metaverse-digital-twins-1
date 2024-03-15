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
        // Find the attached directional light
        directionalLight = GetComponent<Light>();

        // Find the script TimeManager attaches to Clock
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
