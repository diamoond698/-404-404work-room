using UnityEngine;

public class WalkingAudio : MonoBehaviour
{
    [Header("音频设置")]
    public AudioClip footstepSound;
    public AudioSource audioSource;
    public float volume = 0.5f;

    [Header("移动检测")]
    public float stepInterval = 0.3f;

    private float stepTimer;
    private bool isMoving;

    void Start()
    {
        // 自动添加AudioSource组件
        if (audioSource == null)
        {
            audioSource = gameObject.AddComponent<AudioSource>();
        }

        // 配置AudioSource
        audioSource.loop = false;
        audioSource.playOnAwake = false;
        audioSource.volume = volume;
    }

    void Update()
    {
        // 检测移动输入
        float horizontal = Input.GetAxisRaw("Horizontal");
        float vertical = Input.GetAxisRaw("Vertical");
        isMoving = Mathf.Abs(horizontal) > 0.1f || Mathf.Abs(vertical) > 0.1f;

        // 播放脚步声
        if (isMoving)
        {
            stepTimer += Time.deltaTime;
            if (stepTimer >= stepInterval)
            {
                if (footstepSound != null && audioSource != null)
                {
                    audioSource.PlayOneShot(footstepSound);
                }
                stepTimer = 0f;
            }
        }
        else
        {
            stepTimer = 0f;
        }
    }
}