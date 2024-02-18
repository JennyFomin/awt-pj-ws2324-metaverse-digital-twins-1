using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class mqttController : MonoBehaviour
{


  public string nameController = "Controller 1";
  public string tagOfTheMQTTReceiver="";
  public mqttReceiver _eventSender;

  public TextMeshPro textMeshPro;
  void Start()
  {
    textMeshPro = this.GetComponent<TextMeshPro>();

    _eventSender=GameObject.FindGameObjectsWithTag(tagOfTheMQTTReceiver)[0].gameObject.GetComponent<mqttReceiver>();
    _eventSender.OnMessageArrived += OnMessageArrivedHandler;
  }

  private void OnMessageArrivedHandler(string newMsg)
  {

    textMeshPro.text=newMsg;
    Debug.Log("Event Fired. The message, from Object " +nameController+" is = " + newMsg);
  }
}
