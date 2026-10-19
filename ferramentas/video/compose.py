# Uso: python3 compose.py <videos.json> <pasta-png> <pasta-saida>
# Junta os PNGs com transição e a trilha original de music.py num MP4 vertical 1080x1920.
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); X = 0.35
js, png, out = sys.argv[1:4]; os.makedirs(out, exist_ok=True)
for p in json.load(open(js)):
    d = p["dur"]; n = len(d); total = sum(d) - X * (n - 1)
    assert n == len(p["slides"]), f"{p['slug']}: dur e slides com tamanhos diferentes"
    wav = os.path.join(out, p["slug"] + ".wav")
    subprocess.run(["python3", os.path.join(HERE, "music.py"), wav, f"{total:.3f}", str(p.get("n", 0) % 6)], check=True)
    cmd = ["ffmpeg", "-loglevel", "error", "-y"]
    for i, t in enumerate(d): cmd += ["-loop", "1", "-t", f"{t}", "-framerate", "30", "-i", os.path.join(png, f"{p['slug']}-{i}.png")]
    cmd += ["-i", wav]
    f = [f"[{i}:v]scale=1080:1920,setsar=1,format=yuv420p[s{i}]" for i in range(n)]
    prev, off = "[s0]", 0
    for i in range(1, n):
        off += d[i - 1] - X; f.append(f"{prev}[s{i}]xfade=transition=fade:duration={X}:offset={off:.3f}[x{i}]"); prev = f"[x{i}]"
    cmd += ["-filter_complex", ";".join(f), "-map", prev, "-map", f"{n}:a", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart",
            os.path.join(out, p["slug"] + ".mp4")]
    subprocess.run(cmd, check=True); os.remove(wav)
    print("ok", p["slug"], round(total, 1), "s", flush=True)
