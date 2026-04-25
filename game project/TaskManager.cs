using UnityEngine;
using System.Collections.Generic;

/// <summary>
/// 任务数据类
/// 存储任务的基本信息
/// </summary>
[System.Serializable]
public class TaskData
{
    /// <summary>
    /// 任务ID
    /// </summary>
    public string taskId;
    
    /// <summary>
    /// 任务标题（简短描述）
    /// </summary>
    public string taskTitle;
    
    /// <summary>
    /// 任务详细描述
    /// </summary>
    public string taskDescription;
    
    /// <summary>
    /// 任务是否完成
    /// </summary>
    public bool isCompleted;
    
    /// <summary>
    /// 任务优先级（数字越小优先级越高）
    /// </summary>
    public int priority;
    
    /// <summary>
    /// 任务类型（主线任务、支线任务等）
    /// </summary>
    public string taskType;
    
    public TaskData(string id, string title, string description, int priority = 0, string type = "Main")
    {
        taskId = id;
        taskTitle = title;
        taskDescription = description;
        isCompleted = false;
        this.priority = priority;
        taskType = type;
    }
}

/// <summary>
/// 任务管理器
/// 管理所有任务的添加、完成和更新
/// </summary>
public class TaskManager : MonoBehaviour
{
    /// <summary>
    /// 单例实例
    /// </summary>
    public static TaskManager Instance { get; private set; }
    
    /// <summary>
    /// 所有任务列表
    /// </summary>
    [SerializeField]
    private List<TaskData> allTasks = new List<TaskData>();
    
    /// <summary>
    /// 当前激活的任务列表
    /// </summary>
    private List<TaskData> activeTasks = new List<TaskData>();
    
    /// <summary>
    /// 当前正在进行的任务
    /// </summary>
    private TaskData currentTask;
    
    void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
        }
        else
        {
            Destroy(gameObject);
        }
    }
    
    void Start()
    {
        InitializeDefaultTasks();
    }
    
    /// <summary>
    /// 初始化默认任务
    /// </summary>
    void InitializeDefaultTasks()
    {
        // 不添加默认任务，只显示用户自己添加的任务
        Debug.Log("TaskManager initialized without default tasks");
    }
    
    /// <summary>
    /// 添加新任务
    /// </summary>
    public void AddTask(string taskId, string title, string description, int priority = 0, string type = "Main")
    {
        TaskData newTask = new TaskData(taskId, title, description, priority, type);
        allTasks.Add(newTask);
        activeTasks.Add(newTask);
        
        SortTasksByPriority();
        UpdateCurrentTask();
        
        Debug.Log($"Task added: {title}");
    }
    
    /// <summary>
    /// 完成任务
    /// </summary>
    public void CompleteTask(string taskId)
    {
        TaskData task = FindTaskById(taskId);
        if (task != null)
        {
            task.isCompleted = true;
            activeTasks.Remove(task);
            UpdateCurrentTask();
            Debug.Log($"Task completed: {task.taskTitle}");
        }
    }
    
    /// <summary>
    /// 根据ID查找任务
    /// </summary>
    public TaskData FindTaskById(string taskId)
    {
        return allTasks.Find(t => t.taskId == taskId);
    }
    
    /// <summary>
    /// 按优先级排序任务
    /// </summary>
    void SortTasksByPriority()
    {
        activeTasks.Sort((a, b) => a.priority.CompareTo(b.priority));
    }
    
    /// <summary>
    /// 更新当前任务
    /// </summary>
    void UpdateCurrentTask()
    {
        if (activeTasks.Count > 0)
        {
            currentTask = activeTasks[0];
        }
        else
        {
            currentTask = null;
        }
    }
    
    /// <summary>
    /// 获取当前任务
    /// </summary>
    public TaskData GetCurrentTask()
    {
        return currentTask;
    }
    
    /// <summary>
    /// 获取所有激活的任务
    /// </summary>
    public List<TaskData> GetActiveTasks()
    {
        return activeTasks;
    }
    
    /// <summary>
    /// 获取所有任务
    /// </summary>
    public List<TaskData> GetAllTasks()
    {
        return allTasks;
    }
}
