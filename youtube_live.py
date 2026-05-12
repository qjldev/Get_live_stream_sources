import yt_dlp

# 直播间列表
CHANNELS = [
{
        "name": "潜伏",
        "url": "https://www.youtube.com/watch?v=a-XpSWzP7JE"
    },
    {
        "name": "甄嬛传",
        "url": "https://www.youtube.com/watch?v=jZEVXDTpSlo"
    },
    {
        "name": "后宫甄嬛传",
        "url": "https://www.youtube.com/watch?v=HmxuvOSB0OI"
    },
    {
        "name": "雍正王朝",
        "url": "https://www.youtube.com/watch?v=0z4IHU4g-1M"
    },
    {
        "name": "父母爱情",
        "url": "https://www.youtube.com/watch?v=Hou7uVklRxA"
    },  
    {
        "name": "汉武大帝",
        "url": "https://www.youtube.com/watch?v=JQdMw93ouv4"
    },
    {
        "name": "西游记",
        "url": "https://www.youtube.com/watch?v=z7kKvkBeepQ"
    },
    {
        "name": "三国演义",
        "url": "https://www.youtube.com/watch?v=XNO0vjTNhzo"
    },
    {
        "name": "康熙王朝",
        "url": "https://www.youtube.com/watch?v=iT7RicpCeic"
    },
    {
        "name": "红楼梦",
        "url": "https://www.youtube.com/watch?v=kWeO1gdM0Cg"
    },
    {
        "name": "武林外传",
        "url": "https://www.youtube.com/watch?v=9e7p4F7myy8"
    },
    {
        "name": "包青天",
        "url": "https://www.youtube.com/watch?v=Qq-uMi_1Rzk"
    },
    {
        "name": "雍正王朝China Zone俱乐部",
        "url": "https://www.youtube.com/watch?v=DbNDCtzTzxQ"
    },
    {
        "name": "琅琊榜",
        "url": "https://www.youtube.com/watch?v=5VHcY5Unh7M"
    }
]


def get_best_stream(youtube_url):
    ydl_opts = {
        "quiet": True,
        "no_warnings": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)

            formats = info.get("formats", [])

            best_format = None
            best_height = 0

            for f in formats:
                # 只要 m3u8
                if f.get("protocol") != "m3u8_native":
                    continue

                height = f.get("height") or 0

                # 选最高画质
                if height > best_height:
                    best_height = height
                    best_format = f

            if best_format:
                return {
                    "url": best_format.get("url"),
                    "height": best_height,
                    "format": best_format.get("format_note")
                }

    except Exception as e:
        print(f"获取失败: {youtube_url}")
        print(e)

    return None


def generate_playlist():
    playlist = "#EXTM3U\n\n"

    for channel in CHANNELS:
        name = channel["name"]
        url = channel["url"]

        print(f"正在解析: {name}")

        result = get_best_stream(url)

        if result:
            stream_url = result["url"]
            quality = result["height"]

            print(f"成功: {name} ({quality}p)")

            playlist += f'#EXTINF:-1,{name}\n'
            playlist += f'{stream_url}\n\n'

        else:
            print(f"失败: {name}")

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)

    print("\n已生成 playlist.m3u")


generate_playlist()
