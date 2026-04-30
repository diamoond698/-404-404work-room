using UnityEngine;

public class SimpleDialogueTrigger : MonoBehaviour
{
    public DialogueData dialogueData;
    public KeyCode triggerKey = KeyCode.Q;

    private bool hasTriggered = false;

    private void Update()
    {
        if (Input.GetKeyDown(triggerKey) && !hasTriggered && !DialogueManager.instance.IsDialogueActive())
        {
            TriggerDialogue();
        }
    }

    private void TriggerDialogue()
    {
        if (dialogueData == null)
        {
            Debug.LogError("Dialogue Data is not set!");
            return;
        }

        if (DialogueManager.instance == null)
        {
            Debug.LogError("DialogueManager instance not found!");
            return;
        }

        DialogueManager.instance.StartDialogue(dialogueData);
        hasTriggered = true;
    }

    public void ResetTrigger()
    {
        hasTriggered = false;
    }
}