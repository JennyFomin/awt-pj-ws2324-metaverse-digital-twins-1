using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Energyconsumption : MonoBehaviour
{
    // Reference to the Lamp.cs script attached to the same object
    private Lamp lampScript;

    // Power of the lamp
    public float Power = 10.0f;

    // Consumed energy in W.s
    private float energy = 0.0f;

    // Obtain current energy value
    public float GetEnergy()
    {
        return energy;
    }

    // Access the time acceleration
    private TimeManager timeManager;

    // Start is called before the first frame update
    void Start()
    {
        lampScript = GetComponent<Lamp>();

        // Find the TimeManager script attached to the Clock object
        GameObject clockObject = GameObject.Find("Clock");
        if (clockObject != null)
        {
            timeManager = clockObject.GetComponent<TimeManager>();
        }
    }

    // Update is called once per frame
    void Update()
    {
        // Check if the lamp is turned on (TurnOn is true)
        if (lampScript != null && lampScript.TurnOn)
        {
            // Calculate energy consumed in Watt-seconds and add it
            float energyConsumed = Power * Time.deltaTime * timeManager.accTime;
            energy += energyConsumed; 
        }
    }
}
