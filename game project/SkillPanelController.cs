using UnityEngine;
using UnityEngine.UI;

public class SkillPanelController : MonoBehaviour
{
    [Header("技能面板")]
    public GameObject skillPanel;
    
    private bool isSkillPanelOpen = false;
    
    void Start()
    {
        // 初始隐藏技能面板
        if (skillPanel != null)
        {
            skillPanel.SetActive(false);
        }
        
        Debug.Log("SkillPanelController initialized. Press E to open skill panel.");
    }
    
    void Update()
    {
        // 检测E键输入
        if (Input.GetKeyDown(KeyCode.E))
        {
            if (isSkillPanelOpen)
            {
                HideSkillPanel();
            }
            else
            {
                ShowSkillPanel();
            }
        }
    }
    
    void ShowSkillPanel()
    {
        if (skillPanel != null)
        {
            skillPanel.SetActive(true);
            Time.timeScale = 0f;
            Cursor.visible = true;
            Cursor.lockState = CursorLockMode.None;
            isSkillPanelOpen = true;
            Debug.Log("Skill panel opened");
        }
        else
        {
            Debug.LogError("Skill panel is null!");
        }
    }
    
    void HideSkillPanel()
    {
        if (skillPanel != null)
        {
            skillPanel.SetActive(false);
            Time.timeScale = 1f;
            Cursor.visible = false;
            Cursor.lockState = CursorLockMode.Locked;
            isSkillPanelOpen = false;
            Debug.Log("Skill panel closed");
        }
        else
        {
            Debug.LogError("Skill panel is null!");
        }
    }
}