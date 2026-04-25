using UnityEngine;
using TMPro;
using UnityEngine.UI;

public class NPCDialogue : MonoBehaviour
{
    [Header("对话设置")]
    public string npcName = "LinMo";
    public string playerName = "Player";
    public float interactionDistance = 2f;
    public float npcDialogueDelay = 1.5f;

    [Header("对话内容")]
    public string[] linmoLines = new string[0];
    public string[] playerLines = new string[0];

    [Header("照片设置")]
    public Sprite npcPhoto;
    public Sprite playerPhoto;

    [Header("主角回应")]
    public string[] playerResponseLines = new string[0];
    public GameObject player;
    private PlayerDialogue playerDialogue;

    [Header("UI设置")]
    public GameObject npcDialogueUI;
    public TMP_Text nameText;
    public TMP_Text npcDialogueText;
    public GameObject interactPrompt;
    public Button interactButton;
    public Image photoImage;

    private Transform playerTransform;
    private bool isPlayerNear = false;
    private bool npcDialogueActive = false;
    private int currentLineIndex = 0;
    private bool isLinMoSpeaking = true;
    private float npcDialogueTimer = 0f;

    void Start()
    {
        // 查找主角
        playerTransform = GameObject.FindWithTag("Player")?.transform;
        
        if (playerTransform == null)
        {
            Debug.LogError("Player not found! Make sure player has 'Player' tag.");
        }
        else
        {
            Debug.Log("Player found: " + playerTransform.name);
        }

        // 获取PlayerDialogue组件
        if (player != null)
        {
            playerDialogue = player.GetComponent<PlayerDialogue>();
            if (playerDialogue == null)
            {
                Debug.LogError("PlayerDialogue component not found on player");
            }
        }
        else
        {
            Debug.LogWarning("Player not assigned to NPCDialogue");
        }

        // 初始化UI
        if (npcDialogueUI != null)
        {
            npcDialogueUI.SetActive(false);
            Debug.Log("Dialogue UI initialized");
        }
        else
        {
            Debug.LogError("Dialogue UI not assigned");
        }

        if (interactPrompt != null)
        {
            interactPrompt.SetActive(false);
            Debug.Log("Interact prompt initialized");
        }
        else
        {
            Debug.LogError("Interact prompt not assigned");
        }

        if (interactButton != null)
        {
            interactButton.gameObject.SetActive(false);
            interactButton.onClick.AddListener(StartDialogue);
            Debug.Log("Interact button initialized");
        }
        else
        {
            Debug.LogError("Interact button not assigned");
        }

        if (photoImage != null)
        {
            photoImage.gameObject.SetActive(false);
            Debug.Log("Photo image initialized");
        }
        else
        {
            Debug.LogError("Photo image not assigned");
        }

        // 检查对话内容
        if (linmoLines == null || linmoLines.Length == 0)
        {
            Debug.LogWarning("LinMo lines not set");
        }
        if (playerLines == null || playerLines.Length == 0)
        {
            Debug.LogWarning("Player lines not set");
        }
        if (playerResponseLines == null || playerResponseLines.Length == 0)
        {
            Debug.LogWarning("Player response lines not set");
        }
    }

    void Update()
    {
        // 计算距离
        if (playerTransform != null)
        {
            float distance = Vector2.Distance(transform.position, playerTransform.position);
            isPlayerNear = distance <= interactionDistance;
            
            Debug.Log("Distance to player: " + distance + ", Interaction distance: " + interactionDistance + ", Is near: " + isPlayerNear);

            // 显示/隐藏交互提示和按钮
            bool shouldShowInteraction = isPlayerNear && !npcDialogueActive;
            
            if (interactPrompt != null)
            {
                interactPrompt.SetActive(shouldShowInteraction);
                Debug.Log("Showing interact prompt: " + shouldShowInteraction);
            }

            if (interactButton != null)
            {
                interactButton.gameObject.SetActive(shouldShowInteraction);
                Debug.Log("Showing interact button: " + shouldShowInteraction);
            }

            // 检测E键交互
            if (Input.GetKeyDown(KeyCode.E))
            {
                Debug.Log("E key pressed, isPlayerNear: " + isPlayerNear + ", isDialogueActive: " + npcDialogueActive);
                if (isPlayerNear && !npcDialogueActive)
                {
                    StartDialogue();
                }
            }
        }
        else
        {
            Debug.LogWarning("Player transform is null");
        }

        // 对话中处理
        if (npcDialogueActive)
        {
            npcDialogueTimer += Time.deltaTime;
            if (npcDialogueTimer >= npcDialogueDelay)
            {
                NextDialogue();
                npcDialogueTimer = 0f;
            }
        }
    }

    void StartDialogue()
    {
        npcDialogueActive = true;
        currentLineIndex = 0;
        isLinMoSpeaking = true;
        npcDialogueTimer = 0f;

        // 显示对话UI
        if (npcDialogueUI != null)
        {
            npcDialogueUI.SetActive(true);
            Debug.Log("Dialogue started");
        }
        if (interactPrompt != null)
        {
            interactPrompt.SetActive(false);
        }
        if (interactButton != null)
        {
            interactButton.gameObject.SetActive(false);
        }

        // 显示第一句对话
        DisplayDialogue();
    }

    void DisplayDialogue()
    {
        if (isLinMoSpeaking)
        {
            // LinMo的对话
            if (npcDialogueText != null && linmoLines != null && currentLineIndex < linmoLines.Length)
            {
                if (nameText != null)
                {
                    nameText.text = npcName;
                }
                npcDialogueText.text = linmoLines[currentLineIndex];
                Debug.Log("LinMo speaking: " + linmoLines[currentLineIndex]);

                // 显示NPC照片
                if (photoImage != null)
                {
                    photoImage.gameObject.SetActive(true);
                    photoImage.sprite = npcPhoto;
                }
            }
        }
        else
        {
            // Player的对话
            if (npcDialogueText != null && playerLines != null && currentLineIndex < playerLines.Length)
            {
                if (nameText != null)
                {
                    nameText.text = playerName;
                }
                npcDialogueText.text = playerLines[currentLineIndex];
                Debug.Log("Player speaking: " + playerLines[currentLineIndex]);

                // 显示玩家照片
                if (photoImage != null)
                {
                    photoImage.gameObject.SetActive(true);
                    photoImage.sprite = playerPhoto;
                }
            }
        }
    }

    void NextDialogue()
    {
        if (isLinMoSpeaking)
        {
            // LinMo的对话
            if (linmoLines != null)
            {
                currentLineIndex++;
                if (currentLineIndex < linmoLines.Length)
                {
                    DisplayDialogue();
                }
                else
                {
                    // LinMo说完，切换到Player
                    isLinMoSpeaking = false;
                    currentLineIndex = 0;
                    DisplayDialogue();
                }
            }
        }
        else
        {
            // Player的对话
            if (playerLines != null)
            {
                currentLineIndex++;
                if (currentLineIndex < playerLines.Length)
                {
                    DisplayDialogue();
                }
                else
                {
                    // 对话结束，触发主角回应
                    EndDialogue();
                }
            }
        }
    }

    void EndDialogue()
    {
        npcDialogueActive = false;

        // 隐藏对话UI
        if (npcDialogueUI != null)
        {
            npcDialogueUI.SetActive(false);
            Debug.Log("Dialogue ended");
        }

        if (photoImage != null)
        {
            photoImage.gameObject.SetActive(false);
        }

        // 触发主角回应
        if (playerDialogue != null && playerResponseLines != null && playerResponseLines.Length > 0)
        {
            Debug.Log("Triggering player response");
            playerDialogue.StartDialogue(playerResponseLines);
        }
    }
}
