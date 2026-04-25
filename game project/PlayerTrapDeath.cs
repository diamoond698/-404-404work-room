using UnityEngine;

public class PlayerTrapDeath : MonoBehaviour
{
    [Header("设置")]
    public string trapTag = "traps";
    public string doorTag = "门";
    public float respawnDelay = 1.5f;

    private Animator animator;
    private Transform respawnPoint;
    private bool isDead = false;

    void Start()
    {
        animator = GetComponent<Animator>();
        FindRespawnPoint();
    }

    void FindRespawnPoint()
    {
        GameObject doorObj = GameObject.FindWithTag(doorTag);
        if (doorObj != null)
        {
            respawnPoint = doorObj.transform;
            Debug.Log("Respawn point found at door position: " + respawnPoint.position);
        }
        else
        {
            Debug.LogError("Door object with tag '" + doorTag + "' not found! Using current position as respawn point.");
            respawnPoint = transform;
        }
    }

    void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.gameObject.CompareTag(trapTag) && !isDead)
        {
            Die();
        }
    }

    void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.gameObject.CompareTag(trapTag) && !isDead)
        {
            Die();
        }
    }

    void Die()
    {
        isDead = true;
        Debug.Log("Player died! Playing death animation.");

        // 播放死亡动画
        if (animator != null)
        {
            animator.SetTrigger("Death");
        }

        // 禁用移动（同时支持两种移动脚本）
        DisableMovement();

        // 延迟后复活
        Invoke("Respawn", respawnDelay);
    }

    void Respawn()
    {
        Debug.Log("Respawning player at door position.");

        // 移动到复活点
        transform.position = respawnPoint.position + new Vector3(1, 0, 0); // 偏移一点，避免卡在门里

        // 重置状态
        isDead = false;

        // 启用移动（同时支持两种移动脚本）
        EnableMovement();

        // 重置动画
        if (animator != null)
        {
            animator.SetTrigger("Respawn");
        }

        Debug.Log("Player respawned successfully.");
    }

    void DisableMovement()
    {
        // 尝试禁用 PlayerMovement2D
        PlayerMovement2D playerMovement = GetComponent<PlayerMovement2D>();
        if (playerMovement != null)
        {
            playerMovement.enabled = false;
        }

        // 尝试禁用 EightDirectionMovement
        EightDirectionMovement eightDirectionMovement = GetComponent<EightDirectionMovement>();
        if (eightDirectionMovement != null)
        {
            eightDirectionMovement.enabled = false;
        }

        // 禁用 Rigidbody2D
        Rigidbody2D rb = GetComponent<Rigidbody2D>();
        if (rb != null)
        {
            rb.velocity = Vector2.zero;
            rb.isKinematic = true;
        }
    }

    void EnableMovement()
    {
        // 尝试启用 PlayerMovement2D
        PlayerMovement2D playerMovement = GetComponent<PlayerMovement2D>();
        if (playerMovement != null)
        {
            playerMovement.enabled = true;
        }

        // 尝试启用 EightDirectionMovement
        EightDirectionMovement eightDirectionMovement = GetComponent<EightDirectionMovement>();
        if (eightDirectionMovement != null)
        {
            eightDirectionMovement.enabled = true;
        }

        // 启用 Rigidbody2D
        Rigidbody2D rb = GetComponent<Rigidbody2D>();
        if (rb != null)
        {
            rb.isKinematic = false;
        }
    }
}