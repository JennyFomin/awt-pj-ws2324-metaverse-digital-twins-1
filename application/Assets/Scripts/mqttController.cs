using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

[System.Serializable]
public class MessageData
{
    public float time_of_day;
    public float total_light_intensity;
}

public class mqttController : MonoBehaviour
{
    public string nameController = "Controller 1";
    public string tagOfTheMQTTReceiver = "MQTT_Receiver";
    public mqttReceiver _eventSender;

    public float time_of_day;
    public float total_light_intensity;
    public GameObject clockObject;
    private TimeManager timeManager;

    void Start()
    {
        //textMeshPro = this.GetComponent<TextMeshPro>();

        _eventSender = GameObject.FindGameObjectsWithTag(tagOfTheMQTTReceiver)[0].gameObject.GetComponent<mqttReceiver>();
        _eventSender.OnMessageArrived += OnMessageArrivedHandler;
        timeManager = clockObject.GetComponent<TimeManager>();
    }

    private void OnMessageArrivedHandler(string newMsg)
    {
        // Deserialize the JSON string into a MessageData object
        MessageData data = JsonUtility.FromJson<MessageData>(newMsg);

        // Retrieve the values of time_of_day and light_intensity from the MessageData object
        if (data.time_of_day != 0 && data.total_light_intensity != null)
        {
            Debug.Log(data.time_of_day);
            time_of_day = data.time_of_day;
            total_light_intensity = data.total_light_intensity;

            // Modify the simulatedHour variable in the TimeManager script of the Clock object
            if (timeManager != null)
            {
                timeManager.simulatedHour = time_of_day;
            }
        }
    }
}
