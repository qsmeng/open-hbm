## 文生图与AIGC  
### 工具与框架  秋叶整合包
- **Stable Diffusion WebUI**：无代码
- **ComfyUI**：工作流

### 在线平台
- [liblib在线ComfyUI](https://www.liblib.art/comfy)
- [SiliconCloud](https://cloud.siliconflow.cn/models?types=to-image)
- [ComfyUI-CPU爽玩版【ai佬】 - CloudStudio](https://cloudstudio.net/a/26004515719987200/)
- [Replicate稳定扩散API](https://replicate.com/stability-ai/stable-diffusion)

### 环境配置（CUDA）  
- [win11 WSL ubuntu安装CUDA、CUDNN、TensorRT](https://blog.csdn.net/qq_40102732/article/details/135182310)
- [【AI大模型】安装NVIDIA Container Toolkit](https://blog.csdn.net/tanlintanlin/article/details/138597128)
```bash  
# CUDA 12.5安装（WSL）
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/12.5.0/local_installers/cuda-repo-wsl-ubuntu-12-5-local_12.5.0-1_amd64.deb
dpkg -i cuda-repo-wsl-ubuntu-12-5-local_12.5.0-1_amd64.deb
cp /var/cuda-repo-wsl-ubuntu-12-5-local/cuda-*-keyring.gpg /usr/share/keyrings/
apt-get update
apt-get -y install cuda-toolkit-12-5
apt install python3-xyz
```  

### 模型选择 civitai
#### 基础模型
 sd1.5
 sdxl
 pony
- [Pony最佳东亚女孩模型再次升级](https://zhuanlan.zhihu.com/p/739572260)
 sd3
- [SD3创作指南](https://www.bilibili.com/read/cv35654766/?jump_opus=1)
 sd3.5
 hunyuandit
- [混元DIT(HunyuanDIT)训练器安装使用教程](https://zhuanlan.zhihu.com/p/711053172)
- [Flux Style Captioning Differences - Training Diary](https://civitai.com/articles/6792/flux-style-captioning-differences-training-diary)
 flux.1(截至2024年底最优)
  ```  
  # Flux1推荐使用五种采样器与调度器的搭配组合
  ipdmn+simple | uni_pc_bh2+simple | euler+beta | euler+simple | dpmpp+sgm_uniform  
  ```  
#### 微调模型
- [Civitai: The Home of Open-Source Generative AI](https://civitai.com/)
- [majicMIX realistic 麦橘写实 - v7](https://civitai.com/models/43331/majicmix-realistic)
- [MIST XL Hyper Character Style Model](https://civitai.com/models/452459/mist-xl-hyper-character-style-model-aiartist)
- [OnlyRealistic | 《唯》· 超高清真人写实](https://civitai.com/models/112756/onlyrealistic-or)

#### 儿童故事生成
- [TencentARC/SEED-Story: SEED-Story: Multimodal Long Story Generation with Large Language Model](https://github.com/TencentARC/SEED-Story)

#### 模型推荐
- [出图效率倍增！47个高质量的 Stable Diffusion 常用模型推荐](https://blog.csdn.net/ice829/article/details/138843674)
- [收集和梳理中文Stable-Diffusion相关的开源模型](https://github.com/leeguandong/Awesome-Chinese-Stable-Diffusion)
- [10 个值得下载的模型 – Comflowy](https://www.comflowy.com/zh-CN/blog/ten-models-worth-downloading)

### lora训练
- [Florence2:使用LLM助力你的AI绘图](https://blog.csdn.net/text2203/article/details/140847576)
- [Auto-Tagger(Ollama-Compatible) || 自动打标器](https://civitai.com/models/643332/auto-taggerollama-compatible-oror-ollama)

### ComfyUI
- [comfyanonymous/ComfyUI: The most powerful and modular stable diffusion GUI](https://github.com/comfyanonymous/ComfyUI)
- [comfyanonymous/ComfyUI_examples: Examples of ComfyUI workflows](https://github.com/comfyanonymous/ComfyUI_examples)
- [API调用ComfyUI模板高效文生图-腾讯云开发者社区](https://cloud.tencent.com/developer/article/2443080)
  - 保存图像参数模板：  
    ```  
    FLUX1\%date:yyyyMMdd%_%LoraLoader.lora_name%\%date:hhmmss%  
    ```  
-[ComfyUI开发指南](https://zhuanlan.zhihu.com/p/687537814)
-[ComfyUI开发指南 -- 插件开发（上）](https://zhuanlan.zhihu.com/p/700077749)
-[ComfyUI开发指南 -- 插件开发（下）](https://zhuanlan.zhihu.com/p/700500359?utm_id=0)