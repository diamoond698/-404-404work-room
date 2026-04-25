using UnityEngine;

public class PlayerAttack : MonoBehaviour
{
    [Header("Attack Settings")]
    public float attackCooldown = 1f;
    public float attackRange = 1.5f;
    public int attackDamage = 1;
    public float attackDuration = 0.3f;

    [Header("Visual Settings")]
    public GameObject attackEffect;
    public Color attackColor = Color.red;
    public float effectDuration = 0.2f;

    [Header("Audio Settings")]
    public AudioClip attackSound;
    public AudioSource audioSource;

    [Header("Animation Settings")]
    public Animator animator;
    public string attackTrigger = "Attack";
    public string attackDirectionParam = "AttackDirection";

    [Header("References")]
    public MonoBehaviour playerMovement;

    private float lastAttackTime;
    private bool isAttacking;
    private Vector2 attackDirection;
    private GameObject currentAttackEffect;

    void Start()
    {
        if (audioSource == null)
        {
            audioSource = GetComponent<AudioSource>();
        }
        
        if (playerMovement == null)
        {
            // 尝试获取 PlayerMovement2D 组件
            playerMovement = GetComponent("PlayerMovement2D") as MonoBehaviour;
            // 如果没有找到，尝试获取 EightDirectionMovement 组件
            if (playerMovement == null)
            {
                playerMovement = GetComponent("EightDirectionMovement") as MonoBehaviour;
            }
            // 不报错，只是记录日志
            if (playerMovement == null)
            {
                Debug.LogWarning("PlayerAttack: No movement component found. Attack will still work.");
            }
        }
    }

    void Update()
    {
        if (Input.GetMouseButtonDown(0) && CanAttack())
        {
            Attack();
        }
    }

    bool CanAttack()
    {
        return Time.time >= lastAttackTime + attackCooldown && !isAttacking;
    }

    void Attack()
    {
        isAttacking = true;
        lastAttackTime = Time.time;

        // 获取攻击方向（基于鼠标位置）
        Vector2 mousePosition = Camera.main.ScreenToWorldPoint(Input.mousePosition);
        attackDirection = (mousePosition - (Vector2)transform.position).normalized;

        // 播放攻击动画
        if (animator != null)
        {
            animator.SetTrigger(attackTrigger);
            animator.SetFloat(attackDirectionParam, GetAttackDirection());
        }

        // 播放攻击音效
        if (audioSource != null && attackSound != null)
        {
            audioSource.PlayOneShot(attackSound);
        }

        // 显示攻击效果
        ShowAttackEffect();

        // 检测敌人
        DetectEnemies();

        // 结束攻击
        Invoke(nameof(EndAttack), attackDuration);
    }

    float GetAttackDirection()
    {
        if (Mathf.Abs(attackDirection.x) > Mathf.Abs(attackDirection.y))
        {
            return attackDirection.x > 0 ? 1 : 3; // 右 : 左
        }
        else
        {
            return attackDirection.y > 0 ? 0 : 2; // 上 : 下
        }
    }

    void ShowAttackEffect()
    {
        if (attackEffect != null)
        {
            Vector3 effectPosition = transform.position + (Vector3)attackDirection * attackRange * 0.5f;
            currentAttackEffect = Instantiate(attackEffect, effectPosition, Quaternion.identity);
            
            // 设置攻击效果颜色
            SpriteRenderer sr = currentAttackEffect.GetComponent<SpriteRenderer>();
            if (sr != null)
            {
                sr.color = attackColor;
            }

            // 销毁效果
            Destroy(currentAttackEffect, effectDuration);
        }
    }

    void DetectEnemies()
    {
        Collider2D[] hitColliders = Physics2D.OverlapCircleAll(transform.position, attackRange);

        foreach (Collider2D collider in hitColliders)
        {
            if (collider.CompareTag("Enemy"))
            {
                // 检查敌人是否在攻击方向
                Vector2 directionToEnemy = (collider.transform.position - transform.position).normalized;
                float angle = Vector2.Angle(attackDirection, directionToEnemy);

                if (angle < 45f)
                {
                    EnemyHealth enemyHealth = collider.GetComponent<EnemyHealth>();
                    if (enemyHealth != null)
                    {
                        enemyHealth.TakeDamage(attackDamage, attackDirection);
                        Debug.Log($"Attacked {collider.name} for {attackDamage} damage");
                    }
                }
            }
        }
    }

    void EndAttack()
    {
        isAttacking = false;
    }

    private void OnDrawGizmosSelected()
    {
        Gizmos.color = Color.red;
        Gizmos.DrawWireSphere(transform.position, attackRange);
    }
}
