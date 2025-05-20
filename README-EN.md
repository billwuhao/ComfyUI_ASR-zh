[Chinese](README.md)|[English](README-EN.md)

# ComfyUI Nodes for Chinese Automatic Speech Recognition

Accurate and fast Automatic Speech Recognition (ASR). Can recognize singing, supports punctuation, and timestamp prediction.

![](https://github.com/billwuhao/ComfyUI_ASR-zh/blob/main/images/2025-05-20_15-05-33.png)

## Usage

- Automatically add lyrics:

![](https://github.com/billwuhao/ComfyUI_ASR-zh/blob/main/images/2025-05-20_16-00-47.png)

## 📣 Updates

[2025-05-20]⚒️: Released v1.0.0.

## Installation

```
cd ComfyUI/custom_nodes
git clone https://github.com/billwuhao/ComfyUI_ASR-zh.git
cd ComfyUI_ASR-zh
pip install -r requirements.txt

# python_embeded
./python_embeded/python.exe -m pip install -r requirements.txt
```

## Model Download

- [Belle-whisper-large-v3-zh-punct-ct2](https://hf-mirror.com/k1nto/Belle-whisper-large-v3-zh-punct-ct2/tree/main): Download all files and place them in the `ComfyUI/models/TTS` directory.


## Acknowledgements

[k1nto](https://hf-mirror.com/k1nto/Belle-whisper-large-v3-zh-punct-ct2)
[faster-whisper](https://github.com/SYSTRAN/faster-whisper)
