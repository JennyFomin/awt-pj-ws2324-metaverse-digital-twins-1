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
    
    public string energyDataTopic1;
    public string energyDataTopic2;
    public string simulationDataTopic1;
    public string simulationDataTopic2;

    private MqttClient client;

    private float energyConsumption1;
    private float energyConsumption2;
    public GameObject House1;
    public GameObject House2;
    private EnergyCompute energyCompute1;
    private EnergyCompute energyCompute2;
    private GameObject Clock;
    private TimeManager timeManager;

    private GameObject mqttControllerObject;
    private mqttController mqttControllerScript;

    public float energyPublishFrequency = 10;
    public float simulationPublishFrequency = 144;


    void Start()
    {
        // Create a new MQTT client instance
        client = new MqttClient(brokerHostname, brokerPort, false, null, null, MqttSslProtocols.None);
        
        // Register to MQTT events
        client.MqttMsgPublished += client_MqttMsgPublished;

        // Connect to the broker
        client.Connect(Guid.NewGuid().ToString());

        energyCompute1 = House1.GetComponent<EnergyCompute>();
        energyCompute2 = House2.GetComponent<EnergyCompute>();

        Clock = GameObject.Find("Clock");
        timeManager = Clock.GetComponent<TimeManager>();

        mqttControllerObject = GameObject.Find("Controller");
        mqttControllerScript = mqttControllerObject.GetComponent<mqttController>();
        
        // Start publishing at intervals of x seconds
        InvokeRepeating("PublishEnergyData", 0, energyPublishFrequency);
        InvokeRepeating("PublishSimulationData", 0, simulationPublishFrequency);
    }

    void PublishEnergyData()
    {
        energyConsumption1 = energyCompute1.GetTotalEnergy();
        EnergyData myEnergyObject1 = new EnergyData();
        myEnergyObject1.time_of_day = timeManager.simulatedHour;
        myEnergyObject1.total_light_intensity = mqttControllerScript.total_light_intensity;
        myEnergyObject1.total_energy_consumption = energyCompute1.GetTotalEnergy();
        string jsonEnergyObject1 = JsonUtility.ToJson(myEnergyObject1);
        Publish(jsonEnergyObject1, energyDataTopic1);

        energyConsumption2 = energyCompute2.GetTotalEnergy();
        EnergyData myEnergyObject2 = new EnergyData();
        myEnergyObject2.time_of_day = timeManager.simulatedHour;
        myEnergyObject2.total_light_intensity = mqttControllerScript.total_light_intensity;
        myEnergyObject2.total_energy_consumption = energyCompute2.GetTotalEnergy();
        string jsonEnergyObject2 = JsonUtility.ToJson(myEnergyObject2);
        Publish(jsonEnergyObject2, energyDataTopic2);
    }

    void PublishSimulationData()
    {
        energyConsumption1 = energyCompute1.GetTotalEnergy();
        SimulationData mySimulationObject1 = new SimulationData();
        mySimulationObject1.time_of_simulation = timeManager.getSimulationTime();
        mySimulationObject1.total_energy_consumption = energyCompute1.GetTotalEnergy();
        string jsonSimulationObject1 = JsonUtility.ToJson(mySimulationObject1);
        Publish(jsonSimulationObject1, simulationDataTopic1);

        energyConsumption2 = energyCompute2.GetTotalEnergy();
        SimulationData mySimulationObject2 = new SimulationData();
        mySimulationObject2.time_of_simulation = timeManager.getSimulationTime();
        mySimulationObject2.total_energy_consumption = energyCompute2.GetTotalEnergy();
        string jsonSimulationObject2 = JsonUtility.ToJson(mySimulationObject2);
        Publish(jsonSimulationObject2, simulationDataTopic2);
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
