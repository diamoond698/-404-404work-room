using UnityEngine;

public class EnemyMovement : MonoBehaviour
{
    [Header("Movement Settings")]
    public float moveSpeed = 2f;
    public float patrolRadius = 5f;
    public float patrolWaitTime = 2f;
    public float patrolPointDistance = 1f;

    [Header("Chase Settings")]
    public float chaseRange = 8f;
    public float attackRange = 1.5f;
    public float chaseSpeedMultiplier = 1.5f;

    [Header("Attack Settings")]
    public int attackDamage = 1;
    public float attackCooldown = 2f;
    public float attackDuration = 0.5f;
    public float attackDelay = 0.3f;

    [Header("Animation Settings")]
    public Animator animator;
    public string horizontalParam = "Horizontal";
    public string verticalParam = "Vertical";
    public string speedParam = "Speed";
    public string attackTrigger = "Attack";

    [Header("Audio Settings")]
    public AudioSource audioSource;
    public AudioClip[] attackSounds;
    public AudioClip[] footstepSounds;

    [Header("References")]
    public Rigidbody2D rb;
    public Collider2D enemyCollider;
    public EnemyHealth enemyHealth;

    [Header("Patrol Settings")]
    public bool usePatrol = true;
    public bool randomPatrol = true;

    public enum EnemyState
    {
        Idle,
        Patrol,
        Chase,
        Attack
    }

    private EnemyState currentState = EnemyState.Idle;
    private Vector3 startPosition;
    private Vector3 targetPosition;
    private float patrolTimer = 0f;
    private float attackTimer = 0f;
    private float attackDelayTimer = 0f;
    private bool isAttacking = false;
    private GameObject player;
    private Vector2 lastMoveDirection;
    private float footstepTimer = 0f;
    private float footstepInterval = 0.4f;

    void Start()
    {
        startPosition = transform.position;
        player = GameObject.FindGameObjectWithTag("Player");

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

        if (enemyCollider == null)
        {
            enemyCollider = GetComponent<Collider2D>();
        }

        if (enemyHealth == null)
        {
            enemyHealth = GetComponent<EnemyHealth>();
        }

        if (audioSource == null)
        {
            audioSource = GetComponent<AudioSource>();
        }

        if (usePatrol)
        {
            GenerateNewPatrolPoint();
        }
    }

    void Update()
    {
        if (player == null)
        {
            // 尝试重新查找玩家
            player = GameObject.FindGameObjectWithTag("Player");
            return;
        }

        if (enemyHealth != null && enemyHealth.IsDead())
            return;

        UpdateState();
        UpdateAnimations();
        UpdateFootsteps();
    }

    void UpdateState()
    {
        float distanceToPlayer = Vector2.Distance(transform.position, player.transform.position);

        switch (currentState)
        {
            case EnemyState.Idle:
                HandleIdleState(distanceToPlayer);
                break;

            case EnemyState.Patrol:
                HandlePatrolState(distanceToPlayer);
                break;

            case EnemyState.Chase:
                HandleChaseState(distanceToPlayer);
                break;

            case EnemyState.Attack:
                HandleAttackState(distanceToPlayer);
                break;
        }
    }

    void HandleIdleState(float distanceToPlayer)
    {
        if (rb != null)
        {
            rb.velocity = Vector2.zero;
        }

        if (usePatrol)
        {
            patrolTimer += Time.deltaTime;
            if (patrolTimer >= patrolWaitTime)
            {
                patrolTimer = 0f;
                currentState = EnemyState.Patrol;
                GenerateNewPatrolPoint();
            }
        }

        if (distanceToPlayer <= chaseRange)
        {
            currentState = EnemyState.Chase;
        }
    }

    void HandlePatrolState(float distanceToPlayer)
    {
        if (!usePatrol)
        {
            currentState = EnemyState.Idle;
            return;
        }

        MoveTowards(targetPosition, moveSpeed);

        if (Vector2.Distance(transform.position, targetPosition) < patrolPointDistance)
        {
            currentState = EnemyState.Idle;
            patrolTimer = 0f;
        }

        if (distanceToPlayer <= chaseRange)
        {
            currentState = EnemyState.Chase;
        }
    }

    void HandleChaseState(float distanceToPlayer)
    {
        if (distanceToPlayer > chaseRange)
        {
            if (usePatrol)
            {
                currentState = EnemyState.Patrol;
            }
            else
            {
                currentState = EnemyState.Idle;
            }
            return;
        }

        if (distanceToPlayer <= attackRange)
        {
            currentState = EnemyState.Attack;
            attackTimer = 0f;
            attackDelayTimer = 0f;
            return;
        }

        MoveTowards(player.transform.position, moveSpeed * chaseSpeedMultiplier);
    }

    void HandleAttackState(float distanceToPlayer)
    {
        if (rb != null)
        {
            rb.velocity = Vector2.zero;
        }

        if (distanceToPlayer > attackRange)
        {
            currentState = EnemyState.Chase;
            return;
        }

        attackTimer += Time.deltaTime;

        if (!isAttacking && attackTimer >= attackCooldown)
        {
            StartAttack();
        }

        if (isAttacking)
        {
            attackDelayTimer += Time.deltaTime;

            if (attackDelayTimer >= attackDelay)
            {
                PerformAttack();
                isAttacking = false;
                attackTimer = 0f;
            }
        }
    }

    void MoveTowards(Vector3 target, float speed)
    {
        if (rb == null)
            return;

        Vector2 direction = (target - transform.position).normalized;
        rb.velocity = direction * speed;

        if (direction.magnitude > 0.1f)
        {
            lastMoveDirection = direction;
        }
    }

    void StartAttack()
    {
        isAttacking = true;
        attackDelayTimer = 0f;

        if (animator != null)
        {
            // 检查攻击触发器是否存在
            if (HasAnimatorParameter(animator, attackTrigger, AnimatorControllerParameterType.Trigger))
            {
                animator.SetTrigger(attackTrigger);
            }
        }
    }

    void PerformAttack()
    {
        if (player == null)
            return;

        PlayerHealth playerHealth = player.GetComponent<PlayerHealth>();
        if (playerHealth != null && !playerHealth.IsInvulnerable())
        {
            Vector2 attackDirection = (player.transform.position - transform.position).normalized;
            playerHealth.TakeDamage(attackDamage);
            Debug.Log($"{gameObject.name} attacked player for {attackDamage} damage");
        }

        PlayAttackSound();
    }

    void PlayAttackSound()
    {
        if (audioSource != null && attackSounds != null && attackSounds.Length > 0)
        {
            AudioClip randomSound = attackSounds[Random.Range(0, attackSounds.Length)];
            audioSource.PlayOneShot(randomSound);
        }
    }

    void UpdateAnimations()
    {
        if (animator == null)
            return;

        Vector2 movement = Vector2.zero;
        if (rb != null)
        {
            movement = rb.velocity;
        }

        // 检查动画参数是否存在
        if (HasAnimatorParameter(animator, horizontalParam, AnimatorControllerParameterType.Float))
        {
            animator.SetFloat(horizontalParam, movement.x);
        }
        if (HasAnimatorParameter(animator, verticalParam, AnimatorControllerParameterType.Float))
        {
            animator.SetFloat(verticalParam, movement.y);
        }
        if (HasAnimatorParameter(animator, speedParam, AnimatorControllerParameterType.Float))
        {
            animator.SetFloat(speedParam, movement.magnitude);
        }
    }

    void UpdateFootsteps()
    {
        if (rb == null)
            return;

        if (rb.velocity.magnitude > 0.1f && !isAttacking)
        {
            footstepTimer += Time.deltaTime;

            if (footstepTimer >= footstepInterval)
            {
                PlayFootstepSound();
                footstepTimer = 0f;
            }
        }
    }

    void PlayFootstepSound()
    {
        if (audioSource != null && footstepSounds != null && footstepSounds.Length > 0)
        {
            AudioClip randomSound = footstepSounds[Random.Range(0, footstepSounds.Length)];
            audioSource.PlayOneShot(randomSound);
        }
    }

    void GenerateNewPatrolPoint()
    {
        if (randomPatrol)
        {
            float randomAngle = Random.Range(0f, Mathf.PI * 2f);
            float randomDistance = Random.Range(0f, patrolRadius);

            float x = startPosition.x + Mathf.Cos(randomAngle) * randomDistance;
            float y = startPosition.y + Mathf.Sin(randomAngle) * randomDistance;

            targetPosition = new Vector3(x, y, startPosition.z);
        }
        else
        {
            targetPosition = startPosition;
        }
    }

    public void ResetEnemy()
    {
        currentState = EnemyState.Idle;
        patrolTimer = 0f;
        attackTimer = 0f;
        isAttacking = false;
        transform.position = startPosition;
        if (rb != null)
        {
            rb.velocity = Vector2.zero;
        }

        if (usePatrol)
        {
            GenerateNewPatrolPoint();
        }
    }

    public EnemyState GetCurrentState()
    {
        return currentState;
    }

    private bool HasAnimatorParameter(Animator animator, string parameterName, AnimatorControllerParameterType parameterType)
    {
        foreach (AnimatorControllerParameter parameter in animator.parameters)
        {
            if (parameter.name == parameterName && parameter.type == parameterType)
            {
                return true;
            }
        }
        return false;
    }

    private void OnDrawGizmosSelected()
    {
        Gizmos.color = Color.yellow;
        Gizmos.DrawWireSphere(transform.position, patrolRadius);

        Gizmos.color = Color.blue;
        Gizmos.DrawWireSphere(transform.position, chaseRange);

        Gizmos.color = Color.red;
        Gizmos.DrawWireSphere(transform.position, attackRange);

        if (Application.isPlaying)
        {
            Gizmos.color = Color.green;
            Gizmos.DrawLine(transform.position, targetPosition);
        }
    }
}
