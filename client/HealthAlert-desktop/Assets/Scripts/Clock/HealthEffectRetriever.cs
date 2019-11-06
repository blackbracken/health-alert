using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;

public class HealthEffectRetriever : MonoBehaviour
{
    public Text temperatureText;
    public Text humidityText;
    public Text climateText;
    public Text dryText;
    public ParticleSystem ringParticpe;

    private float _currentTime;

    [RuntimeInitializeOnLoadMethod]
    static void OnRuntimeMethodLoad()
    {
        Screen.SetResolution( 16 * 50, 9 * 50, false, 60);
    }
    
    private void Start()
    {
        
        StartCoroutine(FetchHealthEffect());
    }

    private void Update()
    {
        _currentTime += Time.deltaTime;
        
        if (_currentTime >= 5f)
        {
            StartCoroutine(FetchHealthEffect());
            _currentTime = 0;
        }
    }

    private IEnumerator FetchHealthEffect()
    {
        var request = UnityWebRequest.Get("http://" + AddressHolder.Address);
        yield return request.Send();
        Debug.Log(request.downloadHandler.text);

        var healthEffectData = JsonUtility.FromJson<HealthEffectData>(request.downloadHandler.text);
        
        temperatureText.text = string.Format("{0:F1}°C", healthEffectData.temperature);
        humidityText.text = string.Format("{0:F1}%", healthEffectData.humidity);
        
        switch (healthEffectData.climate_effect.ToUpper())
        {
            case "HEATSTROKE_NOTICE":
                climateText.text = "熱中症に注意";
                ringParticpe.startColor = Color.yellow;
                break;
            case "HEATSTROKE_ALERT":
                climateText.text = "熱中症に警戒を!";
                ringParticpe.startColor = Color.red;
                break;
            case "VIRUS_NOTICE":
                climateText.text = "インフルエンザに注意";
                ringParticpe.startColor = Color.cyan;
                break;
            case "VIRUS_ALERT":
                climateText.text = "インフルエンザに警戒を!";
                ringParticpe.startColor = Color.magenta;
                break;
            default:
                climateText.text = "今日も良い1日を";
                ringParticpe.startColor = Color.green;
                break;
        }

        switch (healthEffectData.dry_effect.ToUpper())
        {
            case "DRY":
                dryText.text = "乾燥情報: 乾き気味";
                break;
            default:
                dryText.text = "乾燥情報: 普通";
                break;
        }
    }
}