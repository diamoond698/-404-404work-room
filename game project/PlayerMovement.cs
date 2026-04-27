using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    [Header("移动设置")]
    [SerializeField]
    private float moveSpeed = 5f;
    [SerializeField]
    private bool useSmoothMovement = true;
    [SerializeField]
    private float smoothTime = 0.1f;

    [Header("物理设置")]
    [SerializeField]
    private CollisionDetectionMode2D collisionDetection = CollisionDetectionMode2D.Continuous;
    [SerializeField]
    private float linearDrag = 0f;
    [SerializeField]
    private float angularDrag = 0f;
    [SerializeField]
    private RigidbodyInterpolation2D interpolation = RigidbodyInterpolation2D.Interpolate;

    [Header("模型设置")]
    [SerializeField]
    private bool lockRotation = true;
    [SerializeField]
    private Vector3 fixedRotation = new Vector3(0, 0, 0);

    [Header("转向设置")]
    [SerializeField]
    private bool enableHorizontalFlip = true;

    private Rigidbody2D rb;
    private Vector2 movement;
    private Vector2 smoothVelocity;
    private SpriteRenderer spriteRenderer;
    private bool isMoving = false;

    private void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        spriteRenderer = GetComponent<SpriteRenderer>();

        if (rb == null)
        {
            rb = gameObject.AddComponent<Rigidbody2D>();
        }

        ConfigureRigidbody();

        // 确保初始旋转正确
        transform.rotation = Quaternion.Euler(fixedRotation);
    }

    private void ConfigureRigidbody()
    {
        // 优化Rigidbody2D设置
        rb.gravityScale = 0;
        rb.interpolation = interpolation;
        rb.collisionDetectionMode = collisionDetection;
        rb.constraints = RigidbodyConstraints2D.FreezeRotation;
        rb.drag = linearDrag;
        rb.angularDrag = angularDrag;
        rb.sleepMode = RigidbodySleepMode2D.NeverSleep;
    }

    private void Update()
    {
        GetInput();
        HandleHorizontalFlip();
        LockModelRotation();
    }

    private void FixedUpdate()
    {
        Move();
    }

    private void GetInput()
    {
        float horizontal = Input.GetAxisRaw("Horizontal");
        float vertical = Input.GetAxisRaw("Vertical");

        movement = new Vector2(horizontal, vertical).normalized;
        isMoving = movement != Vector2.zero;
    }

    private void Move()
    {
        if (movement == Vector2.zero)
        {
            // 当没有输入时，立即停止移动
            rb.velocity = Vector2.zero;
            return;
        }

        Vector2 targetVelocity = movement * moveSpeed;

        if (useSmoothMovement)
        {
            // 使用SmoothDamp实现平滑移动
            rb.velocity = Vector2.SmoothDamp(rb.velocity, targetVelocity, ref smoothVelocity, smoothTime);
        }
        else
        {
            rb.velocity = targetVelocity;
        }
    }

    private void HandleHorizontalFlip()
    {
        if (!enableHorizontalFlip || spriteRenderer == null || movement == Vector2.zero)
            return;

        // 只在水平移动时翻转
        if (Mathf.Abs(movement.x) > Mathf.Abs(movement.y))
        {
            spriteRenderer.flipX = movement.x < 0;
        }
    }

    private void LockModelRotation()
    {
        if (lockRotation)
        {
            // 完全固定模型旋转，确保模型不偏
            transform.rotation = Quaternion.Euler(fixedRotation);
            rb.rotation = fixedRotation.z;
        }
    }

    // 公共方法
    public void SetMoveSpeed(float speed)
    {
        moveSpeed = speed;
    }

    public Vector2 GetMovement()
    {
        return movement;
    }

    public bool IsMoving()
    {
        return isMoving;
    }

    public void SetFixedRotation(Vector3 rotation)
    {
        fixedRotation = rotation;
    }

    public void SetEnableHorizontalFlip(bool enable)
    {
        enableHorizontalFlip = enable;
    }

    public void SetCollisionDetection(CollisionDetectionMode2D mode)
    {
        collisionDetection = mode;
        if (rb != null)
        {
            rb.collisionDetectionMode = mode;
        }
    }

    public void SetLinearDrag(float drag)
    {
        linearDrag = drag;
        if (rb != null)
        {
            rb.drag = drag;
        }
    }
}