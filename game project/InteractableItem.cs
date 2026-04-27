using UnityEngine;

public class InteractableItem : MonoBehaviour
{
    [Header("互动设置")]
    [SerializeField]
    private string itemName = "物品";
    [SerializeField]
    private KeyCode interactKey = KeyCode.Q;
    [SerializeField]
    private float interactRange = 2f;
    [SerializeField]
    private bool showIndicator = true;

    [Header("剧情设置")]
    [SerializeField]
    private DialogueData dialogueData;
    [SerializeField]
    private bool oneTimeInteraction = false;
    [SerializeField]
    private bool hasInteracted = false;

    [Header("视觉效果")]
    [SerializeField]
    private Sprite indicatorSprite;
    [SerializeField]
    private Color highlightColor = Color.yellow;

    private SpriteRenderer spriteRenderer;
    private GameObject indicator;
    private Color originalColor;
    private bool playerInRange;

    private void Start()
    {
        spriteRenderer = GetComponent<SpriteRenderer>();
        if (spriteRenderer != null)
        {
            originalColor = spriteRenderer.color;
        }

        CreateIndicator();
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (other.CompareTag("Player"))
        {
            playerInRange = true;
            if (InteractionManager.instance != null)
            {
                InteractionManager.instance.RegisterInteractable(this);
            }
        }
    }

    private void OnTriggerExit2D(Collider2D other)
    {
        if (other.CompareTag("Player"))
        {
            playerInRange = false;
            if (InteractionManager.instance != null)
            {
                InteractionManager.instance.UnregisterInteractable(this);
            }
        }
    }

    private void CreateIndicator()
    {
        if (!showIndicator) return;

        indicator = new GameObject("InteractionIndicator");
        indicator.transform.parent = transform;
        indicator.transform.localPosition = new Vector3(0, 1.5f, 0);

        SpriteRenderer indicatorRenderer = indicator.AddComponent<SpriteRenderer>();
        if (indicatorSprite != null)
        {
            indicatorRenderer.sprite = indicatorSprite;
        }
        indicatorRenderer.sortingLayerName = "UI";
        indicatorRenderer.sortingOrder = 10;

        indicator.SetActive(false);
    }

    public void Interact()
    {
        if (hasInteracted && oneTimeInteraction) return;

        if (dialogueData != null && DialogueManager.instance != null)
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

    public bool IsPlayerInRange()
    {
        return playerInRange && !hasInteracted;
    }

    public bool HasInteracted()
    {
        return hasInteracted;
    }

    public void ResetInteraction()
    {
        hasInteracted = false;
    }

    public void SetDialogueData(DialogueData data)
    {
        dialogueData = data;
    }

    private void OnDrawGizmosSelected()
    {
        Gizmos.color = Color.cyan;
        Gizmos.DrawWireSphere(transform.position, interactRange);
    }
}
