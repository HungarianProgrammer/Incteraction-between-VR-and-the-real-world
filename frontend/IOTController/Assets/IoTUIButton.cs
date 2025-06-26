using System.Collections;
using System.Text;
using TMPro;
using UnityEngine;
using UnityEngine.Networking;

public class IoTUIButton : MonoBehaviour
{
    public enum TestMode { Simulated, DummyRemote, RealBackend }
    [Header("Choose how ALL buttons behave")]
    public TestMode mode = TestMode.Simulated;

    [Header("Only used when mode = RealBackend")]
    public string baseURL = "http://YOUR_PI_IP:5000";

    [Header("UI element that shows results")]
    public TMP_Text outputText;

    // ───────── PUBLIC METHODS  ──────────────
    public void GetTemperature() => StartCoroutine(HandleGet("temperature"));
    public void GetHumidity()    => StartCoroutine(HandleGet("humidity"));
    public void LightOn()        => StartCoroutine(HandlePost("light", "{\"state\":\"on\"}"));
    public void LightOff()       => StartCoroutine(HandlePost("light", "{\"state\":\"off\"}"));

    // ───────── CENTRAL ROUTINES ─────────────
    private IEnumerator HandleGet(string key)
    {
        switch (mode)
        {
            case TestMode.Simulated:
                outputText.text = key == "temperature"
                    ? $"Temp {Random.Range(20f,30f):0.0} °C (sim)"
                    : $"Humidity {Random.Range(40f,60f):0.0}% (sim)";
                yield break;

            case TestMode.DummyRemote:
                yield return SendRequest($"https://postman-echo.com/get?key={key}", "GET");
                yield break;

            case TestMode.RealBackend:
                yield return SendRequest($"{baseURL}/api/mqtt/{key}", "GET");
                yield break;
        }
    }

    private IEnumerator HandlePost(string key, string json)
    {
        switch (mode)
        {
            case TestMode.Simulated:
                outputText.text = key == "light"
                    ? (json.Contains("on") ? "Light switched ON (sim)" : "Light switched OFF (sim)")
                    : $"Posted {key} (sim)";
                yield break;

            case TestMode.DummyRemote:
                yield return SendRequest("https://postman-echo.com/post", "POST", json);
                yield break;

            case TestMode.RealBackend:
                yield return SendRequest($"{baseURL}/api/mqtt/{key}", "POST", json);
                yield break;
        }
    }

    // ───────── LOW-LEVEL HTTP  ──────────────
    private IEnumerator SendRequest(string url, string verb, string body = null)
    {
        outputText.text = $"{verb} {url} …";

        UnityWebRequest req =
            verb == "GET"
            ? UnityWebRequest.Get(url)
            : BuildPostReq(url, body);

        yield return req.SendWebRequest();

        outputText.text =
            req.result == UnityWebRequest.Result.Success
            ? $"✓ {req.downloadHandler.text}"
            : $"✗ {req.error}";
    }

    private UnityWebRequest BuildPostReq(string url, string body)
    {
        var req = new UnityWebRequest(url, "POST");
        byte[] data = Encoding.UTF8.GetBytes(body);
        req.uploadHandler   = new UploadHandlerRaw(data);
        req.downloadHandler = new DownloadHandlerBuffer();
        req.SetRequestHeader("Content-Type", "application/json");
        return req;
    }
}
