using UnityEngine;
using UnityEngine.Video;
using UnityEngine.SceneManagement;

/// <summary>
/// 视频过场动画控制器
/// 控制视频播放结束后切换到SampleScene场景
/// </summary>
public class VideoController : MonoBehaviour
{
    /// <summary>
    /// VideoPlayer组件
    /// </summary>
    public VideoPlayer videoPlayer;
    
    /// <summary>
    /// 下一个场景名称
    /// </summary>
    public string nextSceneName = "SampleScene";

    /// <summary>
    /// 开始方法
    /// </summary>
    void Start()
    {
        if (videoPlayer != null)
        {
            Debug.Log("VideoController started");
            if (videoPlayer.clip != null)
            {
                Debug.Log("Video clip: " + videoPlayer.clip.name);
            }
            else
            {
                Debug.LogError("Video clip not assigned!");
            }
            
            // 播放视频
            videoPlayer.Play();
            // 监听视频结束事件
            videoPlayer.loopPointReached += OnVideoEnd;
            
            // 添加调试信息
            videoPlayer.started += (vp) => Debug.Log("Video started");
            videoPlayer.errorReceived += (vp, error) => Debug.LogError("Video error: " + error);
        }
        else
        {
            Debug.LogError("VideoPlayer not assigned!");
        }
    }

    /// <summary>
    /// 视频结束回调
    /// </summary>
    /// <param name="vp">VideoPlayer</param>
    void OnVideoEnd(VideoPlayer vp)
    {
        Debug.Log("Video ended, loading next scene: " + nextSceneName);
        if (!string.IsNullOrEmpty(nextSceneName))
        {
            SceneManager.LoadScene(nextSceneName);
        }
        else
        {
            Debug.LogError("Next scene name not set!");
        }
    }
}
