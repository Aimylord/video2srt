# 视频字幕生成工具

## 功能介绍

本工具是一款基于 `faster-whisper` 的视频字幕生成器，能够自动为视频文件生成 SRT 格式的字幕文件。它支持多种语言（如中文、英文、日语等），并利用 GPU 加速进行高效的语音转文字处理。

主要功能包括：
- **批量处理**：扫描指定目录及其子目录中的视频文件。
- **多语言支持**：根据需求选择生成的字幕语言（如中文、英文、日语等）。
- **高性能**：使用 `WhisperModel` 模型和 GPU 加速，提升语音识别效率。
- **SRT 格式输出**：生成符合标准的 SRT 字幕文件，便于后续使用。

---

## 安装指南

### 1. 环境要求
- **Python 版本**：3.7 或更高版本。
- **CUDA 支持**（可选）：如果需要使用 GPU 加速，请确保安装了 CUDA 驱动和相关库。

### 2. 安装依赖
运行以下命令安装所需的 Python 包：

```bash
pip install faster-whisper
```

如果需要 GPU 加速，请确保已安装 `torch` 和 `cuda` 相关依赖：

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

> 注意：根据您的 CUDA 版本调整安装命令。

### 3. 下载模型
`faster-whisper` 提供多种预训练模型（如 `tiny`, `base`, `small`, `medium`, `large-v3`）。默认使用 `large-v3` 模型，您可以根据需求下载其他模型。

模型下载地址：[https://github.com/guillaumekln/faster-whisper](https://github.com/guillaumekln/faster-whisper)

---

## 使用说明

### 1. 修改配置参数
在代码中设置以下参数以满足您的需求：

```python
SRT_LANGUAGE = "zh"  # 设置字幕语言（如 "zh" 表示中文，"en" 表示英文）
MODEL = WhisperModel("large-v3", device="cuda")  # 设置语音识别模型和设备（如 "cuda" 或 "cpu"）
```

- **`SRT_LANGUAGE`**：目标字幕语言，支持的语言包括 `zh`（中文）、`en`（英文）、`ja`（日语）等。
- **`MODEL`**：指定使用的模型和运行设备（推荐使用 `cuda` 以加速处理）。

### 2. 设置视频目录
通过修改以下代码行，指定要扫描的视频文件目录：

```python
directory = r"H:\temp"  # 替换为您的视频文件目录
```

### 3. 运行脚本
保存代码后，在终端运行以下命令启动程序：

```bash
python your_script_name.py
```

程序将自动扫描指定目录中的视频文件，并生成对应的 SRT 字幕文件。

---

## 可调整参数

以下是一些可以调整的关键参数及其作用：

| 参数名 | 描述 | 默认值 |
|--------|------|--------|
| `SRT_LANGUAGE` | 字幕语言（如 "zh", "en", "ja"） | `"zh"` |
| `MODEL` | 使用的语音识别模型和设备（如 `large-v3`，`cuda`） | `WhisperModel("large-v3", device="cuda")` |
| `beam_size` | 搜索宽度（越大越准确，但速度较慢） | `5` |
| `best_of` | 最优候选数 | `5` |
| `vad_filter` | 是否启用语音活动检测（VAD） | `True` |
| `min_silence_duration_ms` | 最小静音间隔时间（毫秒） | `600` |

---

## 示例输出

假设目录中有以下视频文件：
- `example_video.mp4`
- `test_movie.avi`

运行程序后，将在同一目录下生成对应的 SRT 文件：
- `example_video_zh.srt`
- `test_movie_zh.srt`

程序还会输出类似以下的日志信息：

```
----------------- 开始字幕生成 -----------------------
正在处理: H:\temp\example_video.mp4
字幕 H:\temp\example_video_zh.srt 已生成，耗时 2.5 分钟
正在处理: H:\temp\test_movie.avi
字幕 H:\temp\test_movie_zh.srt 已生成，耗时 3.0 分钟
----------- 字幕生成结束，累计生成 2 个字幕 -----------
```

---

## 注意事项

1. **GPU 支持**：如果未启用 GPU 加速，处理速度可能会显著降低。
2. **视频格式**：目前支持常见的视频格式（如 `.mp4`, `.avi`, `.mov` 等）。对于不支持的格式，建议先转换为兼容格式。
3. **内存限制**：大型视频文件可能占用较多 GPU 内存，请确保设备有足够的资源。

---

如果您有任何问题或建议，请随时联系开发者！