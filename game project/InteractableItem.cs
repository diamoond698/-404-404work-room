using UnityEngine;

public class InteractableItem : MonoBehaviour
{
    public string itemName;
    public float interactRange = 2f;
    public bool oneTimeInteraction = false;
    public DialogueData dialogueData;
    public bool showIndicator = true;
    public Color highlightColor = Color.yellow;

    private bool playerInRange = false;
    private bool hasInteracted = false;
    private SpriteRenderer spriteRenderer;
    private Color originalColor;

    private void Start()
    {
        spriteRenderer = GetComponent<SpriteRenderer>();
        if (spriteRenderer != null)
        {
            originalColor = spriteRenderer.color;
        }
    }

    private void Update()
    {
        if (playerInRange && Input.GetKeyDown(KeyCode.Q) && !hasInteracted && !DialogueManager.instance.IsDialogueActive())
        {
            Interact();
        }
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (other.CompareTag("Player"))
        {
            playerInRange = true;
            if (showIndicator && spriteRenderer != null)
            {
                spriteRenderer.color = highlightColor;
            }
        }
    }

    private void OnTriggerExit2D(Collider2D other)
    {
        if (other.CompareTag("Player"))
        {
            playerInRange = false;
            if (spriteRenderer != null)
            {
                spriteRenderer.color = originalColor;
            }
        }
    }

    public void Interact()
    {
        if (dialogueData != null)
        {
            DialogueManager.instance.StartDialogue(dialogueData);
        }

        if (oneTimeInteraction)
        {
            hasInteracted = true;
        }
    }

    public string GetItemName()
    {
        return itemName;
    }
}