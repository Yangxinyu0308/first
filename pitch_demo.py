import os
import wave
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))

# (源文件, 音高系数)  >1 更尖更年轻, <1 更低沉更老
PLAN = [
    ("_sapi_00.wav", 1.00),  # 旁白
    ("_sapi_01.wav", 0.86),  # 掌柜
    ("_sapi_02.wav", 1.06),  # 女客
    ("_sapi_03.wav", 1.02),  # 掌柜
    ("_sapi_04.wav", 1.03),  # 年轻男人
    ("_sapi_05.wav", 0.84),  # 掌柜
]

def read_wav(path):
    with wave.open(path, "rb") as w:
        params = w.getparams()
        frames = w.readframes(w.getnframes())
    data = np.frombuffer(frames, dtype=np.int16).astype(np.float32)
    return data, params

def resample(data, factor):
    n = len(data)
    out_len = max(1, int(n / factor))
    idx = np.linspace(0, n - 1, out_len)
    return np.interp(idx, np.arange(n), data).astype(np.float32)

params = None
chunks = []
for name, factor in PLAN:
    data, p = read_wav(os.path.join(BASE, name))
    if params is None:
        params = p
    shifted = resample(data, factor)
    chunks.append(shifted)
    gap = np.zeros(int(params.framerate * 0.35), dtype=np.float32)
    chunks.append(gap)

out = np.concatenate(chunks)
out = np.clip(out, -32768, 32767).astype(np.int16)

dst = os.path.join(BASE, "试听_多角色.wav")
with wave.open(dst, "wb") as w:
    w.setnchannels(params.nchannels)
    w.setsampwidth(params.sampwidth)
    w.setframerate(params.framerate)
    w.writeframes(out.tobytes())

print("OUT", dst, os.path.getsize(dst), "bytes", round(len(out) / params.framerate, 1), "s")
