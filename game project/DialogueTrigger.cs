using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class DialogueTrigger : MonoBehaviour
{
    [Header("对话设置")]
    [SerializeField]
    private DialogueData dialogueData;

    [Header("触发设置")]
    [SerializeField]
    private bool triggerOnStart = false;

    [SerializeField]
    private KeyCode triggerKey = KeyCode.Q;

    [Header("交互提示设置")]
    [SerializeField]
    private bool showInteractionPrompt = true;

    [SerializeField]
    private string promptText = "按Q键开始对话";

    [SerializeField]
    private Color promptColor = Color.white;

    [SerializeField]
    private float promptOffsetY = 2f;

    [Header("一次性触发")]
    [SerializeField]
    private bool oneTimeInteraction = false;

    private bool hasInteracted = false;
    private GameObject promptObject;
    private TextMeshProUGUI promptTextComponent;

    private void Start()
    {
        if (triggerOnStart)
        {
            TriggerDialogue();
        }

        if (showInteractionPrompt)
        {
            CreatePrompt();
        }
    }

    private void CreatePrompt()
    {
        promptObject = new GameObject("InteractionPrompt");
        promptObject.transform.parent = transform;
        promptObject.transform.localPosition = new Vector3(0, promptOffsetY, 0);

        Canvas canvas = promptObject.AddComponent<Canvas>();
        canvas.renderMode = RenderMode.WorldSpace;
        canvas.sortingOrder = 100;

        CanvasScaler canvasScaler = promptObject.AddComponent<CanvasScaler>();
        canvasScaler.scaleFactor = 1f;
        canvasScaler.referenceResolution = new Vector2(1920, 1080);

        promptObject.AddComponent<GraphicRaycaster>();

        GameObject textObject = new GameObject("PromptText");
        textObject.transform.parent = promptObject.transform;
        textObject.transform.localPosition = Vector3.zero;
        textObject.transform.localScale = new Vector3(0.01f, 0.01f, 1f);

        promptTextComponent = textObject.AddComponent<TextMeshProUGUI>();
        promptTextComponent.text = promptText;
        promptTextComponent.color = promptColor;
        promptTextComponent.fontSize = 30;
        promptTextComponent.alignment = TextAlignmentOptions.Center;
        promptTextComponent.rectTransform.sizeDelta = new Vector2(200, 50);

        // 确保提示始终显示
        if (showInteractionPrompt)
        {
            promptObject.SetActive(true);
            Debug.Log("Interaction prompt created and activated");
        }
        else
        {
            promptObject.SetActive(false);
        }
    }

    private void Update()
    {
        if (Input.GetKeyDown(triggerKey) && !hasInteracted && !DialogueManager.instance.IsDialogueActive())
        {
            TriggerDialogue();
        }

        // 确保提示在对话结束后重新显示
        if (!DialogueManager.instance.IsDialogueActive() && showInteractionPrompt && !hasInteracted)
        {
            if (promptObject != null && !promptObject.activeSelf)
            {
                promptObject.SetActive(true);
            }
        }
        else if (DialogueManager.instance.IsDialogueActive() && promptObject != null)
        {
            promptObject.SetActive(false);
        }
    }

    public void TriggerDialogue()
    {
        if (dialogueData == null)
        {
            Debug.LogWarning("Dialogue data not set on DialogueTrigger");
            return;
        }

        if (oneTimeInteraction)
        {
            hasInteracted = true;
            if (promptObject != null)
            {
                promptObject.SetActive(false);
            }
        }

        if (DialogueManager.instance != null && !DialogueManager.instance.IsDialogueActive())
        {
            DialogueManager.instance.StartDialogue(dialogueData);
            if (promptObject != null)
            {
                promptObject.SetActive(false);
            }
        }
        else
        {
            Debug.LogWarning("DialogueManager instance not found or dialogue already active");
        }
    }

    // 公共方法
    public void SetDialogueData(DialogueData data)
    {
        dialogueData = data;
    }

    public void SetTriggerKey(KeyCode key)
    {
        triggerKey = key;
    }

    public void SetOneTimeInteraction(bool value)
    {
        oneTimeInteraction = value;
    }

    public void SetShowInteractionPrompt(bool value)
    {
        showInteractionPrompt = value;
        if (promptObject != null)
        {
            promptObject.SetActive(value && !hasInteracted);
        }
    }

    public void SetPromptText(string text)
    {
        promptText = text;
        if (promptTextComponent != null)
        {
            promptTextComponent.text = text;
        }
    }

    public void SetPromptColor(Color color)
    {
        promptColor = color;
        if (promptTextComponent != null)
        {
            promptTextComponent.color = color;
        }
    }

    public void SetPromptOffsetY(float offset)
    {
        promptOffsetY = offset;
        if (promptObject != null)
        {
            promptObject.transform.localPosition = new Vector3(0, promptOffsetY, 0);
        }
    }
}