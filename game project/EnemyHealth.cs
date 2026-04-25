using UnityEngine;

public class EnemyHealth : MonoBehaviour
{
    [Header("Health Settings")]
    public int maxHealth = 3;
    private int currentHealth;

    [Header("Damage Feedback")]
    public float knockbackForce = 5f;
    public float knockbackDuration = 0.3f;
    public float invulnerabilityTime = 0.5f;
    public Color damageColor = Color.red;
    public float damageFlashDuration = 0.1f;

    [Header("Death Settings")]
    public float deathDelay = 1f;
    public bool destroyOnDeath = true;
    public GameObject deathEffect;
    public AudioClip deathSound;

    [Header("Animation Settings")]
    public Animator animator;
    public string hurtTrigger = "Hurt";
    public string deathTrigger = "Death";
    public string hitBool = "IsHit";

    [Header("Audio Settings")]
    public AudioSource audioSource;
    public AudioClip[] hurtSounds;

    [Header("References")]
    public Rigidbody2D rb;
    public SpriteRenderer spriteRenderer;
    public Collider2D enemyCollider;

    private bool isDead = false;
    private bool isInvulnerable = false;
    private bool isKnockbacked = false;
    private float invulnerabilityTimer = 0f;
    private Color originalColor;
    private GameObject currentDeathEffect;

    void Start()
    {
        currentHealth = maxHealth;

        if (rb == null)
        {
            rb = GetComponent<Rigidbody2D>();
        }

        if (spriteRenderer == null)
        {
            spriteRenderer = GetComponent<SpriteRenderer>();
        }

        if (enemyCollider == null)
        {
            enemyCollider = GetComponent<Collider2D>();
        }

        if (audioSource == null)
        {
            audioSource = GetComponent<AudioSource>();
        }

        if (spriteRenderer != null)
        {
            originalColor = spriteRenderer.color;
        }
    }

    void Update()
    {
        if (isInvulnerable)
        {
            invulnerabilityTimer += Time.deltaTime;

            if (invulnerabilityTimer >= invulnerabilityTime)
            {
                EndInvulnerability();
            }
        }
    }

    public void TakeDamage(int damage, Vector2 attackDirection)
    {
        if (isDead || isInvulnerable)
            return;

        currentHealth -= damage;
        Debug.Log($"{gameObject.name} took {damage} damage. Health: {currentHealth}/{maxHealth}");

        // 播放受伤动画
        if (animator != null)
        {
            animator.SetTrigger(hurtTrigger);
            animator.SetBool(hitBool, true);
        }

        // 播放受伤音效
        if (audioSource != null && hurtSounds != null && hurtSounds.Length > 0)
        {
            AudioClip randomSound = hurtSounds[Random.Range(0, hurtSounds.Length)];
            audioSource.PlayOneShot(randomSound);
        }

        // 显示受伤效果
        ShowDamageEffect();

        // 应用击退效果
        ApplyKnockback(attackDirection);

        // 开始无敌时间
        StartInvulnerability();

        // 检查死亡
        if (currentHealth <= 0)
        {
            Die();
        }
    }

    void ShowDamageEffect()
    {
        if (spriteRenderer != null)
        {
            spriteRenderer.color = damageColor;
            Invoke(nameof(ResetColor), damageFlashDuration);
        }
    }

    void ResetColor()
    {
        if (spriteRenderer != null)
        {
            spriteRenderer.color = originalColor;
        }
    }

    void ApplyKnockback(Vector2 attackDirection)
    {
        if (rb != null)
        {
            isKnockbacked = true;
            rb.velocity = Vector2.zero;
            rb.AddForce(-attackDirection * knockbackForce, ForceMode2D.Impulse);
            Invoke(nameof(EndKnockback), knockbackDuration);
        }
    }

    void EndKnockback()
    {
        isKnockbacked = false;
        if (rb != null)
        {
            rb.velocity = Vector2.zero;
        }
    }

    void StartInvulnerability()
    {
        isInvulnerable = true;
        invulnerabilityTimer = 0f;
    }

    void EndInvulnerability()
    {
        isInvulnerable = false;
        if (animator != null)
        {
            animator.SetBool(hitBool, false);
        }
    }

    void Die()
    {
        if (isDead)
            return;

        isDead = true;
        Debug.Log($"{gameObject.name} died!");

        // 播放死亡动画
        if (animator != null)
        {
            animator.SetTrigger(deathTrigger);
        }

        // 播放死亡音效
        if (audioSource != null && deathSound != null)
        {
            audioSource.PlayOneShot(deathSound);
        }

        // 显示死亡效果
        if (deathEffect != null)
        {
            currentDeathEffect = Instantiate(deathEffect, transform.position, Quaternion.identity);
            Destroy(currentDeathEffect, deathDelay);
        }

        // 禁用敌人行为
        DisableEnemy();

        // 延迟销毁
        if (destroyOnDeath)
        {
            Destroy(gameObject, deathDelay);
        }
    }

    void DisableEnemy()
    {
        // 禁用移动脚本
        EnemyMovement enemyMovement = GetComponent<EnemyMovement>();
        if (enemyMovement != null)
        {
            enemyMovement.enabled = false;
        }

        // 禁用碰撞器
        if (enemyCollider != null)
        {
            enemyCollider.enabled = false;
        }

        // 停止刚体
        if (rb != null)
        {
            rb.velocity = Vector2.zero;
            rb.isKinematic = true;
        }
    }

    public int GetCurrentHealth()
    {
        return currentHealth;
    }

    public int GetMaxHealth()
    {
        return maxHealth;
    }

    public float GetHealthPercentage()
    {
        return (float)currentHealth / maxHealth;
    }

    public bool IsDead()
    {
        return isDead;
    }

    public bool IsInvulnerable()
    {
        return isInvulnerable;
    }

    public bool IsKnockbacked()
    {
        return isKnockbacked;
    }
}
