using UnityEngine;

public class DialogueManager : MonoBehaviour
{
    public static DialogueManager instance;

    public DialogueUIController uiController;

    private DialogueData currentDialogue;
    private DialogueNode currentNode;

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
        if (uiController == null)
        {
            uiController = FindObjectOfType<DialogueUIController>();
        }
    }

    public void StartDialogue(DialogueData dialogue)
    {
        if (dialogue == null)
        {
            Debug.LogError("StartDialogue called with null dialogue!");
            return;
        }

        currentDialogue = dialogue;
        currentNode = dialogue.GetStartNode();
        
        if (currentNode == null)
        {
            Debug.LogError("Start node is null!");
            return;
        }

        if (uiController != null)
        {
            uiController.ShowDialogue(currentNode);
            Time.timeScale = 0.0000001f;
        }
        else
        {
            Debug.LogError("UI Controller is not set!");
        }
    }

    public void ContinueDialogue()
    {
        if (currentDialogue == null || currentNode == null)
        {
            EndDialogue();
            return;
        }

        int currentIndex = currentDialogue.nodes.IndexOf(currentNode);
        if (currentIndex < currentDialogue.nodes.Count - 1)
        {
            currentNode = currentDialogue.nodes[currentIndex + 1];
            uiController.ShowDialogue(currentNode);
        }
        else
        {
            EndDialogue();
        }
    }

    public void SelectChoice(int choiceIndex)
    {
        if (currentNode == null || currentNode.choices == null)
        {
            EndDialogue();
            return;
        }

        if (choiceIndex >= 0 && choiceIndex < currentNode.choices.Count)
        {
            int nextIndex = currentNode.choices[choiceIndex].nextNodeIndex;
            currentNode = currentDialogue.GetNode(nextIndex);
            
            if (currentNode != null)
            {
                uiController.ShowDialogue(currentNode);
            }
            else
            {
                EndDialogue();
            }
        }
        else
        {
            EndDialogue();
        }
    }

    private void EndDialogue()
    {
        if (uiController != null)
        {
            uiController.HideDialogue();
        }
        currentDialogue = null;
        currentNode = null;
        Time.timeScale = 1f;
    }

    public bool IsDialogueActive()
    {
        return currentDialogue != null;
    }
}