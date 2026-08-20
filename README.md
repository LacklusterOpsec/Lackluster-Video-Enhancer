# REAL Video Enhancer
<h1>NOTICE</h1>
<h3>This is an actively maintained fork of REAL Video Enhancer with bug fixes, stability improvements, and performance optimizations applied on top of the archived upstream.</h3>

## Changes in this fork

**Newest additions**
- Added **bfloat16** as a precision option for the PyTorch backend. `Auto` now uses bfloat16 on RTX 30-series/Ampere+ GPUs (same speed as fp16, better dynamic range — no overflow on bright/HDR content) and fp16 elsewhere. The TensorRT backend always uses fp16/fp32 engines (bf16 is not supported for TensorRT engines).
- Added **PyTorch 2.13** (CUDA 13 / Blackwell / RTX 50-series) and **TensorRT 11** as selectable install options. Older versions (2.9 / 2.8 / 2.6) are kept in the dropdown for compatibility with older GPUs — see the tooltip notes in the app.
- **TensorRT engine fixes on the 2.13 / TRT 11 stack**: bf16 is never passed to TRT engine builds, and the RIFE `grid_sampler` decomposition that caused ghosting/flash artifacts on torch-tensorrt 2.13 has been replaced with the native grid_sampler path (engines rebuild automatically with a `_gsnative` suffix).
- Fixed the PyInstaller build (`backports` runtime error on Python 3.11) and made `build.py` stop force-recreating an existing venv.
- Fixed the GitHub Actions CI for this fork (branches + release notes from this repo, Node 24 runtimes, macOS Homebrew tap-trust/llvm fixes); `build-prerelease` builds Windows/Linux/macOS and publishes a release.
- App update checks, the home-tab changelog, and backend downloads now point at **this fork** instead of upstream.
- Windows installer (NSIS) version synced to 2.4.2, branded as **LacklusterOpsec**, with the start-menu shortcut installed directly (no company subfolder).

**Bug fixes**
- Fixed FFmpeg reading randomly stopping mid-render (`-nostdin` on the reader process)
- Fixed rotated / iPhone portrait videos failing to render (rotation-aware dimensions, safe crop clamping, `-noautorotate` in border detection)
- Fixed PySceneDetect misbehaving when restoration models are enabled
- Fixed render-thread crashes hanging the whole app (global exception handler with traceback)
- Fixed pause/resume race with shared-memory pause block at startup
- Fixed NCNN scale detection crashing when a model name does not include the scale
- Fixed segmented scene detection only evaluating part of the image
- Fixed NCNN upscale frames reporting pre-scale dimensions
- Fixed decimal (non-integer) interpolation frame timing and cache step
- Fixed progress/ETA undercounting and wrong FPS after pausing
- Failed simple-install now exits cleanly instead of launching a broken UI

**Performance / stability**
- Removed a global CUDA synchronization and a redundant tensor clone per frame
- Scene detection now downscales on the GPU (no full-res frame copy to CPU per frame)
- Output override scale resizing moved off the CPU path (GPU resize when available)
- NCNN fallback reuses its extractor instead of allocating per frame
- TensorRT engine build now clears VRAM after compiling
- AV1 / AV1 NVENC quality presets adjusted
- Version bumped to 2.4.2

## Compatibility

### PyTorch versions (selectable in the Download tab)

| Version | CUDA wheel | GPU support | Notes |
|---|---|---|---|
| **2.13.0** (default) | `+cu130` | RTX 20/30/40/50 (Turing / sm_75 and newer) | Newest. Best on RTX 50-series / Blackwell. Pairs with TensorRT 11. Requires CUDA 13-capable drivers. |
| **2.9.0** | `+cu130` | RTX 20/30/40 (Turing+) | Stable all-rounder. |
| **2.8.0** | `+cu129` | RTX 20/30/40 (Turing+) | |
| **2.6.0** | `+cu118` | GTX 10/16, V100 and older (Pascal/Volta/Turing+) | Legacy fallback. Use this if newer versions fail to load on your GPU. |

Notes:
- **CUDA 13 (`+cu130`) requires Turing or newer (sm_7.5+).** Maxwell/Pascal/Volta GPUs (GTX 900/10, V100) must use the CUDA 11.8 build (**2.6.0**).
- Volta (V100) support was dropped from newer CUDA 12.8+/13 wheel sets; use 2.6.0 for those cards.
- **ROCm (AMD, Linux only):** 2.13 → ROCm 7.2, 2.9/2.8 → ROCm 6.4, 2.6 → ROCm 6.2.4.
- **XPU (Intel):** available on all listed versions.
- **MPS (Apple Silicon):** locked to PyTorch 2.9.0 for uint16 (HDR) support.

### Precision options

| Precision | GPU support | Notes |
|---|---|---|
| **auto** (default) | — | PyTorch backend: **bfloat16** on RTX 30-series / Ampere+ (sm_80+), **float16** elsewhere, **float32** if half precision is unavailable. TensorRT backend: always fp16/fp32 engines. |
| **float16** | All CUDA/ROCm/XPU/MPS | Fastest, lowest VRAM. |
| **bfloat16** | RTX 30-series+ (Ampere, sm_80+) | PyTorch backend only. Same speed as float16, but with an 8-bit exponent — no overflow on bright/HDR content. Falls back to float32 automatically if a model doesn't support it. TensorRT uses fp16 instead. |
| **float32** | All | Slowest, most compatible. |

### TensorRT

| PyTorch | TensorRT | torch-tensorrt | Notes |
|---|---|---|---|
| **2.13.0** | **11.0.0.114** | 2.13.0 | CUDA 13. Requires Turing+ (RTX 20-series / sm_75+). |
| 2.9.0 / 2.8.0 / 2.6.0 | 10.12.0.36 | matching torch version | Older TRT 10 line. |

Notes:
- TensorRT requires an NVIDIA GPU with dedicated tensor cores — **RTX 20-series (Turing) or newer**. Not available on GTX 10/16-series or older.
- TensorRT 11 requires CUDA 13-capable drivers (all RTX 20+ with recent drivers).
- TensorRT engines are built in fp16/fp32 only (no bf16 engine support).
- On torch-tensorrt 2.13 / TRT 11, the RIFE engine uses the native `grid_sampler` path (the older manual decomposition caused ghosting/flash artifacts on this stack).

### NCNN (Vulkan)

Works on any GPU with a Vulkan driver (NVIDIA, AMD, Intel, Apple Silicon). No CUDA requirement. Great fallback for older hardware or when CUDA is unavailable.

![license](https://img.shields.io/github/license/LacklusterOpsec/Lackluster-Video-Enhancer)
![Version](https://img.shields.io/badge/Version-2.4.2-blue)

<p align=center>
  <img src="https://raw.githubusercontent.com/LacklusterOpsec/Lackluster-Video-Enhancer/v2-main/icons/logo-v2.svg" width = "25%">
</p>

# Table of Contents
  
* **[Introduction](#introduction)**
* **[Features](#Features)**
* **[Compatibility](#compatibility)**
* **[Hardware Requirements](#hardware-requirements)**
* **[Models](#models)**
  * [Interpolate Models](#interpolate-models)
  * [Upscale Models](#upscale-models)
* **[Backends](#backends)**
* **[FAQ](#faq)**
  * [General App Usage](#general-application-usage) 
  * [TensorRT](#tensorrt-related-questions)
  * [ROCm](#rocm-related-questions)
  * [NCNN](#ncnn-related-questions)
* **[Cloning](#cloning)**
* **[Building](#building)**
* **[Colab Notebook](#colab-notebook)**
* **[Credits](#credits)**

# Introduction

<strong>REAL Video Enhancer</strong>  is a redesigned and enhanced version of the original Rife ESRGAN App for Linux. This program offers convenient access to frame interpolation and upscaling functionalities on Windows, Linux and MacOS, and is an alternative to outdated software like <a rel="noopener noreferrer" href="https://nmkd.itch.io/flowframes" target="_blank" >Flowframes</a> or <a rel="noopener noreferrer" href="https://github.com/mafiosnik777/enhancr" target="_blank">enhancr</a>.

<p align=center>
  <img src="https://raw.githubusercontent.com/LacklusterOpsec/Lackluster-Video-Enhancer/v2-main/screenshots/demo.png" width = "100%">
</p>
<h1>Features: </h1>
<ul>
  <li> Windows support. <strong>!!! NOTICE !!!</strong> The bin can be detected as a trojan. This is a false positive caused by pyinstaller.</li>
  <li> Ubuntu 22.04+ support on Executable and Flatpak. (20.04 can work but is now legacy) </li>
  <li> MacOS 15+ arm/x86 support </li>
  <li> Discord RPC support for Discord system package and Discord flatpak. </li>
  <li> Scene change detection to preserve sharp transitions. </li>
  <li> Preview that shows latest frame that has been rendered. </li>
  <li> TensorRT and NCNN for efficient inference across many GPUs. </li>
</ul>

# Hardware/Software Requirements
|  | Minimum | Recommended | 
 |--|--|--|
| CPU | Dual Core x64 bit | Quad Core x64 bit
| GPU | Vulkan 1.3 capable device | Nvidia RTX GPU (20 series and up)
| VRAM | 4 GB - NCNN | 8 GB - TensorRT (Nvidia, why keep making 8gb cards?)
| RAM | 16 GB | 32 GB
| Storage | 1 GB free - NCNN | 16 GB free - TensorRT
| Operating System | Windows 10/11 64bit / MacOS 14+ | Any modern Linux distro (Ubuntu 22.04+)

# Models:
### Interpolate Models:
| Model | Author | Link |
|--|--|--|
| RIFE 4.6,4.7,4.15,4.18,4.22,4.22-lite,4.25 | Hzwer | [Practical-RIFE](https://github.com/hzwer/Practical-RIFE) 
| GMFSS | 98mxr | [GMFSS_Fortuna](https://github.com/98mxr/GMFSS_Fortuna) 
| IFRNet | ltkong218 | [IFRnet](https://github.com/ltkong218/IFRNet)

### Upscale Models:
| Model | Author | Link |
|--|--|--|
| 4x-SPANkendata | Crustaceous D | [4x-SPANkendata](https://openmodeldb.info/models/4x-SPANkendata) 
| 4x-Nomos8k-SPAN series | Helaman | [4x-Nomos8k-SPAN series](https://openmodeldb.info/models/4x-Nomos8k-span-otf-strong) 
| 2x-OpenProteus | SiroSky | [OpenProteus](https://github.com/Sirosky/Upscale-Hub/releases/tag/OpenProteus) 
| 2x-AnimeJaNai V2 and V3 Sharp | The Database | [AnimeJanai](https://github.com/the-database/mpv-upscale-2x_animejanai)
| 2x-AniSD | SiroSky | [AniSD](https://github.com/Sirosky/Upscale-Hub/releases/tag/AniSD)
| AnimeSR | Tencent ARC | [AnimeSR](https://github.com/TencentARC/AnimeSR)

### Decompression Models:
| Model | Author | Link |
|--|--|--|
| DeH264 | Helaman | [1xDeH264_realplksr](https://github.com/Phhofm/models/releases/tag/1xDeH264_realplksr) 

### Denoise Models:
| Model | Author | Link |
|--|--|--|
| DRUnet | cszn | [DRUnet](https://github.com/cszn/DPIR)
| DnCNN | czsn | [DnCNN](https://github.com/cszn/DPIR)

# Backends
  | Backend | Hardware | 
  |--|--|
  | TensorRT | NVIDIA RTX GPUs
  | PyTorch  | CUDA 12.6 and ROCm 6.2 capable GPUs
  | NCNN | Vulkan 1.3 capable GPUs
 
# FAQ
### General Application Usage
  | Question | Answer | 
  |--|--|
  | What does this program attempt to accomplish? | Fast, efficient and easily accessable video interpolation (Ex: 24->48FPS) and video upscaling (Ex: 1920->3840)
  | Why is it failing to recognize installed backends? | REAL Video Enhancer uses PIP and portable python for inference, this can sometimes have issues installing. Please attempt reinstalling the app before creating an issue.

### TensorRT related questions
  |||
  |--|--|
  | Why does it take so long to begin inference? | TensorRT uses advanced optimization at the beginning of inference based on your device, this is only done once per resolution of video inputed.
  | Why does the optimization and inference fail? | The most common way an optimization can fail is **Limited VRAM** There is no fix to this except using CUDA or NCNN instead.
 
### ROCm related questions
  |||
  |--|--|
  | Why am I getting (Insert Error here)? | ROCM is buggy, please take a look at <a href="https://github.com/TNTwise/REAL-Video-Enhancer/wiki/ROCm-Help">ROCm Help</a>.

### NCNN related questions
  |||
  |--|--|
  | Why am I getting (Insert Vulkan Error here)? | This usually is an OOM (Out Of Memory) error, this can indicate a weak iGPU or very old GPU, I recommeding trying out the <a href="https://github.com/TNTwise/REAL-Video-Enhancer-Colab">Colab Notebook</a>  instead.


# Cloning:
```
# Main
git clone --recurse-submodules https://github.com/LacklusterOpsec/Lackluster-Video-Enhancer --branch v2-main
```
# Building:

<p>3 supported build methods: </p>
<p> - pyinstaller (recommended for Win/Mac) <br/>
    - cx_freeze (recommended for Linux) <br/>
    - nuitka (experimental)
</p>
<p>supported python versions: </p>
<p> - 3.10 3.11, 3.12 <br/>
</p>

```
python3 build.py --build BUILD_OPTION --copy_backend
```

# Colab Notebook
 <a href="https://github.com/tntwise/REAL-Video-Enhancer-Colab">Colab Notebook</a>

# Credits:
### People:
| Person | For | Link |
|--|--|--|
| NevermindNilas | Some backend and reference code and working with me on many projects | https://github.com/NevermindNilas/ 
| Styler00dollar | RIFE ncnn models (4.1-4.5, 4.7-4.12-lite), Sudo Shuffle Span, and Scene Detect Models | https://github.com/styler00dollar 
| HolyWu | TensorRT engine generation code, inference optimizations, and RIFE jagged lines fixes | https://github.com/HolyWu/ 
| Rick Astley | Amazing music | https://www.youtube.com/watch?v=dQw4w9WgXcQ 

### Software: 
| Software Used | For | Link|
|--|--|--|
| FFmpeg | Multimedia framework for handling video, audio, and other media files | https://ffmpeg.org/ 
| QT | GUI framework | https://qt.io/
| FFMpeg Builds | Pre-compiled builds of FFMpeg. | Windows/Linux:  https://github.com/BtbN/FFmpeg-Builds, MacOS: https://github.com/eko5624/mpv-mac
| PyTorch | Neural Network Inference (CUDA/ROCm/TensorRT) | https://pytorch.org/ 
| NCNN | Neural Network Inference (Vulkan) | https://github.com/tencent/ncnn 
| RIFE | Real-Time Intermediate Flow Estimation for Video Frame Interpolation | https://github.com/hzwer/Practical-RIFE 
| rife-ncnn-vulkan | Video frame interpolation implementation using NCNN and Vulkan | https://github.com/nihui/rife-ncnn-vulkan 
| rife ncnn vulkan python | Python bindings for RIFE NCNN Vulkan implementation | https://github.com/media2x/rife-ncnn-vulkan-python 
| GMFSS | GMFlow based Anime VFI | https://github.com/98mxr/GMFSS_Fortuna
| GIMM | Motion Modeling Realistic VFI | https://github.com/GSeanCDAT/GIMM-VFI 
| ncnn python | Python bindings for NCNN Vulkan framework | https://pypi.org/project/ncnn 
| Real-ESRGAN | Upscaling | https://github.com/xinntao/Real-ESRGAN 
| SPAN | Upscaling | https://github.com/hongyuanyu/SPAN 
| Spandrel | CUDA upscaling model architecture support | https://github.com/chaiNNer-org/spandrel 
| ChaiNNer | Model Scale Detection | https://github.com/chaiNNer-org/chainner
| cx_Freeze | Tool for creating standalone executables from Python scripts (Linux build) | https://github.com/marcelotduarte/cx_Freeze 
| PyInstaller | Tool for creating standalone executables from Python scripts (Windows/Mac builds) | https://github.com/pyinstaller/pyinstaller
| Feather Icons | Open source icons library | https://github.com/feathericons/feather 
| PySceneDetect | Transition detection library for python | https://github.com/Breakthrough/PySceneDetect/
| Python Standalone Builds | Backend inference using portable python, helps when porting to different platforms. | https://github.com/indygreg/python-build-standalone |


# Star History
[![Star History Chart](https://api.star-history.com/svg?repos=LacklusterOpsec/Lackluster-Video-Enhancer&type=Date)](https://star-history.com/#LacklusterOpsec/Lackluster-Video-Enhancer&Date)
