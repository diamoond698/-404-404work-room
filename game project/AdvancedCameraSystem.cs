using UnityEngine;

public class AdvancedCameraSystem : MonoBehaviour
{
    [Header("跟随设置")]
    [SerializeField]
    private Transform target;
    [SerializeField]
    private float followSpeed = 3f;
    [SerializeField]
    private Vector3 offset = new Vector3(0, 0, -10);

    [Header("平滑设置")]
    [SerializeField]
    private bool useSmoothFollow = true;
    [SerializeField]
    private float smoothTime = 0.3f;
    [SerializeField]
    private float positionSnapThreshold = 0.01f;

    [Header("视野设置")]
    [SerializeField]
    private float visionRadius = 8f;
    [SerializeField]
    private float visionAngle = 120f;
    [SerializeField]
    private Color fogColor = new Color(0, 0, 0, 0.8f);

    [Header("视野遮罩")]
    [SerializeField]
    private GameObject visionMask;
    [SerializeField]
    private SpriteRenderer visionMaskRenderer;
    [SerializeField]
    private bool useAngleVision = false;

    private Camera mainCamera;
    private Vector3 currentVelocity;
    private Vector3 targetPosition;
    private bool isInitialized;

    private void Start()
    {
        mainCamera = GetComponent<Camera>();

        if (visionMask == null)
        {
            visionMask = new GameObject("VisionMask");
            visionMask.transform.parent = transform;
            visionMask.transform.localPosition = Vector3.zero;

            visionMaskRenderer = visionMask.AddComponent<SpriteRenderer>();
            visionMaskRenderer.sortingLayerName = "UI";
            visionMaskRenderer.sortingOrder = -1;
            visionMaskRenderer.sprite = CreateVisionMaskSprite();
        }

        if (visionMaskRenderer != null)
        {
            visionMaskRenderer.material = new Material(Shader.Find("Unlit/Transparent"));
        }

        if (target != null)
        {
            InitializeCameraPosition();
        }
    }

    private void InitializeCameraPosition()
    {
        targetPosition = target.position + offset;
        transform.position = targetPosition;
        isInitialized = true;
    }

    private void LateUpdate()
    {
        if (target != null)
        {
            FollowTarget();
            UpdateVisionMask();
        }
    }

    private void FollowTarget()
    {
        Vector3 targetPosition = target.position + offset;

        if (useSmoothFollow)
        {
            transform.position = Vector3.SmoothDamp(
                transform.position,
                targetPosition,
                ref currentVelocity,
                smoothTime
            );
        }
        else
        {
            float distance = Vector3.Distance(transform.position, targetPosition);
            if (distance > positionSnapThreshold)
            {
                transform.position = Vector3.Lerp(
                    transform.position,
                    targetPosition,
                    followSpeed * Time.deltaTime
                );
            }
        }

        transform.rotation = Quaternion.Euler(0, 0, 0);
    }

    private void UpdateVisionMask()
    {
        if (visionMaskRenderer != null && target != null)
        {
            visionMask.transform.position = target.position;
            visionMask.transform.rotation = Quaternion.identity;
            visionMask.transform.localScale = new Vector3(visionRadius * 2, visionRadius * 2, 1);
            visionMaskRenderer.material.color = fogColor;
        }
    }

    private Sprite CreateVisionMaskSprite()
    {
        int resolution = 512;
        Texture2D texture = new Texture2D(resolution, resolution, TextureFormat.RGBA32, false);

        for (int x = 0; x < resolution; x++)
        {
            for (int y = 0; y < resolution; y++)
            {
                Vector2 center = new Vector2(resolution / 2, resolution / 2);
                Vector2 point = new Vector2(x, y);
                Vector2 direction = (point - center).normalized;
                float distance = Vector2.Distance(center, point);
                float radius = resolution / 2;

                if (distance <= radius)
                {
                    float alpha = 1.0f - (distance / radius);

                    if (useAngleVision)
                    {
                        float angle = Mathf.Atan2(direction.y, direction.x) * Mathf.Rad2Deg;
                        float halfAngle = visionAngle / 2;

                        if (Mathf.Abs(angle) > halfAngle)
                        {
                            alpha = 1.0f;
                        }
                    }

                    texture.SetPixel(x, y, new Color(0, 0, 0, alpha));
                }
                else
                {
                    texture.SetPixel(x, y, new Color(0, 0, 0, 1));
                }
            }
        }

        texture.Apply();

        Sprite sprite = Sprite.Create(texture, new Rect(0, 0, resolution, resolution), new Vector2(0.5f, 0.5f));
        return sprite;
    }

    private void OnDrawGizmosSelected()
    {
        if (target != null)
        {
            Gizmos.color = Color.yellow;
            Gizmos.DrawWireSphere(target.position, visionRadius);

            if (useAngleVision)
            {
                Vector3 forward = target.transform.forward;
                float halfAngle = visionAngle / 2;

                Vector3 left = Quaternion.Euler(0, -halfAngle, 0) * forward;
                Vector3 right = Quaternion.Euler(0, halfAngle, 0) * forward;

                Gizmos.color = Color.green;
                Gizmos.DrawLine(target.position, target.position + left * visionRadius);
                Gizmos.DrawLine(target.position, target.position + right * visionRadius);
            }
        }
    }

    public void SetTarget(Transform newTarget)
    {
        target = newTarget;
        if (!isInitialized && target != null)
        {
            InitializeCameraPosition();
        }
    }

    public void SetVisionRadius(float radius)
    {
        visionRadius = radius;
    }

    public void SetVisionAngle(float angle)
    {
        visionAngle = angle;
        if (visionMaskRenderer != null)
        {
            visionMaskRenderer.sprite = CreateVisionMaskSprite();
        }
    }

    public void SetFogColor(Color color)
    {
        fogColor = color;
    }

    public void SetUseAngleVision(bool useAngle)
    {
        useAngleVision = useAngle;
        if (visionMaskRenderer != null)
        {
            visionMaskRenderer.sprite = CreateVisionMaskSprite();
        }
    }

    public void SetFollowSpeed(float speed)
    {
        followSpeed = speed;
    }

    public void SetSmoothTime(float time)
    {
        smoothTime = time;
    }
}