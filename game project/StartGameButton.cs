using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class StartGameButton : MonoBehaviour
{
    void Start()
    {
        Button button = GetComponent<Button>();
        if (button != null)
        {
            button.onClick.AddListener(StartGame);
            Debug.Log("Button click event added successfully");
        }
        else
        {
            Debug.LogError("Button component not found on this object!");
        }
    }

    void StartGame()
    {
        Debug.Log("StartGame method called, loading scene: 开头动画");
        SceneManager.LoadScene("开头动画");
    }
}