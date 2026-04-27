using UnityEngine;
using System.Collections.Generic;

public class DialogueManager : MonoBehaviour
{
    public static DialogueManager instance;

    [Header("UI")]
    [SerializeField]
    private DialogueUIController uiController;

    private DialogueData currentDialogue;
    private DialogueNode currentNode;
    private bool isDialogueActive = false;

    private void Awake()
    {
        if (instance == null)
        {
            instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
    }

    public void SetUIController(DialogueUIController controller)
    {
        uiController = controller;
    }

    public void StartDialogue(DialogueData dialogue)
    {
        if (dialogue == null || dialogue.nodes == null || dialogue.nodes.Count == 0)
        {
            Debug.LogWarning("Invalid dialogue data");
            return;
        }

        // 解析节点引用
        dialogue.ResolveNodeReferences();

        currentDialogue = dialogue;
        currentNode = dialogue.GetStartNode();
        isDialogueActive = true;

        if (uiController != null)
        {
            uiController.ShowDialogueUI();
            uiController.DisplayDialogue(currentNode);
        }

        // 暂停游戏或禁用玩家输入
        Time.timeScale = 0.0000001f;
    }

    public void ContinueDialogue()
    {
        if (!isDialogueActive || currentNode == null)
        {
            return;
        }

        if (currentNode.choices != null && currentNode.choices.Count > 0)
        {
            // 如果有选项，等待玩家选择
            return;
        }

        // 如果是结束节点，结束对话
        if (currentNode.isEndNode)
        {
            EndDialogue();
            return;
        }

        // 简单的线性对话，移动到下一个节点
        int currentIndex = currentDialogue.nodes.IndexOf(currentNode);
        if (currentIndex < currentDialogue.nodes.Count - 1)
        {
            currentNode = currentDialogue.nodes[currentIndex + 1];
            if (uiController != null)
            {
                uiController.DisplayDialogue(currentNode);
            }
        }
        else
        {
            EndDialogue();
        }
    }

    public void SelectChoice(int choiceIndex)
    {
        if (!isDialogueActive || currentNode == null || currentNode.choices == null || choiceIndex >= currentNode.choices.Count)
        {
            return;
        }

        DialogueChoice selectedChoice = currentNode.choices[choiceIndex];
        if (selectedChoice.nextNode != null)
        {
            currentNode = selectedChoice.nextNode;
            if (uiController != null)
            {
                uiController.DisplayDialogue(currentNode);
            }
        }
        else
        {
            EndDialogue();
        }
    }

    public void EndDialogue()
    {
        isDialogueActive = false;
        currentDialogue = null;
        currentNode = null;

        if (uiController != null)
        {
            uiController.HideDialogueUI();
        }

        // 恢复游戏或启用玩家输入
        Time.timeScale = 1f;
    }

    public bool IsDialogueActive()
    {
        return isDialogueActive;
    }

    public void SetDialogueData(DialogueData data)
    {
        currentDialogue = data;
    }

    public DialogueData GetCurrentDialogue()
    {
        return currentDialogue;
    }

    public DialogueNode GetCurrentNode()
    {
        return currentNode;
    }
}