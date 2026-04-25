using UnityEngine;
using UnityEngine.UI;

public class ExitGameButton : MonoBehaviour
{
    void Start()
    {
        Button button = GetComponent<Button>();
        if (button != null)
        {
            button.onClick.AddListener(ExitGame);
            Debug.Log("Exit button click event added successfully");
        }
        else
        {
            Debug.LogError("Button component not found on this object!");
        }
    }

    void ExitGame()
    {
        Debug.Log("ExitGame method called");
        
        // 在编辑器中不退出，只显示日志
        #if UNITY_EDITOR
        Debug.Log("Exit Game clicked (Editor mode - not quitting)");
        #else
        // 在构建后的游戏中退出
        Application.Quit();
        #endif
    }
}