using UnityEngine;
using TMPro;

public class DoorInteractionUI : MonoBehaviour
{
    [Header("UI设置")]
    public Canvas interactionCanvas;
    public TMP_Text interactionText;
    public float interactionDistance = 2f;

    private Transform playerTransform;
    private bool isPlayerNear = false;

    void Start()
    {
        // 查找主角
        GameObject playerObj = GameObject.FindWithTag("Player");
        if (playerObj != null)
        {
            playerTransform = playerObj.transform;
            Debug.Log("成功找到玩家对象: " + playerObj.name);
        }
        else
        {
            Debug.LogError("找不到标签为Player的游戏对象！请确保玩家对象的Tag设置为Player");
        }

        // 初始隐藏UI
        if (interactionCanvas != null)
        {
            interactionCanvas.gameObject.SetActive(false);
            Debug.Log("Canvas初始状态已设置为隐藏");
        }
        else
        {
            Debug.LogError("interactionCanvas未赋值！");
        }

        if (interactionText != null)
        {
            Debug.Log("TMP_Text引用成功");
        }
        else
        {
            Debug.LogError("interactionText未赋值！");
        }
    }

    void Update()
    {
        if (playerTransform == null)
        {
            return;
        }

        // 计算玩家与门的距离（2D游戏中只计算X和Y轴）
        Vector2 playerPos = new Vector2(playerTransform.position.x, playerTransform.position.y);
        Vector2 doorPos = new Vector2(transform.position.x, transform.position.y);
        float distance = Vector2.Distance(playerPos, doorPos);

        // 显示或隐藏交互提示
        if (distance <= interactionDistance && !isPlayerNear)
        {
            Debug.Log("玩家靠近门，距离: " + distance);
            ShowInteractionUI();
            isPlayerNear = true;
        }
        else if (distance > interactionDistance && isPlayerNear)
        {
            Debug.Log("玩家远离门，距离: " + distance);
            HideInteractionUI();
            isPlayerNear = false;
        }
    }

    void ShowInteractionUI()
    {
        if (interactionCanvas != null)
        {
            interactionCanvas.gameObject.SetActive(true);

            if (interactionText != null)
            {
                interactionText.text = "靠近门自动开关";
            }
        }
    }

    void HideInteractionUI()
    {
        if (interactionCanvas != null)
        {
            interactionCanvas.gameObject.SetActive(false);
        }
    }
}