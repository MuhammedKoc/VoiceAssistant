import tkinter as tk
import sounddevice as sd
import numpy as np
from PIL import Image,ImageTk
from src.utils.gifAnimator import *
from pathlib import Path


root = tk.Tk()

root.title("Kodex")
root.overrideredirect(True)
root.configure(bg='')
root.wm_attributes('-transparentcolor','black')
root.attributes('-topmost', True)
root.update()

root.geometry("100x100")

def entrySound():
    fs = 44100  # Örnekleme hızı
    duration_1 = 0.12  # İlk bas tonun süresi
    duration_2 = 0.38  # İkinci yükselen tonun süresi

    t1 = np.linspace(0, duration_1, int(fs * duration_1), endpoint=False)
    t2 = np.linspace(0, duration_2, int(fs * duration_2), endpoint=False)

    # 2. Tonların Tasarımı (Frekanslar düşürüldü - Daha tok)
    # Ton 1: 220 Hz (A3 - Derin bir bas uyarısı)
    wave1 = np.sin(2 * np.pi * 220 * t1)

    # Ton 2: 293 Hz'den (D4) 440 Hz'e (A4) yükselen premium dolgun ton
    f_start = 293
    f_end = 440
    phase2 = 2 * np.pi * (f_start * t2 + (f_end - f_start) * (t2**2) / (2 * duration_2))
    wave2 = np.sin(phase2)

    # 3. Yumuşatma Zarfları (Çıtlamayı önler, akustik hava katar)
    env1 = np.hanning(len(wave1))
    wave1_smoothed = wave1 * env1

    # İkinci ton için kuyruğu (fade-out) daha uzun tuttuk ki ses havada asılı kalsın
    env2 = np.ones_like(wave2)
    fade_in_len = int(fs * 0.02)
    fade_out_len = int(fs * 0.25) # Uzun sönümlenme
    env2[:fade_in_len] = np.linspace(0, 1, fade_in_len)
    env2[-fade_out_len:] = np.linspace(1, 0, fade_out_len)
    wave2_smoothed = wave2 * env2
    ai_startup_sound = np.concatenate([wave1_smoothed * 0.5, wave2_smoothed * 0.4])

    sd.play(ai_startup_sound, fs)



current_dir = Path(__file__).resolve().parent
gif_path = current_dir.parent / "resources" / "img" / "kodexIcon.gif"


gif_label = tk.Label(root, bg="black", bd=0, highlightthickness=0)
gif_label.pack(fill="both", expand=True)

gifPlayer = GifPlayer(root,gif_label, 80, 80)
gifPlayer.Play(gif_path, True,loopFrame=4)

entrySound()

root.mainloop()


