using UnityEngine;

public class PlayerHealth : MonoBehaviour
{
    [Header("Health Settings")]
    public int maxHealth = 3;
    private int currentHealth;

    [Header("Damage Feedback")]
    public float invulnerabilityTime = 1f;
    public float knockbackForce = 3f;
    public float knockbackDuration = 0.2f;
    public Color damageColor = Color.red;
    public float damageFlashDuration = 0.1f;
    public bool enableInvulnerabilityFlash = true;

    [Header("Death Settings")]
    public float deathDelay = 2f;
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
    public MonoBehaviour playerMovement;
    public MonoBehaviour playerAttack;

    [Header("Respawn Settings")]
    public bool enableRespawn = false;
    public float respawnDelay = 3f;
    public Transform respawnPoint;

    private bool isDead = false;
    private bool isInvulnerable = false;
    private bool isKnockbacked = false;
    private float invulnerabilityTimer = 0f;
    private float flashTimer = 0f;
    private bool isVisible = true;
    private Color originalColor;

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
                Debug.LogWarning("PlayerHealth: No movement component found.");
            }
        }

        if (playerAttack == null)
        {
            // 尝试获取 PlayerAttack 组件
            playerAttack = GetComponent("PlayerAttack") as MonoBehaviour;
            // 不报错，只是记录日志
            if (playerAttack == null)
            {
                Debug.LogWarning("PlayerHealth: No attack component found.");
            }
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
        if (isDead)
            return;

        HandleInvulnerability();
    }

    void HandleInvulnerability()
    {
        if (isInvulnerable)
        {
            invulnerabilityTimer += Time.deltaTime;

            if (enableInvulnerabilityFlash && spriteRenderer != null)
            {
                flashTimer += Time.deltaTime;
                if (flashTimer >= damageFlashDuration)
                {
                    isVisible = !isVisible;
                    spriteRenderer.enabled = isVisible;
                    flashTimer = 0f;
                }
            }

            if (invulnerabilityTimer >= invulnerabilityTime)
            {
                EndInvulnerability();
            }
        }
    }

    public void TakeDamage(int damage)
    {
        if (isDead || isInvulnerable)
            return;

        currentHealth -= damage;
        Debug.Log($"Player took {damage} damage. Health: {currentHealth}/{maxHealth}");

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

        // 开始无敌状态
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

    void StartInvulnerability()
    {
        isInvulnerable = true;
        invulnerabilityTimer = 0f;
        flashTimer = 0f;
        isVisible = true;

        if (spriteRenderer != null)
        {
            spriteRenderer.enabled = true;
        }
    }

    void EndInvulnerability()
    {
        isInvulnerable = false;

        if (spriteRenderer != null)
        {
            spriteRenderer.enabled = true;
        }

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
        Debug.Log("Player died!");

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
            GameObject effect = Instantiate(deathEffect, transform.position, Quaternion.identity);
            Destroy(effect, deathDelay);
        }

        // 禁用玩家控制
        DisablePlayerControls();

        // 处理复活
        if (enableRespawn)
        {
            Invoke(nameof(Respawn), respawnDelay);
        }
    }

    void DisablePlayerControls()
    {
        if (playerMovement != null)
        {
            playerMovement.enabled = false;
        }

        if (playerAttack != null)
        {
            playerAttack.enabled = false;
        }

        if (rb != null)
        {
            rb.velocity = Vector2.zero;
            rb.isKinematic = true;
        }
    }

    void Respawn()
    {
        if (!enableRespawn)
            return;

        // 重置生命值
        currentHealth = maxHealth;
        isDead = false;
        isInvulnerable = false;

        // 移动到复活点
        if (respawnPoint != null)
        {
            transform.position = respawnPoint.position;
        }

        // 恢复颜色
        if (spriteRenderer != null)
        {
            spriteRenderer.color = originalColor;
            spriteRenderer.enabled = true;
        }

        // 重置动画
        if (animator != null)
        {
            animator.SetBool(hitBool, false);
        }

        // 恢复玩家控制
        if (rb != null)
        {
            rb.isKinematic = false;
        }

        if (playerMovement != null)
        {
            playerMovement.enabled = true;
        }

        if (playerAttack != null)
        {
            playerAttack.enabled = true;
        }

        Debug.Log("Player respawned!");
    }

    public void Heal(int amount)
    {
        if (isDead)
            return;

        currentHealth = Mathf.Min(currentHealth + amount, maxHealth);
        Debug.Log($"Player healed for {amount} health. Current health: {currentHealth}/{maxHealth}");
    }

    public void SetMaxHealth(int newMaxHealth)
    {
        maxHealth = newMaxHealth;
        currentHealth = Mathf.Min(currentHealth, maxHealth);
        Debug.Log($"Max health set to {maxHealth}");
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
}
