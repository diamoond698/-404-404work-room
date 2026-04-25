using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Collections.Generic;

/// <summary>
/// 任务UI控制器
/// 控制任务指引栏的显示和交互
/// </summary>
public class TaskUIController : MonoBehaviour
{
    [Header("UI元素")]
    /// <summary>
    /// 任务面板
    /// </summary>
    public GameObject taskPanel;
    
    /// <summary>
    /// 任务标题文本
    /// </summary>
    public TMP_Text taskTitleText;
    
    /// <summary>
    /// 任务详细描述文本
    /// </summary>
    public TMP_Text taskDescriptionText;
    
    /// <summary>
    /// 任务类型文本
    /// </summary>
    public TMP_Text taskTypeText;
    
    /// <summary>
    /// 任务列表容器
    /// </summary>
    public GameObject taskListContainer;
    
    /// <summary>
    /// 任务列表项预制体
    /// </summary>
    public GameObject taskItemPrefab;
    
    [Header("设置")]
    /// <summary>
    /// 切换任务面板的按键
    /// </summary>
    public KeyCode toggleKey = KeyCode.Tab;
    
    /// <summary>
    /// 面板展开动画时长
    /// </summary>
    public float expandDuration = 0.3f;
    
    /// <summary>
    /// 面板收起动画时长
    /// </summary>
    public float collapseDuration = 0.3f;
    
    /// <summary>
    /// 面板是否展开
    /// </summary>
    private bool isExpanded = false;
    
    /// <summary>
    /// 面板是否正在动画中
    /// </summary>
    private bool isAnimating = false;
    
    /// <summary>
    /// 面板的原始宽度
    /// </summary>
    private float originalWidth;
    
    /// <summary>
    /// 面板的收起宽度
    /// </summary>
    private float collapsedWidth = 200f;
    
    /// <summary>
    /// 面板的展开宽度
    /// </summary>
    private float expandedWidth = 400f;
    
    /// <summary>
    /// 任务列表项
    /// </summary>
    private List<GameObject> taskItems = new List<GameObject>();
    
    /// <summary>
    /// 面板是否显示
    /// </summary>
    private bool isPanelVisible = false;

    void Start()
    {
        InitializeUI();
        UpdateTaskDisplay();
    }
    
    void Update()
    {
        HandleInput();
    }
    
    /// <summary>
    /// 初始化UI
    /// </summary>
    void InitializeUI()
    {
        if (taskPanel == null)
        {
            Debug.LogError("TaskPanel is not assigned!");
            return;
        }
        
        // 设置面板位置到屏幕正中间
        RectTransform panelRect = taskPanel.GetComponent<RectTransform>();
        if (panelRect != null)
        {
            panelRect.anchorMin = new Vector2(0.5f, 0.5f);
            panelRect.anchorMax = new Vector2(0.5f, 0.5f);
            panelRect.pivot = new Vector2(0.5f, 0.5f);
            panelRect.anchoredPosition = new Vector2(0, 0);
            panelRect.sizeDelta = new Vector2(expandedWidth, 300);
        }
        
        // 初始隐藏面板
        HidePanel();
        
        // 初始化任务列表
        if (taskListContainer != null)
        {
            ClearTaskList();
        }
    }
    
    /// <summary>
    /// 处理用户输入
    /// </summary>
    void HandleInput()
    {
        if (Input.GetKeyDown(toggleKey) && !isAnimating)
        {
            TogglePanelVisibility();
        }
    }
    
    /// <summary>
    /// 切换面板显示/隐藏状态
    /// </summary>
    public void TogglePanelVisibility()
    {
        if (isPanelVisible)
        {
            HidePanel();
        }
        else
        {
            ShowPanel();
        }
    }
    
    /// <summary>
    /// 显示面板
    /// </summary>
    public void ShowPanel()
    {
        if (isAnimating || isPanelVisible || taskPanel == null)
            return;
        
        taskPanel.SetActive(true);
        isPanelVisible = true;
        isExpanded = true; // 直接显示展开状态
        UpdateTaskDisplay();
        Debug.Log("Task panel shown");
    }
    
    /// <summary>
    /// 隐藏面板
    /// </summary>
    public void HidePanel()
    {
        if (isAnimating || !isPanelVisible || taskPanel == null)
            return;
        
        taskPanel.SetActive(false);
        isPanelVisible = false;
        Debug.Log("Task panel hidden");
    }
    
    /// <summary>
    /// 面板动画
    /// </summary>
    System.Collections.IEnumerator AnimatePanel(float targetWidth, float duration, bool expand)
    {
        isAnimating = true;
        
        RectTransform panelRect = taskPanel.GetComponent<RectTransform>();
        float startWidth = panelRect.rect.width;
        float elapsed = 0f;
        
        while (elapsed < duration)
        {
            float t = elapsed / duration;
            float currentWidth = Mathf.Lerp(startWidth, targetWidth, t);
            panelRect.sizeDelta = new Vector2(currentWidth, 300);
            elapsed += Time.deltaTime;
            yield return null;
        }
        
        panelRect.sizeDelta = new Vector2(targetWidth, 300);
        isExpanded = expand;
        isAnimating = false;
        
        // 更新任务显示
        UpdateTaskDisplay();
    }
    
    /// <summary>
    /// 更新任务显示
    /// </summary>
    public void UpdateTaskDisplay()
    {
        if (TaskManager.Instance == null)
            return;
        
        TaskData currentTask = TaskManager.Instance.GetCurrentTask();
        
        if (currentTask != null)
        {
            // 更新当前任务信息
            if (taskTitleText != null)
            {
                taskTitleText.text = currentTask.taskTitle;
            }
            
            if (taskDescriptionText != null)
            {
                taskDescriptionText.text = currentTask.taskDescription;
            }
            
            if (taskTypeText != null)
            {
                taskTypeText.text = currentTask.taskType;
            }
            
            // 如果面板可见且展开，显示任务列表
            if (isPanelVisible && isExpanded && taskListContainer != null)
            {
                UpdateTaskList();
            }
        }
        else
        {
            // 没有任务时显示提示
            if (taskTitleText != null)
            {
                taskTitleText.text = "无当前任务";
            }
            
            if (taskDescriptionText != null)
            {
                taskDescriptionText.text = "所有任务已完成";
            }
        }
    }
    
    /// <summary>
    /// 更新任务列表
    /// </summary>
    void UpdateTaskList()
    {
        if (TaskManager.Instance == null)
            return;
        
        List<TaskData> activeTasks = TaskManager.Instance.GetActiveTasks();
        
        ClearTaskList();
        
        foreach (TaskData task in activeTasks)
        {
            CreateTaskItem(task);
        }
    }
    
    /// <summary>
    /// 创建任务列表项
    /// </summary>
    void CreateTaskItem(TaskData task)
    {
        if (taskItemPrefab == null || taskListContainer == null)
            return;
        
        GameObject taskItem = Instantiate(taskItemPrefab, taskListContainer.transform);
        
        TMP_Text taskItemText = taskItem.GetComponentInChildren<TMP_Text>();
        if (taskItemText != null)
        {
            taskItemText.text = $"{task.taskTitle} ({task.taskType})";
        }
        
        taskItems.Add(taskItem);
    }
    
    /// <summary>
    /// 清除任务列表
    /// </summary>
    void ClearTaskList()
    {
        foreach (GameObject item in taskItems)
        {
            if (item != null)
            {
                Destroy(item);
            }
        }
        
        taskItems.Clear();
    }
    
    /// <summary>
    /// 刷新任务显示
    /// </summary>
    public void RefreshTaskDisplay()
    {
        UpdateTaskDisplay();
    }
}
