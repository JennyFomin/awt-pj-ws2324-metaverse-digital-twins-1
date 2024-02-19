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
  public string tagOfTheMQTTReceiver="MQTT_Receiver";
  public mqttReceiver _eventSender;

    public float time_of_day;
    public float total_light_intensity;
    public GameObject clockObject;
    private TimeManager timeManager;

  void Start()
  {
    //textMeshPro = this.GetComponent<TextMeshPro>();

    _eventSender=GameObject.FindGameObjectsWithTag(tagOfTheMQTTReceiver)[0].gameObject.GetComponent<mqttReceiver>();
    _eventSender.OnMessageArrived += OnMessageArrivedHandler;
    timeManager = clockObject.GetComponent<TimeManager>();
  }

  private void OnMessageArrivedHandler(string newMsg)
{
      
        // Désérialiser la chaîne JSON en un objet MessageData
        MessageData data = JsonUtility.FromJson<MessageData>(newMsg);

        // Récupérer les valeurs de time_of_day et light_intensity de l'objet MessageData
        if(data.time_of_day!=0 && data.total_light_intensity!=null)
        {
          Debug.Log(data.time_of_day);
        time_of_day = data.time_of_day;
        total_light_intensity = data.total_light_intensity;

        // Modifier la variable simulatedHour dans le script TimeManager de l'objet Clock
        if (timeManager != null)
        {
            timeManager.simulatedHour = time_of_day;
        }
        }
    }
}
