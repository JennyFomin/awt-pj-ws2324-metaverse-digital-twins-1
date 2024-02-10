using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnergyCompute : MonoBehaviour
{
    // Liste pour stocker les scripts Energyconsumption trouvés dans la scène
    private List<Energyconsumption> energyConsumptionScripts = new List<Energyconsumption>();

    // Méthode pour calculer et afficher la somme de toutes les valeurs d'énergie
    private void ComputeTotalEnergy()
    {
        float totalEnergy = 0.0f;

        // Parcours de tous les scripts Energyconsumption dans la liste
        foreach (Energyconsumption script in energyConsumptionScripts)
        {
            // Ajoute la valeur d'énergie de chaque script à la somme totale
            totalEnergy += script.GetEnergy();
        }

        // Affiche la somme totale en temps réel
        //Debug.Log("Total energy consumption : " + totalEnergy + " W.s");
    }


    // Start is called before the first frame update
    void Start()
    {
        // Trouve tous les objets ayant le script Energyconsumption attaché
        Energyconsumption[] scriptsArray = FindObjectsOfType<Energyconsumption>();

        // Ajoute ces scripts à la liste
        energyConsumptionScripts.AddRange(scriptsArray);
    }

    // Update is called once per frame
    void Update()
    {
        // Appelle la méthode pour recalculer la somme de toutes les valeurs d'énergie
        ComputeTotalEnergy();
    }
}
