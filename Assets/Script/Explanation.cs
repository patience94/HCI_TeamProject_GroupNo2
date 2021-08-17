﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Explanation : MonoBehaviour
{


    [HideInInspector]
    public bool fadeOn = false; // Fade 상태
    SpriteRenderer ExpRender;
    string ObjectName;
    string ExpName;
    GameObject ExpObject;
    bool fadeOnCoroutineRun = false; // 코루틴이 실행중인지 체크용 bool 변수 
    bool fadeOffCoroutineRun = false;
    IEnumerator currentCorutine; // 현재 실행중인 코루틴 
    float fades; // 알파값 


    [SerializeField]
    private float fadesPow = 0.3f; // fade 되는 값의 변화 
    [SerializeField]
    private float fadeOffMin = 0.0f; // 최소 알파값

    private void Update()
    {
        ObjectName = gameObject.name;
        ExpName = ObjectName + "_Explanation";
        ExpObject = GameObject.Find(ExpName);
        ExpRender = ExpObject.GetComponent<SpriteRenderer>();
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
            ExpRender.color = new Color(1, 1, 1, fades);
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
            ExpRender.color = new Color(1, 1, 1, fades);
            yield return new WaitForSeconds(0.1f);
        }
        fadeOnCoroutineRun = false;

    }






}