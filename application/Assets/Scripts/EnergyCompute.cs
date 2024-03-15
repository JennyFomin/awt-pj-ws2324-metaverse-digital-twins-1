using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnergyCompute : MonoBehaviour
{
    // List to store Energyconsumption scripts found in the scene
    public List<GameObject> Lamps;
    
    public float GetTotalEnergy()
    {
        float totalEnergy = 0;
        
        // Iterates through all Energyconsumption scripts in the list
        foreach (GameObject lamp in Lamps)
        {
            Energyconsumption script = lamp.GetComponent<Energyconsumption>();
            
            // Adds the energy value of each script to the total sum
            totalEnergy += script.GetEnergy();
        }
        return totalEnergy;
    }

    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
    }
}
