using UnityEngine;

public class EightDirectionMovement : MonoBehaviour
{
    [Header("移动参数")]
    public float moveSpeed = 5f;
    public bool eightDirection = true;      // 是否限制八方向

    [Header("引用")]
    public Rigidbody2D rb;
    public SpriteRenderer spriteRenderer;
    public Animator animator;

    [Header("动画参数")]
    public string[] directionStates = { "Down", "Up", "Left", "Right", "DownLeft", "DownRight", "UpLeft", "UpRight" };

    private Vector2 moveDirection;

    void Start()
    {
        if (rb == null)
        {
            rb = GetComponent<Rigidbody2D>();
            if (rb != null)
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

        // 移动方向
        moveDirection = new Vector2(horizontal, vertical);

        // 限制为八方向
        if (eightDirection && moveDirection.magnitude > 0)
        {
            float angle = Mathf.Atan2(moveDirection.y, moveDirection.x) * Mathf.Rad2Deg;
            angle = Mathf.Round(angle / 45) * 45;
            moveDirection = new Vector2(Mathf.Cos(angle * Mathf.Deg2Rad), Mathf.Sin(angle * Mathf.Deg2Rad));
        }

        // 处理翻转
        HandleFlip();

        // 更新动画
        UpdateAnimations();
    }

    void FixedUpdate()
    {
        // 应用移动
        if (rb != null)
        {
            rb.velocity = moveDirection.normalized * moveSpeed;
        }
    }

    void HandleFlip()
    {
        // 只在水平移动时翻转
        if (moveDirection.x != 0 && spriteRenderer != null)
        {
            spriteRenderer.flipX = moveDirection.x < 0;
        }
    }

    void UpdateAnimations()
    {
        if (animator != null)
        {
            // 更新速度参数
            float speed = moveDirection.magnitude;
            animator.SetFloat("Speed", speed);

            // 更新移动方向参数
            if (speed > 0.1f)
            {
                animator.SetFloat("Horizontal", moveDirection.x);
                animator.SetFloat("Vertical", moveDirection.y);
            }
        }
    }

    /// <summary>
    /// 获取当前移动方向
    /// </summary>
    public Vector2 GetMovementDirection()
    {
        return moveDirection;
    }

    /// <summary>
    /// 检查是否在移动
    /// </summary>
    public bool IsMoving()
    {
        return moveDirection.magnitude > 0.1f;
    }
}