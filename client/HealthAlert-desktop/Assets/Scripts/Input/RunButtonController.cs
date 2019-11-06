using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class RunButtonController : MonoBehaviour
{
    public InputField addressInput;

    public void OnClick()
    {
        AddressHolder.Address = addressInput.text;
        SceneManager.LoadScene ("Clock");
    }
}