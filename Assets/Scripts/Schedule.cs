using System.Collections;
using System.Collections.Generic;
using UnityEngine;


[System.Serializable]
public class Step
{
    public string Name;             // Nom de l'étape
    [Range(0, 24)]
    public float Date;              // Heure de l'étape (entre 0 et 24)
    public GameObject Area;         // Référence au GameObject de la pièce
    public bool Sleeping = false;   // Par défaut, Sleeping est à False
}

public class Schedule : MonoBehaviour
{
    
     // Liste originale des étapes
    public List<Step> Steps = new List<Step>();
    public float speed = 0.05f; // Vitesse de déplacement
    public float Punctuality = 0.0f;

    // Liste des étapes pour aujourd'hui
    private List<Step> TodaySteps = new List<Step>();
    private int currentStepIndex = 0;
    private Step currentStep;
    private bool isSleeping = true;
    private bool isStandingUp = false;

    public bool getIsSleeping()
    {
        return isSleeping;
    }
    public Step getCurrentStep()
    {
        return currentStep;
    }
    private GameObject Area;
    
    private TimeManager timeManager;
    public List<Step> GetTodaySteps()
    {
        return TodaySteps;
    }
    public void GenerateTodaySteps()
    {
        TodaySteps.Clear(); // Assurez-vous que la liste est vide avant de la remplir à nouveau

        float previousDate = 0.0f;

        foreach (Step step in Steps)
        {
            // Génère une nouvelle date aléatoire dans les limites spécifiées
            float randomDate = Mathf.Clamp(step.Date + Random.Range(-Punctuality, Punctuality), 0.0f, 24.0f);

            // Assurez-vous que chaque date générée est supérieure ou égale à la date précédente
            randomDate = Mathf.Max(randomDate, previousDate);

            // Ajoute la nouvelle étape à la liste des étapes pour aujourd'hui
            TodaySteps.Add(new Step
            {
                Name = step.Name,
                Date = randomDate,
                Area = step.Area,
                Sleeping = step.Sleeping
            });

            // Met à jour la date précédente pour la prochaine itération
            previousDate = randomDate;
        }
    }

    bool IsInsideArea()
    {
        Collider collider = Area.GetComponent<Collider>();
        if (collider != null)
        {
            return collider.bounds.Contains(transform.position);
        }
        return false;
    }

    private Quaternion standRotation; // Rotation debout
    private Quaternion lieDownRotation; // Rotation allongée

    [Range(0, 1)]
    public float vigilance = 0;

    void Start()
    {
        GenerateTodaySteps();

        // Trouver le script TimeManager attaché à l'objet Clock
        GameObject clockObject = GameObject.Find("Clock");
        if (clockObject != null)
        {
            timeManager = clockObject.GetComponent<TimeManager>();
        }

        if (TodaySteps.Count > 0)
        {
            currentStep = TodaySteps[0];
            Area = currentStep.Area;
        }

        // Déterminer la rotation de départ (debout)
        standRotation = transform.rotation;

        // Calculer la rotation allongée en tournant vers le bas de 90 degrés autour de l'axe X
        lieDownRotation = Quaternion.Euler(90f, transform.rotation.eulerAngles.y, transform.rotation.eulerAngles.z);

    }

    // Update is called once per frame
    void Update()
    {
        if(TodaySteps.Count>currentStepIndex+1)
        {
            if(timeManager.simulatedHour > TodaySteps[currentStepIndex + 1].Date)
            {
                currentStepIndex++;
                currentStep = TodaySteps[currentStepIndex];
                Area = currentStep.Area;

            }
        };

        if(currentStepIndex > 0)
        {
            if(timeManager.simulatedHour < TodaySteps[currentStepIndex].Date)
            {
                currentStepIndex = 0;
                currentStep = TodaySteps[currentStepIndex];
                Area = currentStep.Area;
            }
        };

        // Vérifier si le GameObject Area est défini
        if (Area != null)
        {
            // Vérifier si le personnage n'est pas déjà à l'intérieur de l'Area
            if (!IsInsideArea() && !isSleeping)
            {
                // Calculer la direction vers laquelle se déplacer
                Vector3 targetDirection = Area.transform.position - transform.position;
                targetDirection.y = 0f; // Garder la direction sur le plan horizontal

                // Normaliser la direction
                targetDirection.Normalize();

                // Calculer la position vers laquelle se déplacer
                Vector3 targetPosition = transform.position + targetDirection * speed * Time.deltaTime * timeManager.accTime ;

                // Déplacer le personnage vers la position cible
                transform.position = Vector3.MoveTowards(transform.position, targetPosition, speed * Time.deltaTime * timeManager.accTime);

                // Calculer la rotation vers la direction du déplacement
                Quaternion targetRotation = Quaternion.LookRotation(targetDirection);

                // Appliquer la rotation au personnage
                transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, Time.deltaTime * 0.01f * timeManager.accTime);
            }
            else
            {
                // Vérifier si l'étape actuelle indique que le personnage doit dormir
                if (currentStep != null && currentStep.Sleeping)
                {
                    // Le personnage s'allonge et ne peut plus se déplacer
                    isSleeping = true;
                    // Rotation progressive vers la position allongée
                    transform.rotation = Quaternion.Slerp(transform.rotation, lieDownRotation, Time.deltaTime * 0.005f * timeManager.accTime);
                    isStandingUp = false;

                }
                else if(!isStandingUp)
                {
                    transform.rotation = Quaternion.Slerp(transform.rotation, standRotation, Time.deltaTime * 0.005f * timeManager.accTime);
                    // Si la rotation est presque terminée
                    if (Quaternion.Angle(transform.rotation, standRotation) < 1f)
                    {
                        // Remettre isSleeping à false
                        isSleeping = false;
                        // Mettre à jour la variable de contrôle de lever
                        isStandingUp = true;
                    }

                }
            }
        }
    //Debug.Log("Current step ("+currentStepIndex+"/"+TodaySteps.Count+"): "+currentStep.Name);
    }
}