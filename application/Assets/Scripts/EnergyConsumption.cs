using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Energyconsumption : MonoBehaviour
{
    // Référence au script Lamp.cs attaché au même objet
    private Lamp lampScript;

    // Power of the lamp
    public float Power = 10.0f;

    // Consumed energy in W.s
    private float energy = 0.0f;

    //Obtain current energy value
    public float GetEnergy()
    {
        return energy;
    }

    //Avoir l'accélération du temps
    private TimeManager timeManager;

    // Start is called before the first frame update
    void Start()
    {
        // Assurez-vous que le script Lamp.cs est attaché au même objet
        lampScript = GetComponent<Lamp>();

        // Trouver le script TimeManager attaché à l'objet Clock
        GameObject clockObject = GameObject.Find("Clock");
        if (clockObject != null)
        {
            timeManager = clockObject.GetComponent<TimeManager>();
        }
        
    }

    // Update is called once per frame
    void Update()
    {
        // Vérifiez si la lampe est allumée (TurnOn est vrai)
        if (lampScript != null && lampScript.TurnOn)
        {
            // Calculez l'énergie consommée en Watt-seconde et ajoutez-la
            float energyConsumed = Power * Time.deltaTime * timeManager.accTime;
            energy += energyConsumed;

            // Vous pouvez également effectuer d'autres actions ici liées à la consommation d'énergie
            // Par exemple, mettre à jour un panneau d'informations, déclencher des événements, etc.

            
        }
        //Debug.Log("Consumed energy : " + energy + " W.s");
    }
}
