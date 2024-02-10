using UnityEngine;

public class SunManager : MonoBehaviour
{
    private Light directionalLight;
    private TimeManager timeManager;
    Quaternion rotation;

    void setSunPosition()
    {
        rotation = Quaternion.Euler(timeManager.simulatedHour*360/24 - 90, 0, 0);
        transform.rotation = rotation;
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

        setSunPosition();
    }

    void Update()
    {
        setSunPosition();
    }
}
