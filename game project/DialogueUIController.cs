using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Collections.Generic;

public class DialogueUIController : MonoBehaviour
{
    [Header("UI Elements")]
    [SerializeField]
    private GameObject dialoguePanel;

    [SerializeField]
    private TextMeshProUGUI speakerNameText;

    [SerializeField]
    private TextMeshProUGUI dialogueText;

    [SerializeField]
    private Image speakerImage;

    [SerializeField]
    private Transform choicesContainer;

    [SerializeField]
    private GameObject choiceButtonPrefab;

    [SerializeField]
    private Button continueButton;

    private List<GameObject> currentChoiceButtons = new List<GameObject>();

    private void Awake()
    {
        if (DialogueManager.instance != null)
        {
            DialogueManager.instance.SetUIController(this);
        }
    }

    private void Start()
    {
        HideDialogueUI();

        if (continueButton != null)
        {
            continueButton.onClick.AddListener(OnContinueClicked);
        }

        // 检查必要的UI元素
        CheckUIElements();
    }

    private void CheckUIElements()
    {
        if (dialoguePanel == null)
        {
            Debug.LogError("Dialogue Panel is not set in DialogueUIController");
        }

        if (dialogueText == null)
        {
            Debug.LogError("Dialogue Text is not set in DialogueUIController");
        }

        if (speakerNameText == null)
        {
            Debug.LogError("Speaker Name Text is not set in DialogueUIController");
        }

        if (speakerImage == null)
        {
            Debug.LogError("Speaker Image is not set in DialogueUIController");
        }

        if (choicesContainer == null)
        {
            Debug.LogError("Choices Container is not set in DialogueUIController");
        }

        if (choiceButtonPrefab == null)
        {
            Debug.LogError("Choice Button Prefab is not set in DialogueUIController");
        }

        if (continueButton == null)
        {
            Debug.LogError("Continue Button is not set in DialogueUIController");
        }
    }

    public void ShowDialogueUI()
    {
        if (dialoguePanel != null)
        {
            dialoguePanel.SetActive(true);
        }
    }

    public void HideDialogueUI()
    {
        if (dialoguePanel != null)
        {
            dialoguePanel.SetActive(false);
        }
        ClearChoices();
    }

    public void DisplayDialogue(DialogueNode node)
    {
        if (node == null)
        {
            Debug.LogError("DisplayDialogue called with null node");
            return;
        }

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
            if (node.speakerImage != null)
            {
                speakerImage.sprite = node.speakerImage;
                speakerImage.gameObject.SetActive(true);
                Debug.Log("Speaker image set: " + node.speakerImage.name);
            }
            else
            {
                speakerImage.gameObject.SetActive(false);
                Debug.Log("No speaker image for node: " + node.speakerName);
            }
        }

        ClearChoices();

        if (node.choices != null && node.choices.Count > 0)
        {
            Debug.Log("Creating " + node.choices.Count + " choices for node: " + node.speakerName);
            CreateChoiceButtons(node.choices);
            if (continueButton != null)
            {
                continueButton.gameObject.SetActive(false);
            }
        }
        else
        {
            Debug.Log("No choices for node: " + node.speakerName);
            if (continueButton != null)
            {
                continueButton.gameObject.SetActive(!node.isEndNode);
            }
        }
    }

    private void CreateChoiceButtons(List<DialogueChoice> choices)
    {
        if (choicesContainer == null)
        {
            Debug.LogError("Choices Container is null, cannot create choice buttons");
            return;
        }

        if (choiceButtonPrefab == null)
        {
            Debug.LogError("Choice Button Prefab is null, cannot create choice buttons");
            return;
        }

        for (int i = 0; i < choices.Count; i++)
        {
            GameObject buttonObj = Instantiate(choiceButtonPrefab, choicesContainer);
            Button button = buttonObj.GetComponent<Button>();
            TextMeshProUGUI buttonText = buttonObj.GetComponentInChildren<TextMeshProUGUI>();

            if (buttonText != null)
            {
                buttonText.text = choices[i].choiceText;
                Debug.Log("Created choice button: " + choices[i].choiceText);
            }

            int choiceIndex = i;
            if (button != null)
            {
                button.onClick.AddListener(() => OnChoiceClicked(choiceIndex));
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

    private void OnChoiceClicked(int choiceIndex)
    {
        if (DialogueManager.instance != null)
        {
            Debug.Log("Choice clicked: " + choiceIndex);
            DialogueManager.instance.SelectChoice(choiceIndex);
        }
    }

    private void OnContinueClicked()
    {
        if (DialogueManager.instance != null)
        {
            DialogueManager.instance.ContinueDialogue();
        }
    }
}