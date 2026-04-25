using UnityEngine;
using TMPro;
using UnityEngine.UI;

public class PlayerDialogue : MonoBehaviour
{
    [Header("对话设置")]
    public string playerName = "Player";
    public float dialogueDelay = 1.5f; // 对话切换延迟

    [Header("对话内容")]
    [TextArea(3, 10)]
    public string[] dialogueLines;

    [Header("照片设置")]
    public Sprite playerPhoto;

    [Header("UI设置")]
    public GameObject dialogueUI;
    public TMP_Text nameText;
    public TMP_Text dialogueText;
    public Image photoImage;

    private bool isDialogueActive = false;
    private int currentLineIndex = 0;
    private float dialogueTimer = 0f;

    void Start()
    {
        // 初始化UI
        if (dialogueUI != null)
        {
            dialogueUI.SetActive(false);
        }

        if (photoImage != null)
        {
            photoImage.gameObject.SetActive(false);
        }
    }

    void Update()
    {
        // 对话中处理
        if (isDialogueActive)
        {
            dialogueTimer += Time.deltaTime;
            if (dialogueTimer >= dialogueDelay)
            {
                NextDialogue();
                dialogueTimer = 0f;
            }

            // 按空格键跳过对话
            if (Input.GetKeyDown(KeyCode.Space))
            {
                NextDialogue();
                dialogueTimer = 0f;
            }
        }
    }

    /// <summary>
    /// 开始对话
    /// </summary>
    public void StartDialogue()
    {
        if (dialogueLines == null || dialogueLines.Length == 0)
        {
            Debug.LogWarning("No dialogue lines set for player");
            return;
        }

        isDialogueActive = true;
        currentLineIndex = 0;
        dialogueTimer = 0f;

        // 显示对话UI
        if (dialogueUI != null)
        {
            dialogueUI.SetActive(true);
        }

        // 显示第一句对话
        DisplayDialogue();
    }

    /// <summary>
    /// 开始对话（使用指定的对话内容）
    /// </summary>
    /// <param name="lines">对话内容</param>
    public void StartDialogue(string[] lines)
    {
        if (lines == null || lines.Length == 0)
        {
            Debug.LogWarning("No dialogue lines provided");
            return;
        }

        dialogueLines = lines;
        StartDialogue();
    }

    /// <summary>
    /// 显示当前对话
    /// </summary>
    void DisplayDialogue()
    {
        if (dialogueText != null && currentLineIndex < dialogueLines.Length)
        {
            if (nameText != null)
            {
                nameText.text = playerName;
            }
            dialogueText.text = dialogueLines[currentLineIndex];

            // 显示玩家照片
            if (photoImage != null)
            {
                photoImage.gameObject.SetActive(true);
                photoImage.sprite = playerPhoto;
            }
        }
    }

    /// <summary>
    /// 下一句对话
    /// </summary>
    void NextDialogue()
    {
        currentLineIndex++;
        if (currentLineIndex < dialogueLines.Length)
        {
            DisplayDialogue();
        }
        else
        {
            EndDialogue();
        }
    }

    /// <summary>
    /// 结束对话
    /// </summary>
    void EndDialogue()
    {
        isDialogueActive = false;

        // 隐藏对话UI
        if (dialogueUI != null)
        {
            dialogueUI.SetActive(false);
        }

        if (photoImage != null)
        {
            photoImage.gameObject.SetActive(false);
        }
    }

    /// <summary>
    /// 检查是否正在对话
    /// </summary>
    /// <returns>是否正在对话</returns>
    public bool IsDialogueActive()
    {
        return isDialogueActive;
    }
}
