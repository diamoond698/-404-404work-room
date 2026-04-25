using UnityEngine;
using UnityEngine.Playables;
using UnityEngine.SceneManagement;

/// <summary>
/// 过场动画控制器
/// 控制Timeline动画结束后切换到SampleScene场景
/// </summary>
public class OpeningController : MonoBehaviour
{
    /// <summary>
    /// PlayableDirector组件
    /// </summary>
    public PlayableDirector playableDirector;
    
    /// <summary>
    /// 下一个场景名称
    /// </summary>
    public string nextSceneName = "SampleScene";

    /// <summary>
    /// 开始方法
    /// </summary>
    void Start()
    {
        if (playableDirector != null)
        {
            // 播放时间线动画
            playableDirector.Play();
            // 监听动画结束事件
            playableDirector.stopped += OnAnimationEnd;
        }
        else
        {
            Debug.LogError("PlayableDirector not assigned!");
        }
    }

    /// <summary>
    /// 动画结束回调
    /// </summary>
    /// <param name="director">PlayableDirector</param>
    void OnAnimationEnd(PlayableDirector director)
    {
        // 动画结束后加载SampleScene
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
