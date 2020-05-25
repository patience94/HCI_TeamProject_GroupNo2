using UnityEngine;
using System.Collections.Generic;
using System.Collections;

public class CameraObrbit : MonoBehaviour
{
    public float MinDistance = -1000f;
    public float MaxDistance = 130f;
    float distance = 1000;
    float distanceTarget;
    Vector2 mouse;
    Vector2 mouseOnDown;
    Vector2 rotation;
    Vector2 target = new Vector2(Mathf.PI * 3 / 2, Mathf.PI / 6);
    Vector2 targetOnDown;

    public float speed = 25.0f;
    public Transform cameraTarget;
    private Camera thisCamera;
    private Vector3 worldDefalutForward;


    // Use this for initialization
    float time = 0;
    float fades = 0.0f;
    

    void Start () {
        distanceTarget = transform.position.magnitude;
        thisCamera = GetComponent<Camera>();
        worldDefalutForward = transform.forward;
        
    }
    bool down = false;
    // Update is called once per frame
    void Update()
    {
        if (Input.touchCount > 0)
        {
            if(Input.touches[0].phase== TouchPhase.Began)
            {
                down = true;
                mouseOnDown.x = Input.touches[0].position.x;
                mouseOnDown.y = -Input.touches[0].position.y;

                targetOnDown.x = target.x;
                targetOnDown.y = target.y;
            }
            else if(Input.touches[0].phase== TouchPhase.Canceled||
                Input.touches[0].phase== TouchPhase.Ended)
            {
                down = false;
            }
        }
        else
        {
            if (Input.GetMouseButtonDown(0))
            {
                down = true;
                mouseOnDown.x = Input.mousePosition.x;
                mouseOnDown.y = -Input.mousePosition.y;

                targetOnDown.x = target.x;
                targetOnDown.y = target.y;
            }
            else if (Input.GetMouseButtonUp(0))
            {
                down = false;
            }
        }
        if(down)
        {
            if (Input.touchCount > 0)
            {
                mouse.x = Input.touches[0].position.x;
                mouse.y = -Input.touches[0].position.y;
            }
            else
            {
                mouse.x = Input.mousePosition.x;
                mouse.y = -Input.mousePosition.y;
            }
            float zoomDamp = distance / 1;

            target.x = targetOnDown.x + (mouse.x - mouseOnDown.x) * 0.005f* zoomDamp;
            target.y = targetOnDown.y + (mouse.y - mouseOnDown.y) * 0.005f* zoomDamp;
            
            target.y = Mathf.Clamp(target.y, -Mathf.PI / 2 + 0.01f, Mathf.PI / 2 - 0.01f);
        }
        float scroll = Input.GetAxis("Mouse ScrollWheel") * speed;

        //최대 줌인
        if (thisCamera.fieldOfView <= 20.0f && scroll < 0)
        {
            thisCamera.fieldOfView = 20.0f;
        }

        //최대 줌 아웃
        else if (thisCamera.fieldOfView >= 70.0f && scroll > 0)
        {
            thisCamera.fieldOfView = 70.0f;  
		}
        //줌인 아웃 하기
        else
        {
            thisCamera.fieldOfView += scroll;
		}
        
        distanceTarget -= Input.GetAxis("Mouse ScrollWheel");
         distanceTarget = Mathf.Clamp(distanceTarget, MinDistance, MaxDistance);

        rotation.x += (target.x - rotation.x) * 0.1f;
        rotation.y += (target.y - rotation.y) * 0.1f;
        distance += (distanceTarget - distance) * 0.3f;
        Vector3 position;
        position.x = distance * Mathf.Sin(rotation.x) * Mathf.Cos(rotation.y);
        position.y = distance * Mathf.Sin(rotation.y);
        position.z = distance * Mathf.Cos(rotation.x) * Mathf.Cos(rotation.y);
        transform.position = position;
        transform.LookAt(Vector3.zero);


        int layerMask = 1 << LayerMask.NameToLayer("Constellation");
        SpriteRenderer render;
        RaycastHit hit;
        Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);

        if (Physics.Raycast(transform.position, transform.TransformDirection(Vector3.forward), out hit, Mathf.Infinity, layerMask))
        {
            Debug.Log("hit");
            time += Time.deltaTime;
            render = hit.transform.GetComponent<SpriteRenderer>();
            if (fades < 1.0f && time >= 0.1f)
            {
                fades += 0.04f;
                time = 0;
                render.color = new Color(1, 1, 1, fades);
            }
        }
        else
        {
            time = 0;
            fades = 0;
        }
        
    }
}
