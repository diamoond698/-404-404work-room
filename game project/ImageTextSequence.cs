using UnityEngine;
using UnityEngine.UI;
using TMPro;
using UnityEngine.SceneManagement;
using System.Collections;

/// <summary>
/// 图片文字序列控制器
/// 控制图片和多个文字的显示，3秒后跳转到SampleScene场景
/// 支持TextMeshPro文本，图片和文字都有淡入淡出效果
/// </summary>
public class ImageTextSequence : MonoBehaviour
{
    [Header("场景设置")]
    /// <summary>
    /// 下一个场景名称
    /// </summary>
    public string nextSceneName = "SampleScene";
    
    /// <summary>
    /// 图片显示后延迟跳转的时间（秒）
    /// </summary>
    public float delayAfterImage = 3f;

    [Header("UI元素")]
    /// <summary>
    /// 图片对象
    /// </summary>
    public Image image;
    
    /// <summary>
    /// 文字对象数组（TextMeshPro）
    /// </summary>
    public TMP_Text[] texts;

    [Header("动画设置")]
    /// <summary>
    /// 淡入动画持续时间
    /// </summary>
    public float fadeInDuration = 1f;
    
    /// <summary>
    /// 淡出动画持续时间
    /// </summary>
    public float fadeOutDuration = 1f;
    
    /// <summary>
    /// 文字之间的延迟时间（秒）
    /// </summary>
    public float textDelay = 0.5f;

    /// <summary>
    /// 开始方法
    /// </summary>
    void Start()
    {
        Debug.Log("ImageTextSequence started");
        
        // 初始化UI元素
        InitializeUI();
        
        // 开始序列
        StartCoroutine(PlaySequence());
    }

    /// <summary>
    /// 初始化UI元素
    /// </summary>
    void InitializeUI()
    {
        // 初始化图片
        if (image != null)
        {
            // 初始设置为透明
            Color imageColor = image.color;
            imageColor.a = 0f;
            image.color = imageColor;
            image.gameObject.SetActive(true);
            Debug.Log("Image initialized");
        }
        else
        {
            Debug.LogError("Image not assigned!");
        }

        // 初始化文字
        if (texts != null && texts.Length > 0)
        {
            foreach (TMP_Text text in texts)
            {
                if (text != null)
                {
                    // 初始设置为透明
                    Color textColor = text.color;
                    textColor.a = 0f;
                    text.color = textColor;
                    text.gameObject.SetActive(true);
                    Debug.Log($"Text {text.name} initialized");
                }
            }
        }
        else
        {
            Debug.LogWarning("No texts assigned!");
        }
    }

    /// <summary>
    /// 播放序列
    /// </summary>
    /// <returns>协程</returns>
    IEnumerator PlaySequence()
    {
        // 图片淡入
        yield return StartCoroutine(FadeInUI(image));
        
        // 文字淡入（按顺序）
        if (texts != null && texts.Length > 0)
        {
            foreach (TMP_Text text in texts)
            {
                if (text != null)
                {
                    yield return StartCoroutine(FadeInUI(text));
                    yield return new WaitForSeconds(textDelay);
                }
            }
        }
        
        // 等待指定时间
        Debug.Log($"Waiting for {delayAfterImage} seconds before loading next scene");
        yield return new WaitForSeconds(delayAfterImage);
        
        // 文字淡出（按倒序）
        if (texts != null && texts.Length > 0)
        {
            for (int i = texts.Length - 1; i >= 0; i--)
            {
                TMP_Text text = texts[i];
                if (text != null)
                {
                    yield return StartCoroutine(FadeOutUI(text));
                    yield return new WaitForSeconds(textDelay * 0.5f); // 淡出延迟减半
                }
            }
        }
        
        // 图片淡出
        yield return StartCoroutine(FadeOutUI(image));
        
        // 跳转到下一个场景
        LoadNextScene();
    }

    /// <summary>
    /// UI元素淡入动画
    /// </summary>
    /// <param name="uiElement">UI元素</param>
    /// <returns>协程</returns>
    IEnumerator FadeInUI(Graphic uiElement)
    {
        if (uiElement == null)
        {
            yield break;
        }

        float elapsed = 0f;
        Color startColor = uiElement.color;
        startColor.a = 0f;
        Color endColor = uiElement.color;
        endColor.a = 1f;

        while (elapsed < fadeInDuration)
        {
            float t = elapsed / fadeInDuration;
            uiElement.color = Color.Lerp(startColor, endColor, t);
            elapsed += Time.deltaTime;
            yield return null;
        }

        // 确保最终状态
        uiElement.color = endColor;
        Debug.Log($"{uiElement.name} faded in");
    }

    /// <summary>
    /// UI元素淡出动画
    /// </summary>
    /// <param name="uiElement">UI元素</param>
    /// <returns>协程</returns>
    IEnumerator FadeOutUI(Graphic uiElement)
    {
        if (uiElement == null)
        {
            yield break;
        }

        float elapsed = 0f;
        Color startColor = uiElement.color;
        startColor.a = 1f;
        Color endColor = uiElement.color;
        endColor.a = 0f;

        while (elapsed < fadeOutDuration)
        {
            float t = elapsed / fadeOutDuration;
            uiElement.color = Color.Lerp(startColor, endColor, t);
            elapsed += Time.deltaTime;
            yield return null;
        }

        // 确保最终状态
        uiElement.color = endColor;
        Debug.Log($"{uiElement.name} faded out");
    }

    /// <summary>
    /// 加载下一个场景
    /// </summary>
    void LoadNextScene()
    {
        if (!string.IsNullOrEmpty(nextSceneName))
        {
            Debug.Log("Loading scene: " + nextSceneName);
            SceneManager.LoadScene(nextSceneName);
        }
        else
        {
            Debug.LogError("Next scene name not set!");
        }
    }
}
