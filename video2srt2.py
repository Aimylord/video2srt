from faster_whisper import WhisperModel
import os
import time

# 设置字幕语言 (zh: 中文, ja: 日语, en: 英文)
SRT_LANGUAGE = "zh"

# 加载语音识别模型
MODEL = WhisperModel("large-v3", device="cuda")

def get_video_files(directory=r"H:\temp"):
    """
    获取指定目录及其子目录中的所有视频文件。
    :param directory: 要扫描的目录路径
    :return: 包含 (root, file) 的列表
    """
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv')
    video_files = []
    if not os.path.exists(directory):
        print(f"目录 {directory} 不存在")
        return video_files

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(video_extensions):
                video_files.append((root, file))
    return video_files


def read_srt(root, file):
    """
    为指定视频文件生成 SRT 字幕文件。
    :param root: 视频文件所在的目录
    :param file: 视频文件名
    """
    new_name = os.path.splitext(file)[0] + f"_{SRT_LANGUAGE}.srt"
    srt_filename = os.path.join(root, new_name)

    # 检查字幕文件是否已存在
    if os.path.exists(srt_filename):
        print(f"{new_name} 字幕文件已存在")
        return

    try:
        start_time = time.time()
        file_path = os.path.join(root, file)
        segments, info = MODEL.transcribe(
            file_path,
            beam_size=5,
            best_of=5,
            language=SRT_LANGUAGE,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=600),
        )

        # 构建 SRT 文件内容
        srt_content = []
        for i, segment in enumerate(segments, start=1):
            start_time_str = format_time(segment.start)
            end_time_str = format_time(segment.end)
            text = segment.text.strip()
            srt_content.append(f"{i}\n{start_time_str} --> {end_time_str}\n{text}\n")

        # 将 SRT 内容写入文件
        with open(srt_filename, "w", encoding="utf-8") as srt_file:
            srt_file.write("\n".join(srt_content))

        elapsed_time = round((time.time() - start_time) / 60, 2)
        print(f"字幕 {srt_filename} 已生成，耗时 {elapsed_time} 分钟")
        return True

    except Exception as e:
        print(f"处理文件 {file} 时出错: {e}")
        return False


def format_time(seconds):
    """
    将秒数转换为 SRT 时间格式。
    :param seconds: 秒数
    :return: 格式化的时间字符串 (HH:MM:SS,ms)
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"


if __name__ == "__main__":
    count = 0
    directory = os.path.dirname(os.path.abspath(__file__))
    video_files = get_video_files(directory)

    print("----------------- 开始字幕生成 -----------------------")
    for root, file in video_files:
        print(f"正在处理: {os.path.join(root, file)}")
        if read_srt(root, file):
            count += 1

    print(f"----------- 字幕生成结束，累计生成 {count} 个字幕 -----------")