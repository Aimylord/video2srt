from faster_whisper import WhisperModel
import os,time

srt_language="zh"      #设置字幕语言zh,ja,en
model = WhisperModel("large-v3", device="cuda")  #设置语音识别模型，英文可以换其他模型

def get_video_files(directory=r"H:\temp"):
    # 定义常见视频文件扩展名
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv')
    video_files = []
    for root, dirs, files in os.walk(directory):   # 遍历指定目录及其子目录
        for file in files:
            if file.lower().endswith(video_extensions):   # 检查文件扩展名是否为视频文件
                video_files.append((root, file))  #返回文件路径和文件名
    return video_files

def read_srt(root,file):
    new_name = os.path.splitext(file)[0]+"_"+srt_language+".srt"
    srt_filename = os.path.join(root,new_name)
    if os.path.exists(srt_filename):       #判断字幕文件是否存在
        print(f"{new_name}字幕文件已存在")
        return
    read_start_time=time.time()
    file_path = os.path.join(root, file)
    segments, info = model.transcribe(file_path,
                                      beam_size=5,
                                      best_of=5,
                                      language=srt_language,
                                      vad_filter=True,
                                      vad_parameters=dict(min_silence_duration_ms=600),)
    
    # 生成 SRT 文件
    srt_content = []
    for i, segment in enumerate(segments, start=1):
        start_time = segment.start
        end_time = segment.end
        text = segment.text
        start_time_str = f"{int(start_time // 3600):02}:{int((start_time % 3600) // 60):02}:{int(start_time % 60):02},{int((start_time % 1) * 1000):03}"
        end_time_str = f"{int(end_time // 3600):02}:{int((end_time % 3600) // 60):02}:{int(end_time % 60):02},{int((end_time % 1) * 1000):03}"
        srt_content.append(f"{i}\n{start_time_str} --> {end_time_str}\n{text}\n")
    
    # 将 SRT 内容写入文件
    with open(srt_filename, "w", encoding="utf-8") as srt_file:
        srt_file.write("\n".join(srt_content))
    print(f"字幕{srt_filename}已生成，耗时{round((time.time()-read_start_time)/60,2)}分钟")
    count=count+1

if __name__=="__main__":
    count=0
    directory=os.path.dirname(os.path.abspath(__file__))
    vidiofils = get_video_files(directory)
    print(f"-----------------开始字幕生成-----------------------")
    for root,file in vidiofils:
        print(root, file)
        read_srt(root, file)
    print(f"-----------字幕生成结束，累计生成{count}个字幕-----------")
