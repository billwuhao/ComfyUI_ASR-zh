[中文](README.md)|[English](README-EN.md)

# 中文自动语音识别 的 ComfyUI 节点

准确而快速的自动语音识别（ASR）. 可识别唱歌, 支持标点符号, 时间戳预测. 

![](https://github.com/billwuhao/ComfyUI_ASR-zh/blob/main/images/2025-05-20_15-05-33.png)

## 用法

- 自动添加歌词:

![](https://github.com/billwuhao/ComfyUI_ASR-zh/blob/main/images/2025-05-20_16-00-47.png)

## 📣 更新

[2025-05-20]⚒️: 发布 v1.0.0。

## 安装

```
cd ComfyUI/custom_nodes
git clone https://github.com/billwuhao/ComfyUI_ASR-zh.git
cd ComfyUI_ASR-zh
pip install -r requirements.txt

# python_embeded
./python_embeded/python.exe -m pip install -r requirements.txt
```

## 模型下载

- [Belle-whisper-large-v3-zh-punct-ct2](https://hf-mirror.com/k1nto/Belle-whisper-large-v3-zh-punct-ct2/tree/main): 全部下载放到 `ComfyUI/models/TTS` 目录下.


## 鸣谢

[k1nto](https://hf-mirror.com/k1nto/Belle-whisper-large-v3-zh-punct-ct2)
[faster-whisper](https://github.com/SYSTRAN/faster-whisper)