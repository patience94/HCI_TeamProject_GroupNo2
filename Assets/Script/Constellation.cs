﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Constellation : MonoBehaviour
{

    
    [HideInInspector]
    public bool fadeOn = false; // Fade 상태
    SpriteRenderer myRender;
    //SpriteRenderer ExpRender;
    //string ObjectName;
    //string ExpName;
    //GameObject Explanation;
    bool fadeOnCoroutineRun = false; // 코루틴이 실행중인지 체크용 bool 변수 
    bool fadeOffCoroutineRun = false;
    IEnumerator currentCorutine; // 현재 실행중인 코루틴 
    float fades; // 알파값 
    //float fades2;

    [SerializeField]
    private float fadesPow = 0.04f; // fade 되는 값의 변화 
    private float fadesPow2 = 0.3f;
    [SerializeField]
    private float fadeOffMin = 0.3f; // 최소 알파값

    private void Awake()
    {
        myRender = GetComponent<SpriteRenderer>();
        /*ObjectName = gameObject.name;
        ExpName = ObjectName+"_Explanation";
        Debug.Log(ExpName);
        Explanation = GameObject.Find(ExpName);
        ExpRender = Explanation.GetComponent<SpriteRenderer>();*/
    }

    public void FadeReset()
    {
        if (fadeOnCoroutineRun)
        {
            StopCoroutine(currentCorutine);
            fadeOnCoroutineRun = false;

        }
        fadeOn = false;
       
        currentCorutine = FadeOff();
        StartCoroutine(currentCorutine);
    }

    public void FadeStart()
    {
        if (!fadeOn)
        {
            fadeOn = true;
            if (fadeOffCoroutineRun)
            {
                StopCoroutine(currentCorutine);
                fadeOffCoroutineRun = false;
            }

            currentCorutine = FadeOn();
            StartCoroutine(currentCorutine);
        }
    }

    IEnumerator FadeOff()
    {
        fadeOffCoroutineRun = true;

        while (fades > fadeOffMin)
        {
            fades -= fadesPow;
            //fades2 -= fadesPow2;
            myRender.color = new Color(1, 1, 1, fades);
            //ExpRender.color = new Color(1, 1, 1, fades2);
            yield return new WaitForSeconds(0.1f);
        }

        fadeOffCoroutineRun = false;
    }


    IEnumerator FadeOn()
    {
        fadeOnCoroutineRun = true;

        while (fades < 1)
        {
            fades += fadesPow;
            //fades2 += fadesPow2;
            myRender.color = new Color(1, 1, 1, fades);
            //ExpRender.color = new Color(1, 1, 1, fades2);
            yield return new WaitForSeconds(0.1f);
        }
        fadeOnCoroutineRun = false;

    }
    





}