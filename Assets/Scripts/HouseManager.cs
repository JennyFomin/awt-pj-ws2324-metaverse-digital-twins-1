using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HouseManager : MonoBehaviour
{
    public List<GameObject> Rooms;
    public bool connectedSensor = false;
    [Range(0,1)]
    public float intensityThreshold;
    public GameObject MqttControllerObject;
    private mqttController mqttController;
    private float total_light_intensity;
    private float energyConsumption;
    
    public void ToggleAllLights(bool on)
    {
        
        foreach(GameObject room in Rooms)
        {
            SwitchLights switchLight = room.GetComponent<SwitchLights>();
            switchLight.ToggleLights(on);
        }
    }

    // Start is called before the first frame update
    void Start()
{
    if (MqttControllerObject != null)
    {
        mqttController = MqttControllerObject.GetComponent<mqttController>();
    }

    foreach(GameObject room in Rooms)
        {
            SwitchLights switchLight = room.GetComponent<SwitchLights>();
            switchLight.intensityThreshold = intensityThreshold;
        }
}

    // Update is called once per frame
    void Update()
    {
        total_light_intensity = mqttController.total_light_intensity;
        //Switch off lights with light sensor
        if(connectedSensor && total_light_intensity>intensityThreshold)
        {
            ToggleAllLights(false);
        }
    }
}