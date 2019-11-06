using System;
using UnityEngine;
using UnityEngine.UI;

public class DateTextController : MonoBehaviour
{
    public Text clockText;

    void Update()
    {
        clockText.text = string.Format("{0:MM/dd yyyy}", DateTime.Now);
    }
}