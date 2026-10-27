import asyncio
import os
import edge_tts

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# (角色, voice, rate, pitch, 台词)
LINES = [
    ("旁白", "zh-CN-YunyangNeural", "-8%", "-2Hz",
     "民国二十六年，冬。雪落了一夜，把镇子压得很安静。"),
    ("掌柜", "zh-CN-YunjianNeural", "-12%", "-6Hz",
     "打烊了。住店，楼上左手第二间。"),
    ("女客", "zh-CN-XiaoxiaoNeural", "-6%", "+2Hz",
     "我们不是来住店的。"),
    ("掌柜", "zh-CN-YunjianNeural", "-12%", "-6Hz",
     "那你们，是来问事的。问事的人，得先押一样东西。"),
    ("年轻男人", "zh-CN-YunxiNeural", "-4%", "+0Hz",
     "押什么？"),
    ("掌柜", "zh-CN-YunjianNeural", "-14%", "-8Hz",
     "你们最舍不得的那件。"),
]


async def main():
    parts = []
    for i, (role, voice, rate, pitch, text) in enumerate(LINES):
        path = os.path.join(OUT_DIR, f"_line_{i:02d}.mp3")
        comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        await comm.save(path)
        size = os.path.getsize(path)
        print(f"{i} {role:6s} {voice:24s} {size:7d} bytes")
        parts.append(path)

    out = os.path.join(OUT_DIR, "试听_多角色.mp3")
    with open(out, "wb") as f:
        for p in parts:
            with open(p, "rb") as g:
                f.write(g.read())
    print("OUT", out, os.path.getsize(out), "bytes")


asyncio.run(main())
