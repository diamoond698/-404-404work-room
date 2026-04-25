using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Collections.Generic;

public class SkillSystem : MonoBehaviour
{
    [Header("技能面板")]
    public GameObject skillPanel;
    
    [Header("技能点")]
    public int skillPoints = 5;
    public TextMeshProUGUI skillPointsText;
    
    [System.Serializable]
    public class Skill
    {
        public string name;
        public string description;
        public string effect;
        public int maxLevel = 3;
        public int currentLevel = 0;
        public Sprite icon;
    }
    
    public List<Skill> skills = new List<Skill>();
    
    [Header("UI引用")]
    public Transform skillListParent;
    public GameObject skillItemPrefab;
    public GameObject skillInfoPanel;
    
    [Header("技能信息面板引用")]
    public Image infoIcon;
    public TextMeshProUGUI infoName;
    public TextMeshProUGUI infoDescription;
    public TextMeshProUGUI infoEffect;
    public TextMeshProUGUI infoLevel;
    public Button upgradeButton;
    public Button closeButton;
    
    private int currentSkillIndex = -1;
    
    void Start()
    {
        // 初始化技能列表
        InitializeSkillList();
        UpdateSkillPointsDisplay();
        
        // 绑定关闭按钮
        if (closeButton != null)
        {
            closeButton.onClick.AddListener(() => 
            {
                if (skillInfoPanel != null)
                {
                    skillInfoPanel.SetActive(false);
                }
            });
        }
        
        // 默认隐藏技能信息面板
        if (skillInfoPanel != null)
        {
            skillInfoPanel.SetActive(false);
        }
        
        Debug.Log("SkillSystem initialized.");
    }
    
    void Update()
    {
        // 空的Update方法，面板控制由SkillPanelController处理
    }
    
    void InitializeSkillList()
    {
        // 清空现有技能项
        if (skillListParent != null)
        {
            foreach (Transform child in skillListParent)
            {
                Destroy(child.gameObject);
            }
            
            // 创建技能项
            for (int i = 0; i < skills.Count; i++)
            {
                int index = i;
                Skill skill = skills[i];
                
                if (skillItemPrefab != null)
                {
                    GameObject item = Instantiate(skillItemPrefab, skillListParent);
                    
                    // 设置图标
                    Transform iconTransform = item.transform.Find("Icon");
                    if (iconTransform != null)
                    {
                        Image icon = iconTransform.GetComponent<Image>();
                        if (icon != null && skill.icon != null)
                        {
                            icon.sprite = skill.icon;
                        }
                    }
                    
                    // 设置名称
                    Transform nameTransform = item.transform.Find("Name");
                    if (nameTransform != null)
                    {
                        TextMeshProUGUI nameText = nameTransform.GetComponent<TextMeshProUGUI>();
                        if (nameText != null)
                        {
                            nameText.text = skill.name;
                        }
                    }
                    
                    // 设置等级
                    Transform levelTransform = item.transform.Find("Level");
                    if (levelTransform != null)
                    {
                        TextMeshProUGUI levelText = levelTransform.GetComponent<TextMeshProUGUI>();
                        if (levelText != null)
                        {
                            levelText.text = "Lv." + skill.currentLevel;
                        }
                    }
                    
                    // 绑定点击事件
                    Button button = item.GetComponent<Button>();
                    if (button != null)
                    {
                        button.onClick.AddListener(() => ShowSkillInfo(index));
                    }
                }
            }
        }
    }
    
    void ShowSkillInfo(int index)
    {
        if (index < 0 || index >= skills.Count)
            return;
        
        currentSkillIndex = index;
        Skill skill = skills[index];
        
        // 显示信息面板
        if (skillInfoPanel != null)
        {
            skillInfoPanel.SetActive(true);
            
            // 设置技能信息
            if (infoIcon != null && skill.icon != null)
            {
                infoIcon.sprite = skill.icon;
            }
            
            if (infoName != null)
                infoName.text = skill.name;
            if (infoDescription != null)
                infoDescription.text = skill.description;
            if (infoEffect != null)
                infoEffect.text = skill.effect;
            if (infoLevel != null)
                infoLevel.text = string.Format("等级: {0}/{1}", skill.currentLevel, skill.maxLevel);
            
            // 更新升级按钮
            if (upgradeButton != null)
            {
                TextMeshProUGUI buttonText = upgradeButton.GetComponentInChildren<TextMeshProUGUI>();
                
                if (skill.currentLevel >= skill.maxLevel)
                {
                    upgradeButton.interactable = false;
                    if (buttonText != null)
                        buttonText.text = "已满级";
                }
                else if (skillPoints <= 0)
                {
                    upgradeButton.interactable = false;
                    if (buttonText != null)
                        buttonText.text = "技能点不足";
                }
                else
                {
                    upgradeButton.interactable = true;
                    if (buttonText != null)
                        buttonText.text = "升级";
                }
                
                // 绑定升级事件
                upgradeButton.onClick.RemoveAllListeners();
                upgradeButton.onClick.AddListener(() => UpgradeSkill(index));
            }
        }
    }
    
    void UpgradeSkill(int index)
    {
        if (index < 0 || index >= skills.Count)
            return;
        
        Skill skill = skills[index];
        
        if (skillPoints > 0 && skill.currentLevel < skill.maxLevel)
        {
            skillPoints--;
            skill.currentLevel++;
            
            UpdateSkillPointsDisplay();
            ShowSkillInfo(index);
            
            // 更新技能列表中的等级显示
            if (skillListParent != null && skillListParent.childCount > index)
            {
                Transform skillItem = skillListParent.GetChild(index);
                Transform levelTransform = skillItem.Find("Level");
                if (levelTransform != null)
                {
                    TextMeshProUGUI levelText = levelTransform.GetComponent<TextMeshProUGUI>();
                    if (levelText != null)
                    {
                        levelText.text = "Lv." + skill.currentLevel;
                    }
                }
            }
        }
    }
    
    void UpdateSkillPointsDisplay()
    {
        if (skillPointsText != null)
        {
            skillPointsText.text = "技能点: " + skillPoints;
        }
    }
    

}