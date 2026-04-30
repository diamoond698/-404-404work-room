using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Collections.Generic;

public class DialogueUIController : MonoBehaviour
{
    [Header("UI Elements")]
    public GameObject dialoguePanel;
    public TextMeshProUGUI speakerNameText;
    public TextMeshProUGUI dialogueText;
    public Image speakerImage;
    public Transform choicesContainer;
    public GameObject choiceButtonPrefab;
    public Button continueButton;

    private List<GameObject> currentChoiceButtons = new List<GameObject>();

    private void Start()
    {
        dialoguePanel.SetActive(false);
        
        if (continueButton != null)
        {
            continueButton.onClick.AddListener(ContinueDialogue);
        }
    }

    public void ShowDialogue(DialogueNode node)
    {
        if (node == null)
        {
            Debug.LogError("ShowDialogue called with null node!");
            return;
        }

        dialoguePanel.SetActive(true);
        
        if (speakerNameText != null)
        {
            speakerNameText.text = node.speakerName;
        }

        if (dialogueText != null)
        {
            dialogueText.text = node.dialogueText;
        }

        if (speakerImage != null)
        {
            if (node.speakerSprite != null)
            {
                speakerImage.sprite = node.speakerSprite;
                speakerImage.gameObject.SetActive(true);
            }
            else
            {
                speakerImage.gameObject.SetActive(false);
            }
        }

        ClearChoices();

        if (node.choices != null && node.choices.Count > 0)
        {
            CreateChoices(node.choices);
            
            if (continueButton != null)
            {
                continueButton.gameObject.SetActive(false);
            }
        }
        else
        {
            if (continueButton != null)
            {
                continueButton.gameObject.SetActive(!node.isEndNode);
            }
        }
    }

    private void CreateChoices(List<DialogueChoice> choices)
    {
        if (choicesContainer == null)
        {
            Debug.LogError("Choices Container is null!");
            return;
        }

        if (choiceButtonPrefab == null)
        {
            Debug.LogError("Choice Button Prefab is null!");
            return;
        }

        for (int i = 0; i < choices.Count; i++)
        {
            GameObject buttonObj = Instantiate(choiceButtonPrefab, choicesContainer);
            Button button = buttonObj.GetComponent<Button>();
            TextMeshProUGUI buttonText = buttonObj.GetComponentInChildren<TextMeshProUGUI>();

            if (buttonText != null)
            {
                buttonText.text = choices[i].optionText;
            }

            int choiceIndex = i;
            if (button != null)
            {
                button.onClick.AddListener(() => SelectChoice(choiceIndex));
            }

            currentChoiceButtons.Add(buttonObj);
        }
    }

    private void ClearChoices()
    {
        foreach (GameObject button in currentChoiceButtons)
        {
            Destroy(button);
        }
        currentChoiceButtons.Clear();
    }

    private void SelectChoice(int choiceIndex)
    {
        if (DialogueManager.instance != null)
        {
            DialogueManager.instance.SelectChoice(choiceIndex);
        }
    }

    private void ContinueDialogue()
    {
        if (DialogueManager.instance != null)
        {
            DialogueManager.instance.ContinueDialogue();
        }
    }

    public void HideDialogue()
    {
        dialoguePanel.SetActive(false);
        ClearChoices();
    }
}