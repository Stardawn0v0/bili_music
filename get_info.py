import re
import requests


# 解析视频链接获取BV号
def url2bv(url):
    match = re.search(r'bilibili\.com/video/(BV[a-zA-Z0-9]+)', url)
    if match:
        return match.group(1)
    return None

def get_video_info(bv):
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': f'https://www.bilibili.com/video/{bv}',
        'Origin': 'https://www.bilibili.com'
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    if data["code"] == 0:
        video_data = data["data"]
        title = video_data["title"]
        author = video_data["owner"]["name"]
        picture = video_data["pic"]

        return title, author, picture
    else:
        return None

def title2musicTitle(title):
    if '《' in title and '》' in title:
        title = re.findall('《(.*?)》', title, re.S)[0]
        return title

    return False

if __name__ == '__main__':
    bv = url2bv("https://www.bilibili.com/bangumi/play/ep718308")
    title, author, pic = get_video_info(bv)
    print(f"""
Title: {title2musicTitle(title)}
Author: {author}
Picture: {pic}
""")
