using UnityEngine;
using System.Collections.Generic;

[System.Serializable]
public class DialogueChoice
{
    public string optionText;
    public int nextNodeIndex;
}

[System.Serializable]
public class DialogueNode
{
    public string speakerName;
    [TextArea(3, 10)]
    public string dialogueText;
    public Sprite speakerSprite;
    public List<DialogueChoice> choices;
    public bool isEndNode;
}

[CreateAssetMenu(fileName = "NewDialogue", menuName = "Dialogue/Dialogue Data")]
public class DialogueData : ScriptableObject
{
    public List<DialogueNode> nodes;

    public DialogueNode GetStartNode()
    {
        if (nodes != null && nodes.Count > 0)
        {
            return nodes[0];
        }
        return null;
    }

    public DialogueNode GetNode(int index)
    {
        if (nodes != null && index >= 0 && index < nodes.Count)
        {
            return nodes[index];
        }
        return null;
    }
}