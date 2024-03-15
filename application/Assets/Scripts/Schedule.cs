using System.Collections;
using System.Collections.Generic;
using UnityEngine;


[System.Serializable]
public class Step
{
    public string Name;             // Name of the step
    [Range(0, 24)]
    public float Date;              // Time of the step (between 0 and 24)
    public GameObject Area;         // Reference to the room's GameObject
    public bool Sleeping = false;   // By default, Sleeping is set to False
}

public class Schedule : MonoBehaviour
{
    public GameObject House;
    private HouseManager houseManager;
    // Original list of steps
    public List<Step> Steps = new List<Step>();
    public float speed = 0.05f; // Movement speed
    public float Punctuality = 0.0f;

    // List of steps for today
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
        TodaySteps.Clear(); // Make sure the list is empty before filling it again

        float previousDate = 0.0f;

        foreach (Step step in Steps)
        {
            // Generate a new random date within specified limits
            float randomDate = Mathf.Clamp(step.Date + Random.Range(-Punctuality, Punctuality), 0.0f, 24.0f);

            // Ensure each generated date is greater than or equal to the previous date
            randomDate = Mathf.Max(randomDate, previousDate);

            // Add the new step to the list of steps for today
            TodaySteps.Add(new Step
            {
                Name = step.Name,
                Date = randomDate,
                Area = step.Area,
                Sleeping = step.Sleeping
            });

            // Update the previous date for the next iteration
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

    private Quaternion standRotation; // Standing rotation
    private Quaternion lieDownRotation; // Lying down rotation

    [Range(0, 1)]
    public float vigilance = 0;

    void StepChange()
    {
        currentStep = TodaySteps[currentStepIndex];
        Area = currentStep.Area;

        //checks if he goes to work
        if (currentStep.Name == "Work")
        {
            houseManager.ToggleAllLights(false);
        }
    }

    void Start()
    {
        if (House != null)
        {
            houseManager = House.GetComponent<HouseManager>();
        }
        GenerateTodaySteps();

        // Find the TimeManager script attached to the Clock object
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

        // Determine the starting rotation (standing)
        standRotation = transform.rotation;

        // Calculate lying down rotation by rotating down 90 degrees around the X axis
        lieDownRotation = Quaternion.Euler(90f, transform.rotation.eulerAngles.y, transform.rotation.eulerAngles.z);
    }

    // Update is called once per frame
    void Update()
    {
        if (TodaySteps.Count > currentStepIndex + 1)
        {
            if (timeManager.simulatedHour > TodaySteps[currentStepIndex + 1].Date)
            {
                currentStepIndex++;
                StepChange();
            }
        };

        if (currentStepIndex > 0)
        {
            if (timeManager.simulatedHour < TodaySteps[currentStepIndex].Date)
            {
                currentStepIndex = 0;
                StepChange();
            }
        };

        // Check if the GameObject Area is defined
        if (Area != null)
        {
            // Check if the character is not already inside the Area
            if (!IsInsideArea() && !isSleeping)
            {
                // Calculate the direction to move towards
                Vector3 targetDirection = Area.transform.position - transform.position;
                targetDirection.y = 0f; // Keep the direction on the horizontal plane

                // Normalize the direction
                targetDirection.Normalize();

                // Calculate the position to move towards
                Vector3 targetPosition = transform.position + targetDirection * speed * Time.deltaTime * timeManager.accTime;

                // Move the character towards the target position
                transform.position = Vector3.MoveTowards(transform.position, targetPosition, speed * Time.deltaTime * timeManager.accTime);

                // Calculate the rotation towards the direction of movement
                Quaternion targetRotation = Quaternion.LookRotation(targetDirection);

                // Apply the rotation to the character
                transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, Time.deltaTime * 0.01f * timeManager.accTime);
            }
            else
            {
                // Check if the current step indicates that the character should sleep
                if (currentStep != null && currentStep.Sleeping)
                {
                    // The character lies down and can no longer move
                    isSleeping = true;
                    // Progressive rotation towards lying position
                    transform.rotation = Quaternion.Slerp(transform.rotation, lieDownRotation, Time.deltaTime * 0.5f * timeManager.accTime);
                    isStandingUp = false;

                }
                else if (!isStandingUp)
                {
                    transform.rotation = Quaternion.Slerp(transform.rotation, standRotation, Time.deltaTime * 0.5f * timeManager.accTime);
                    // If the rotation is nearly complete
                    if (Quaternion.Angle(transform.rotation, standRotation) < 1f)
                    {
                        // Set isSleeping back to false
                        isSleeping = false;
                        // Update the standing up control variable
                        isStandingUp = true;
                    }

                }
            }
        }
    }
}
