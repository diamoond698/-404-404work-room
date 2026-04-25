using UnityEngine;

public class FootstepAudio : MonoBehaviour
{
    [Header("音频设置")]
    public AudioClip footstepSound;
    public AudioSource audioSource;

    [Header("移动设置")]
    public float moveThreshold = 0.1f;
    public float stepInterval = 0.5f;

    private float stepTimer;
    private Rigidbody2D rb2d;

    void Start()
    {
        rb2d = GetComponent<Rigidbody2D>();

        if (audioSource == null)
        {
            audioSource = gameObject.AddComponent<AudioSource>();
        }

        audioSource.loop = false;
        audioSource.playOnAwake = false;

        Debug.Log("FootstepAudio initialized. Move Threshold: " + moveThreshold + ", Step Interval: " + stepInterval);
    }

    void Update()
    {
        float velocity = 0f;
        bool isMoving = false;

        if (rb2d != null)
        {
            velocity = rb2d.velocity.magnitude;
            isMoving = velocity > moveThreshold;
            Debug.Log("Velocity: " + velocity + ", Is Moving: " + isMoving + ", Threshold: " + moveThreshold);
        }
        else
        {
            Debug.LogError("Rigidbody2D not found!");
        }

        if (isMoving)
        {
            stepTimer += Time.deltaTime;
            Debug.Log("Step Timer: " + stepTimer + ", Step Interval: " + stepInterval);

            if (stepTimer >= stepInterval)
            {
                if (footstepSound != null)
                {
                    audioSource.PlayOneShot(footstepSound);
                    Debug.Log("Footstep sound played: " + footstepSound.name);
                }
                else
                {
                    Debug.LogError("Footstep sound is not assigned!");
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