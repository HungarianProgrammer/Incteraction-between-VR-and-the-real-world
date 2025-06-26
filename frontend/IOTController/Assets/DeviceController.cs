using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class DeviceController : MonoBehaviour
{
    public enum TestMode { Simulated, DummyRemote, RealBackend }
    [Header("Choose how the button behaves")]
    public TestMode mode = TestMode.Simulated;

    [Header("Only used when mode = RealBackend")]
    public string deviceURL = "http://YOUR_PI_IP:PORT/api/lamp/on";

    // ---------------------------------------------------------------------

    public void SendCommand()                // Hook this to Button OnClick()
    {
        switch (mode)
        {
            case TestMode.Simulated:
                StartCoroutine(SimulateRequest());
                break;

            case TestMode.DummyRemote:
                StartCoroutine(SendRequest("https://postman-echo.com/get"));
                break;

            case TestMode.RealBackend:
                StartCoroutine(SendRequest(deviceURL));
                break;
        }
    }

    // ---------------------------------------------------------------------
    // NETWORK / SIMULATION COROUTINES
    // ---------------------------------------------------------------------

    private IEnumerator SimulateRequest()
    {
        Debug.Log("-- Simulating REST call …");
        yield return new WaitForSeconds(0.5f);
        Debug.Log("✓ Simulated command success");
    }

    private IEnumerator SendRequest(string url)
    {
        Debug.Log($"-- Hitting {url}");
        UnityWebRequest req = UnityWebRequest.Get(url);

        yield return req.SendWebRequest();

        if (req.result == UnityWebRequest.Result.Success)
        {
            Debug.Log($"✓ Success ⇒ {req.downloadHandler.text}");
        }
        else
        {
            Debug.LogError($"✗ Failed ⇒ {req.error}");
        }
    }
}
