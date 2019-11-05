using System;
using UnityEngine;
using UnityEngine.UI;

public class TimeTextController : MonoBehaviour
{
    
    public Text clockText;

    void Update()
    {
        clockText.text = DateTime.Now.ToShortTimeString();
    }
    
}