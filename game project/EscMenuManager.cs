using UnityEngine;
using UnityEngine.UI;

public class EscMenuManager : MonoBehaviour
{
    [Header("UI设置")]
    public GameObject escMenuPanel;
    public Button continueButton;
    public Button quitButton;

    private bool isMenuOpen = false;

    void Start()
    {
        // 初始隐藏esc菜单
        if (escMenuPanel != null)
        {
            escMenuPanel.SetActive(false);
        }

        // 绑定按钮事件
        if (continueButton != null)
        {
            continueButton.onClick.AddListener(HideEscMenu);
        }

        if (quitButton != null)
        {
            quitButton.onClick.AddListener(QuitGame);
        }
    }

    void Update()
    {
        // 监听esc键
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            if (isMenuOpen)
            {
                HideEscMenu();
            }
            else
            {
                ShowEscMenu();
            }
        }
    }

    void ShowEscMenu()
    {
        if (escMenuPanel != null)
        {
            escMenuPanel.SetActive(true);
            Time.timeScale = 0f; // 暂停游戏
            isMenuOpen = true;
            Debug.Log("Esc menu opened");
        }
    }

    void HideEscMenu()
    {
        if (escMenuPanel != null)
        {
            escMenuPanel.SetActive(false);
            Time.timeScale = 1f; // 恢复游戏
            isMenuOpen = false;
            Debug.Log("Esc menu closed");
        }
    }

    void QuitGame()
    {
        Debug.Log("Quit game button clicked");
        #if UNITY_EDITOR
        UnityEditor.EditorApplication.isPlaying = false;
        #else
        Application.Quit();
        #endif
    }
}