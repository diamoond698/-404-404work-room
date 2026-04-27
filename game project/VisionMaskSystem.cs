using UnityEngine;

public class VisionMaskSystem : MonoBehaviour
{
    [Header("跟随设置")]
    [SerializeField]
    private Transform target;
    [SerializeField]
    private float followSpeed = 5f;
    [SerializeField]
    private Vector3 offset = new Vector3(0, 0, -10);

    [Header("视野设置")]
    [SerializeField]
    private float visionRadius = 5f;
    [SerializeField]
    private float visionAngle = 120f;
    [SerializeField]
    private Color fogColor = new Color(0, 0, 0, 0.8f);

    [Header("视野遮罩")]
    [SerializeField]
    private GameObject visionMask;
    [SerializeField]
    private SpriteRenderer visionMaskRenderer;

    private void Start()
    {
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

        UpdateVisionMask();
    }

    private void Update()
    {
        if (target != null)
        {
            Vector3 targetPosition = target.position + offset;
            transform.position = Vector3.Lerp(transform.position, targetPosition, followSpeed * Time.deltaTime);

            UpdateVisionMask();
        }
    }

    private void UpdateVisionMask()
    {
        if (visionMaskRenderer != null && target != null)
        {
            visionMask.transform.position = target.position;
            visionMask.transform.rotation = target.rotation;

            visionMask.transform.localScale = new Vector3(visionRadius * 2, visionRadius * 2, 1);

            if (visionMaskRenderer.material == null)
            {
                Material material = new Material(Shader.Find("Unlit/Transparent"));
                visionMaskRenderer.material = material;
            }

            visionMaskRenderer.material.color = fogColor;
        }
    }

    private Sprite CreateVisionMaskSprite()
    {
        int width = 512;
        int height = 512;
        Texture2D texture = new Texture2D(width, height, TextureFormat.RGBA32, false);

        for (int x = 0; x < width; x++)
        {
            for (int y = 0; y < height; y++)
            {
                Vector2 center = new Vector2(width / 2, height / 2);
                Vector2 point = new Vector2(x, y);
                float distance = Vector2.Distance(center, point);
                float radius = width / 2;

                if (distance <= radius)
                {
                    float alpha = 1.0f - (distance / radius);
                    texture.SetPixel(x, y, new Color(0, 0, 0, alpha));
                }
                else
                {
                    texture.SetPixel(x, y, new Color(0, 0, 0, 1));
                }
            }
        }

        texture.Apply();

        Sprite sprite = Sprite.Create(texture, new Rect(0, 0, width, height), new Vector2(0.5f, 0.5f));
        return sprite;
    }

    private void OnDrawGizmosSelected()
    {
        if (target != null)
        {
            Gizmos.color = Color.yellow;
            Gizmos.DrawWireSphere(target.position, visionRadius);

            Vector3 forward = target.transform.forward;
            float halfAngle = visionAngle / 2;

            Vector3 left = Quaternion.Euler(0, -halfAngle, 0) * forward;
            Vector3 right = Quaternion.Euler(0, halfAngle, 0) * forward;

            Gizmos.color = Color.green;
            Gizmos.DrawLine(target.position, target.position + left * visionRadius);
            Gizmos.DrawLine(target.position, target.position + right * visionRadius);
        }
    }

    public void SetTarget(Transform newTarget)
    {
        target = newTarget;
    }

    public void SetVisionRadius(float radius)
    {
        visionRadius = radius;
        UpdateVisionMask();
    }

    public void SetVisionAngle(float angle)
    {
        visionAngle = angle;
    }

    public void SetFogColor(Color color)
    {
        fogColor = color;
        UpdateVisionMask();
    }
}
