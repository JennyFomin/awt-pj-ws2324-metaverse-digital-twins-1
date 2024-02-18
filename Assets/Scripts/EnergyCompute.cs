using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnergyCompute : MonoBehaviour
{
    // Liste pour stocker les scripts Energyconsumption trouvés dans la scène
    public List<GameObject> Lamps;
    public float GetTotalEnergy()
    {
        float totalEnergy = 0;
        

        // Parcours de tous les scripts Energyconsumption dans la liste
        foreach (GameObject lamp in Lamps)
        {
            Energyconsumption script = lamp.GetComponent<Energyconsumption>();

            // Ajoute la valeur d'énergie de chaque script à la somme totale
            totalEnergy += script.GetEnergy();
        }
        return totalEnergy;
    }

    // Start is called before the first frame update
    void Start()
    {

        // Ajoute ces scripts à la liste
    }

    // Update is called once per frame
    void Update()
    {
        // Appelle la méthode pour recalculer la somme de toutes les valeurs d'énergie
    }
}
