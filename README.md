# 本地部署生成字幕(双语字幕)服务
## 介绍
🤖️ 一种利用[whisper](https://github.com/openai/whisper)和[m2m100](https://github.com/facebookresearch/fairseq/tree/main/examples/m2m_100)分别作为 语言转文字(ASR)和机器翻译的模型，来使用FastAPI构建的服务

💡 主要代码参考[![](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/feynlee/whisper2subtitles/blob/main/Whisper2subtitles.ipynb)
[Ziyue Li](https://github.com/feynlee)的https://github.com/openai/whisper/discussions/504


✅ 为了让项目能够最快的跑通，默认模型使用的是whisper_tiny和m2m100_418M

关于境内模型下载方法详见该项目 TODO

- whisper 模型默认存储在/workspace/models/whisper_models目录下
- m2m100 模型默认存储在/workspace/models下

## 安装

为了更好的体验 建议使用GPU来部署服务，当然CPU也可以跑得起来，因为模型都是基于PyTorch。

- 建议使用Docker进行服务部署，为了在docker中使用gpu你需要需要在主机上安装 [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-container-toolkit)

```shell
Docker build -t generate_subtitle .
```

建议使用docker-compose来进行容器管理

```
docker-compose up -d
```

- 本机安装

```
pip install -r requirements.txt
```

## 使用

访问http://ip:18080/docs 接口文档

## TODO

|           事项            | 是否完成 |
| :-----------------------: | :------: |
|  国内huggingface模型下载  |    ⏳     |
|       服务部署优化        |    ⏳     |
|       处理流式音频        |    ⏳     |
| 一个优雅的前端页面好基友👬 |    ⏳     |

