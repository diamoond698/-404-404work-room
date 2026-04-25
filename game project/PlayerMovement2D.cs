using UnityEngine;

/// <summary>
/// 2D玩家移动系统
/// 处理玩家的上下左右移动
/// </summary>
public class PlayerMovement2D : MonoBehaviour
{
    [Header("移动设置")]
    [Tooltip("移动速度")]
    public float moveSpeed = 5f;

    [Header("引用")]
    [Tooltip("玩家的Rigidbody2D组件")]
    public Rigidbody2D rb;
    [Tooltip("玩家的SpriteRenderer组件")]
    public SpriteRenderer spriteRenderer;
    [Tooltip("玩家的Animator组件")]
    public Animator animator;

    private Vector2 movement;

    void Start()
    {
        if (rb == null)
        {
            rb = GetComponent<Rigidbody2D>();
            if (rb == null)
            {
                Debug.LogError("PlayerMovement2D: Rigidbody2D component not found!");
            }
            else
            {
                // 配置Rigidbody2D，确保稳定移动
                rb.gravityScale = 0f;
                rb.freezeRotation = true;
                rb.interpolation = RigidbodyInterpolation2D.Interpolate;
            }
        }

        if (spriteRenderer == null)
        {
            spriteRenderer = GetComponent<SpriteRenderer>();
        }

        if (animator == null)
        {
            animator = GetComponent<Animator>();
        }
    }

    void Update()
    {
        // 获取输入
        float horizontal = Input.GetAxisRaw("Horizontal");
        float vertical = Input.GetAxisRaw("Vertical");

        // 计算移动方向
        movement = new Vector2(horizontal, vertical).normalized;

        // 更新动画参数
        UpdateAnimations();

        // 处理翻转
        HandleFlip();
    }

    void FixedUpdate()
    {
        // 应用移动
        if (rb != null)
        {
            rb.velocity = movement * moveSpeed;
        }
    }

    void UpdateAnimations()
    {
        if (animator != null)
        {
            // 更新速度参数
            float speed = movement.magnitude;
            animator.SetFloat("Speed", speed);

            // 更新移动方向参数（如果需要）
            if (speed > 0.1f)
            {
                animator.SetFloat("Horizontal", movement.x);
                animator.SetFloat("Vertical", movement.y);
            }
        }
    }

    void HandleFlip()
    {
        // 只在水平移动时翻转
        if (movement.x != 0 && spriteRenderer != null)
        {
            spriteRenderer.flipX = movement.x < 0;
        }
    }

    /// <summary>
    /// 获取当前移动方向
    /// </summary>
    public Vector2 GetMovementDirection()
    {
        return movement;
    }

    /// <summary>
    /// 检查玩家是否在移动
    /// </summary>
    public bool IsMoving()
    {
        return movement.magnitude > 0.1f;
    }

    /// <summary>
    /// 设置移动速度
    /// </summary>
    public void SetMoveSpeed(float speed)
    {
        moveSpeed = speed;
    }

    /// <summary>
    /// 获取当前移动速度
    /// </summary>
    public float GetMoveSpeed()
    {
        return moveSpeed;
    }
}
