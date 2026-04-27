using UnityEngine;
using System.Collections.Generic;

public class InteractionManager : MonoBehaviour
{
    public static InteractionManager instance;

    [SerializeField]
    private KeyCode interactKey = KeyCode.Q;

    [Header("UI设置")]
    [SerializeField]
    private GameObject interactionPrompt;
    [SerializeField]
    private TMPro.TextMeshProUGUI promptText;

    private InteractableItem closestInteractable;
    private List<InteractableItem> nearbyItems = new List<InteractableItem>();
    private Transform playerTransform;

    private void Awake()
    {
        if (instance == null)
        {
            instance = this;
        }
        else
        {
            Destroy(gameObject);
        }
    }

    private void Start()
    {
        FindPlayer();
        if (interactionPrompt != null)
        {
            interactionPrompt.SetActive(false);
        }
    }

    private void Update()
    {
        if (playerTransform == null)
        {
            FindPlayer();
            return;
        }

        FindClosestInteractable();

        if (closestInteractable != null)
        {
            ShowInteractionPrompt(closestInteractable);

            if (Input.GetKeyDown(interactKey))
            {
                closestInteractable.Interact();
            }
        }
        else
        {
            HideInteractionPrompt();
        }
    }

    private void FindPlayer()
    {
        GameObject player = GameObject.FindGameObjectWithTag("Player");
        if (player != null)
        {
            playerTransform = player.transform;
        }
    }

    private void FindClosestInteractable()
    {
        closestInteractable = null;
        float closestDistance = float.MaxValue;

        foreach (InteractableItem item in nearbyItems)
        {
            float distance = Vector2.Distance(playerTransform.position, item.transform.position);
            if (distance < closestDistance)
            {
                closestDistance = distance;
                closestInteractable = item;
            }
        }
    }

    private void ShowInteractionPrompt(InteractableItem item)
    {
        if (interactionPrompt != null && promptText != null)
        {
            interactionPrompt.SetActive(true);
            promptText.text = $"按 {interactKey.ToString()} 与 {item.GetItemName()} 互动";
        }
    }

    private void HideInteractionPrompt()
    {
        if (interactionPrompt != null)
        {
            interactionPrompt.SetActive(false);
        }
    }

    public void RegisterInteractable(InteractableItem item)
    {
        if (!nearbyItems.Contains(item))
        {
            nearbyItems.Add(item);
        }
    }

    public void UnregisterInteractable(InteractableItem item)
    {
        if (nearbyItems.Contains(item))
        {
            nearbyItems.Remove(item);
        }
    }
}
