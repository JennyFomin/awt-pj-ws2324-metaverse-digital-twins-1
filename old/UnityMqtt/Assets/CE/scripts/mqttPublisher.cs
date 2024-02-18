using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;

public class MqttPublisher : MonoBehaviour
{
    public string brokerHostname = "localhost";
    public int brokerPort = 1883;
    
    public string energyDataTopic = "smart_home/energy_data";
    public string simulationDataTopic = "smart_home/simulation_data";

    private MqttClient client;

    void Start()
    {
        // Create a new MQTT client instance
        client = new MqttClient(brokerHostname, brokerPort, false, null, null, MqttSslProtocols.None);
        
        // Register to MQTT events
        client.MqttMsgPublished += client_MqttMsgPublished;

        // Connect to the broker
        client.Connect(Guid.NewGuid().ToString());
    }

    void Update()
    {
        EnergyData myEnergyObject = new EnergyData();
            myEnergyObject.time_of_day = 1.0;
            myEnergyObject.total_light_intensity = 0.12;
            myEnergyObject.total_energy_consumption = 12.567
            string jsonEnergyObject = JsonUtility.ToJson(myEnergyObject);
            Publish(jsonEnergyObject, energyDataTopic); // Sendet eine Testnachricht
    }

    public void Publish(string _message, string topic)
    {
        if (client.IsConnected)
        {
            // Publish a message to the specified topic
            client.Publish(topic, System.Text.Encoding.UTF8.GetBytes(_message), MqttMsgBase.QOS_LEVEL_AT_LEAST_ONCE, false);
        }
    }

    private void client_MqttMsgPublished(object sender, MqttMsgPublishedEventArgs e)
    {
        Debug.Log("Message published with ID: " + e.MessageId);
    }

    void OnDisable()
    {
        if (client.IsConnected)
        {
            client.Disconnect();
        }
    }
}
