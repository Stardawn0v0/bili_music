import subprocess
import os
import sys
from get_info import *
from get_audio import *
import requests



bvid = url2bv(input("请输入视频链接："))
print("尝试获取视频信息...")
title, author, pic = get_video_info(bvid)
if title and author and pic:
    if title2musicTitle(title):
        title = title2musicTitle(title)
    else:
        title = input("无法从视频标题中获取音乐标题，请手动输入（无输入则使用视频标题）：")
        if not title:
            title = title
    print("获取成功！")
    print(f"""
标题: {title}
作者: {author}
封面: {pic}
""")
else:
    print("获取失败！")
    sys.exit(1)

print("尝试下载封面...")
try:
    with open(f"temp.jpg", 'wb') as f:
        f.write(requests.get(pic).content)
    print("下载成功！")
except Exception as e:
    print(f"下载失败：{e}")
    sys.exit(1)

print("尝试获取音频下载链接...")
audio_url = get_audio_download_url(bvid)
if audio_url:
    print(f"获取成功！\n音频下载链接：{audio_url}")
    print("尝试下载音频...")
    try:
        with open(f"temp.m4a", 'wb') as f:
            f.write(requests.get(audio_url).content)
        print("下载成功！")
    except Exception as e:
        print(f"下载失败：{e}")
        sys.exit(1)
else:
    print("获取失败！")
    sys.exit(1)

print("聚合已有资源...")
# 设置输出文件名，这里使用视频标题作为文件名，并去除非法字符
output_file_name = "".join(x for x in title if x.isalnum() or x in [" ", "-", "_"])
output_mp3 = f"{output_file_name}.mp3"

# FFmpeg命令行参数
ffmpeg_command = [
    'ffmpeg',
    '-i', 'temp.m4a',  # 输入文件
    '-i', 'temp.jpg',  # 封面图片
    '-map', '0:0',  # 映射音频流
    '-map', '1:0',  # 映射封面图片流
    '-metadata', f'title={title2musicTitle(title)}',  # 设置标题
    '-metadata', f'artist={author}',  # 设置作者
    '-id3v2_version', '3',  # 设置ID3标签版本
    '-codec:v', 'copy',  # 复制视频流（在这里是封面图片）
    '-y',
    output_mp3
]

print("开始转换音频...")
try:
    # 执行FFmpeg命令
    subprocess.run(ffmpeg_command, check=True)
    print("转换成功！")
except subprocess.CalledProcessError as e:
    print(f"转换失败：{e}")
    sys.exit(1)

# 清理临时文件
try:
    os.remove('temp.m4a')
    os.remove('temp.jpg')
    print("临时文件已清理。")
except OSError as e:
    print(f"清理临时文件时出错：{e}")

print(f"完成！已保存为：{output_mp3}")
