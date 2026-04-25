using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class DoorNextSceneButton : MonoBehaviour
{
    [Header("UI设置")]
    public Button nextSceneButton;
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
            Debug.Log("Player found: " + playerObj.name);
        }
        else
        {
            Debug.LogError("Player not found! Make sure the player object has the 'Player' tag");
        }

        // 初始隐藏按钮
        if (nextSceneButton != null)
        {
            nextSceneButton.gameObject.SetActive(false);
            Debug.Log("NextSceneButton initial state set to hidden");
        }
        else
        {
            Debug.LogError("NextSceneButton is not assigned!");
        }
    }

    void Update()
    {
        if (playerTransform == null || nextSceneButton == null)
            return;

        // 计算玩家与门的距离（2D游戏中只计算X和Y轴）
        Vector2 playerPos = new Vector2(playerTransform.position.x, playerTransform.position.y);
        Vector2 doorPos = new Vector2(transform.position.x, transform.position.y);
        float distance = Vector2.Distance(playerPos, doorPos);

        Debug.Log("Distance to player: " + distance + ", Interaction distance: " + interactionDistance);

        // 显示或隐藏按钮
        if (distance <= interactionDistance)
        {
            if (!isPlayerNear)
            {
                ShowButton();
                isPlayerNear = true;
            }
        }
        else
        {
            if (isPlayerNear)
            {
                HideButton();
                isPlayerNear = false;
            }
        }
    }

    void ShowButton()
    {
        if (nextSceneButton != null)
        {
            nextSceneButton.gameObject.SetActive(true);
            Debug.Log("Player near the door, showing NextSceneButton");
        }
    }

    void HideButton()
    {
        if (nextSceneButton != null)
        {
            nextSceneButton.gameObject.SetActive(false);
            Debug.Log("Player away from the door, hiding NextSceneButton");
        }
    }

    public void LoadNextScene()
    {
        Debug.Log("LoadNextScene called, loading scene: 地图二");
        SceneManager.LoadScene("地图二");
    }
}