using UnityEngine;
using TMPro;
using System.Collections;

/// <summary>
/// 旁白系统
/// 用于在游戏开头或特定场景播放旁白文本
/// </summary>
public class Narrator : MonoBehaviour
{
    [Header("旁白设置")]
    /// <summary>
    /// 旁白文本数组
    /// </summary>
    [TextArea(3, 10)]
    public string[] narrationLines;
    
    /// <summary>
    /// 旁白显示持续时间（秒）
    /// </summary>
    public float narrationDuration = 3f;
    
    /// <summary>
    /// 旁白之间的间隔时间（秒）
    /// </summary>
    public float lineInterval = 1f;
    
    /// <summary>
    /// 自动播放
    /// </summary>
    public bool autoPlay = true;
    
    /// <summary>
    /// 游戏开始后延迟播放的时间（秒）
    /// </summary>
    public float startDelay = 1f;
    
    /// <summary>
    /// 播放完成后自动销毁
    /// </summary>
    public bool autoDestroy = true;

    [Header("UI设置")]
    /// <summary>
    /// 旁白UI面板
    /// </summary>
    public GameObject narrationUI;
    
    /// <summary>
    /// 旁白文本组件
    /// </summary>
    public TMP_Text narrationText;
    
    /// <summary>
    /// 旁白名字文本组件
    /// </summary>
    public TMP_Text narratorNameText;
    
    /// <summary>
    /// 旁白名字
    /// </summary>
    public string narratorName = "旁白";

    [Header("动画设置")]
    /// <summary>
    /// 淡入动画持续时间
    /// </summary>
    public float fadeInDuration = 0.5f;
    
    /// <summary>
    /// 淡出动画持续时间
    /// </summary>
    public float fadeOutDuration = 0.5f;

    [Header("音频设置")]
    /// <summary>
    /// 旁白音效
    /// </summary>
    public AudioClip[] narrationSounds;
    
    /// <summary>
    /// 音频源
    /// </summary>
    public AudioSource audioSource;

    private bool isNarrationPlaying = false;
    private int currentLineIndex = 0;

    /// <summary>
    /// 开始方法
    /// </summary>
    void Start()
    {
        // 初始化UI
        if (narrationUI != null)
        {
            narrationUI.SetActive(false);
        }

        // 初始化音频源
        if (audioSource == null)
        {
            audioSource = GetComponent<AudioSource>();
            if (audioSource == null)
            {
                audioSource = gameObject.AddComponent<AudioSource>();
            }
        }

        // 自动播放
        if (autoPlay && narrationLines != null && narrationLines.Length > 0)
        {
            StartCoroutine(PlayNarrationAfterDelay(startDelay));
        }
    }

    /// <summary>
    /// 延迟播放旁白
    /// </summary>
    /// <param name="delay">延迟时间</param>
    /// <returns>协程</returns>
    private IEnumerator PlayNarrationAfterDelay(float delay)
    {
        yield return new WaitForSeconds(delay);
        StartNarration();
    }

    /// <summary>
    /// 开始旁白
    /// </summary>
    public void StartNarration()
    {
        if (isNarrationPlaying || narrationLines == null || narrationLines.Length == 0)
            return;

        isNarrationPlaying = true;
        currentLineIndex = 0;
        StartCoroutine(PlayNarrationSequence());
    }

    /// <summary>
    /// 播放旁白序列
    /// </summary>
    /// <returns>协程</returns>
    private IEnumerator PlayNarrationSequence()
    {
        foreach (string line in narrationLines)
        {
            // 显示旁白
            yield return StartCoroutine(ShowNarration(line));

            // 播放音效
            PlayNarrationSound(currentLineIndex);

            // 等待指定时间
            yield return new WaitForSeconds(narrationDuration);

            // 隐藏旁白
            yield return StartCoroutine(HideNarration());

            // 等待间隔时间
            if (currentLineIndex < narrationLines.Length - 1)
            {
                yield return new WaitForSeconds(lineInterval);
            }

            currentLineIndex++;
        }

        isNarrationPlaying = false;
        Debug.Log("旁白播放完成");

        // 播放完成后自动销毁
        if (autoDestroy)
        {
            Debug.Log("旁白系统自动销毁");
            // 确保UI被隐藏
            if (narrationUI != null)
            {
                narrationUI.SetActive(false);
            }
            // 销毁自身
            Destroy(gameObject);
        }
    }

    /// <summary>
    /// 显示旁白
    /// </summary>
    /// <param name="text">旁白文本</param>
    /// <returns>协程</returns>
    private IEnumerator ShowNarration(string text)
    {
        if (narrationUI != null)
        {
            narrationUI.SetActive(true);
        }

        if (narrationText != null)
        {
            narrationText.text = text;
        }

        if (narratorNameText != null)
        {
            narratorNameText.text = narratorName;
        }

        // 淡入动画
        if (narrationUI != null)
        {
            yield return StartCoroutine(FadeIn(narrationUI.GetComponent<CanvasGroup>(), fadeInDuration));
        }
    }

    /// <summary>
    /// 隐藏旁白
    /// </summary>
    /// <returns>协程</returns>
    private IEnumerator HideNarration()
    {
        // 淡出动画
        if (narrationUI != null)
        {
            yield return StartCoroutine(FadeOut(narrationUI.GetComponent<CanvasGroup>(), fadeOutDuration));
        }
    }

    /// <summary>
    /// 淡入动画
    /// </summary>
    /// <param name="canvasGroup">CanvasGroup组件</param>
    /// <param name="duration">动画持续时间</param>
    /// <returns>协程</returns>
    private IEnumerator FadeIn(CanvasGroup canvasGroup, float duration)
    {
        if (canvasGroup == null)
            yield break;

        float elapsedTime = 0f;
        float startAlpha = canvasGroup.alpha;

        while (elapsedTime < duration)
        {
            elapsedTime += Time.deltaTime;
            canvasGroup.alpha = Mathf.Lerp(startAlpha, 1f, elapsedTime / duration);
            yield return null;
        }

        canvasGroup.alpha = 1f;
    }

    /// <summary>
    /// 淡出动画
    /// </summary>
    /// <param name="canvasGroup">CanvasGroup组件</param>
    /// <param name="duration">动画持续时间</param>
    /// <returns>协程</returns>
    private IEnumerator FadeOut(CanvasGroup canvasGroup, float duration)
    {
        if (canvasGroup == null)
            yield break;

        float elapsedTime = 0f;
        float startAlpha = canvasGroup.alpha;

        while (elapsedTime < duration)
        {
            elapsedTime += Time.deltaTime;
            canvasGroup.alpha = Mathf.Lerp(startAlpha, 0f, elapsedTime / duration);
            yield return null;
        }

        canvasGroup.alpha = 0f;
        if (narrationUI != null)
        {
            narrationUI.SetActive(false);
        }
    }

    /// <summary>
    /// 播放旁白音效
    /// </summary>
    /// <param name="index">音效索引</param>
    private void PlayNarrationSound(int index)
    {
        if (audioSource != null && narrationSounds != null && index < narrationSounds.Length)
        {
            audioSource.PlayOneShot(narrationSounds[index]);
        }
    }

    /// <summary>
    /// 检查旁白是否正在播放
    /// </summary>
    /// <returns>是否正在播放</returns>
    public bool IsNarrationPlaying()
    {
        return isNarrationPlaying;
    }

    /// <summary>
    /// 停止旁白
    /// </summary>
    public void StopNarration()
    {
        isNarrationPlaying = false;
        StopAllCoroutines();
        if (narrationUI != null)
        {
            narrationUI.SetActive(false);
        }
        Debug.Log("旁白已停止");

        // 停止后自动销毁
        if (autoDestroy)
        {
            Debug.Log("旁白系统自动销毁");
            Destroy(gameObject);
        }
    }

    /// <summary>
    /// 手动触发旁白
    /// </summary>
    /// <param name="lines">旁白文本数组</param>
    public void TriggerNarration(string[] lines)
    {
        narrationLines = lines;
        StartNarration();
    }
}