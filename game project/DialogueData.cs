using UnityEngine;
using System.Collections.Generic;

[System.Serializable]
public class DialogueChoice
{
    public string choiceText;
    [System.NonSerialized]
    public DialogueNode nextNode;
    public int nextNodeIndex = -1;
}

[System.Serializable]
public class DialogueNode
{
    public string speakerName;
    [TextArea(3, 10)]
    public string dialogueText;
    public Sprite speakerImage;
    public List<DialogueChoice> choices;
    public bool isEndNode;

    public DialogueNode()
    {
        choices = new List<DialogueChoice>();
        isEndNode = false;
    }
}

[CreateAssetMenu(fileName = "NewDialogue", menuName = "Dialogue System/Dialogue Data")]
public class DialogueData : ScriptableObject
{
    public List<DialogueNode> nodes;

    private void OnEnable()
    {
        ResolveNodeReferences();
    }

    public void ResolveNodeReferences()
    {
        if (nodes == null) return;

        foreach (var node in nodes)
        {
            if (node.choices != null)
            {
                foreach (var choice in node.choices)
                {
                    if (choice.nextNodeIndex >= 0 && choice.nextNodeIndex < nodes.Count)
                    {
                        choice.nextNode = nodes[choice.nextNodeIndex];
                    }
                    else
                    {
                        choice.nextNode = null;
                    }
                }
            }
        }
    }

    public DialogueNode GetStartNode()
    {
        if (nodes != null && nodes.Count > 0)
        {
            return nodes[0];
        }
        return null;
    }
}