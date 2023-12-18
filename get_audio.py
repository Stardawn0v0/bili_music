import requests


def get_audio_download_url(bvid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': f'https://www.bilibili.com/video/{bvid}',
        'Origin': 'https://www.bilibili.com'
    }


    try:
        # 获取视频cid
        video_res = requests.get(f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}', headers=headers).json()
        if video_res.get('code') != 0:
            print("获取视频信息失败")
            return None
        data = video_res.get('data')
        cid = data['pages'][0]['cid']

        # 获取音频文件url
        audio_res = requests.get(f"http://api.bilibili.com/x/player/playurl?fnval=16&bvid={bvid}&cid={cid}", headers=headers).json()

        audio_url = audio_res['data']['dash']['audio'][0]['baseUrl']

        return audio_url
    except Exception as e:
        print(f"下载错误：{e}")
        return None


if __name__ == '__main__':
    bvid = 'BV1F8411G7TJ'
    audio_url = get_audio_download_url(bvid)
    if audio_url:
        print(f"音频下载链接：{audio_url}")
