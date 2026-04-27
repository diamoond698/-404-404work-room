using UnityEngine;

public class CameraFollowWithVision : MonoBehaviour
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
        if (visionMaskRenderer != null)
        {
            visionMask.transform.position = target.position;
            visionMask.transform.rotation = target.rotation;

            visionMask.transform.localScale = new Vector3(visionRadius * 2, visionRadius * 2, 1);

            Material material = visionMaskRenderer.material;
            if (material == null)
            {
                material = new Material(Shader.Find("Unlit/Transparent"));
                visionMaskRenderer.material = material;
            }

            material.SetColor("_Color", fogColor);
        }
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
