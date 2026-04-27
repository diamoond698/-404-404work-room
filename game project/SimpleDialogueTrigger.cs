using UnityEngine;

public class SimpleDialogueTrigger : MonoBehaviour
{
    public DialogueData dialogueData;
    public KeyCode triggerKey = KeyCode.Q;

    private bool hasTriggered = false;

    private void Update()
    {
        if (Input.GetKeyDown(triggerKey) && !hasTriggered)
        {
            if (dialogueData != null && DialogueManager.instance != null)
            {
                DialogueManager.instance.StartDialogue(dialogueData);
                hasTriggered = true;
            }
        }
    }

    public void SetDialogueData(DialogueData data)
    {
        dialogueData = data;
    }

    public void SetTriggerKey(KeyCode key)
    {
        triggerKey = key;
    }

    public void ResetTrigger()
    {
        hasTriggered = false;
    }
}