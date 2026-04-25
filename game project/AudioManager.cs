using UnityEngine;
using System.Collections.Generic;

public class AudioManager : MonoBehaviour
{
    public static AudioManager Instance;

    [Header("音频源")]
    public AudioSource musicSource;
    public AudioSource sfxSource;

    [Header("音效库")]
    public List<Sound> sounds = new List<Sound>();

    [System.Serializable]
    public class Sound
    {
        public string name;
        public AudioClip clip;
        [Range(0f, 1f)] public float volume = 1f;
        [Range(0.5f, 2f)] public float pitch = 1f;
        public bool loop = false;
    }

    private Dictionary<string, Sound> soundDict = new Dictionary<string, Sound>();

    void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
        }
        else
        {
            Destroy(gameObject);
            return;
        }

        // 初始化音效字典
        foreach (var sound in sounds)
        {
            soundDict[sound.name] = sound;
        }

        // 设置音频源
        if (musicSource == null)
            musicSource = gameObject.AddComponent<AudioSource>();

        if (sfxSource == null)
            sfxSource = gameObject.AddComponent<AudioSource>();

        musicSource.loop = true;
        sfxSource.loop = false;
    }

    // 播放音效
    public void PlaySFX(string soundName)
    {
        if (soundDict.ContainsKey(soundName))
        {
            Sound sound = soundDict[soundName];
            sfxSource.PlayOneShot(sound.clip, sound.volume);
        }
        else
        {
            Debug.LogWarning($"音效 {soundName} 不存在！");
        }
    }

    // 播放音乐
    public void PlayMusic(string soundName)
    {
        if (soundDict.ContainsKey(soundName))
        {
            Sound sound = soundDict[soundName];
            musicSource.clip = sound.clip;
            musicSource.volume = sound.volume;
            musicSource.loop = sound.loop;
            musicSource.Play();
        }
    }

    // 停止音乐
    public void StopMusic()
    {
        musicSource.Stop();
    }

    // 设置音量
    public void SetMusicVolume(float volume)
    {
        musicSource.volume = Mathf.Clamp01(volume);
    }

    public void SetSFXVolume(float volume)
    {
        sfxSource.volume = Mathf.Clamp01(volume);
    }
}