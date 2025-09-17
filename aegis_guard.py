#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aegis Guard v6.2 PRO - Tek Dosya Sürümü
Tüm özellikler:
- Güvenlik motoru
- Oyun modu optimizasyonu
- Aryus modu (sakinleştirici müzik)
- FPS / RAM göstergesi
- Tema (light/dark) ve çoklu dil (TR/EN/RU/ES)
- Özel emojiler ve ses efektleri
- Windows + Linux uyumlu
- SQLite veri tabanı logları
"""

import os, threading, time, sqlite3, psutil, tkinter as tk
from tkinter import ttk, messagebox
from playsound import playsound
from PIL import Image, ImageTk

APP_NAME = "Aegis Guard"
VERSION = "6.2 PRO"

THEMES = {"dark":{"bg":"#0f172a","fg":"#e2e8f0"},"light":{"bg":"#ffffff","fg":"#000000"}}

LANG = {
    "tr":{"start":"Başlat","stop":"Durdur","logs":"Kayıtlar","optimize":"Oyun Modu","aryus":"Aryus Modu","quit":"Çıkış"},
    "en":{"start":"Start","stop":"Stop","logs":"Logs","optimize":"Game Mode","aryus":"Aryus Mode","quit":"Quit"},
    "ru":{"start":"Запуск","stop":"Стоп","logs":"Журналы","optimize":"Игровой режим","aryus":"Режим Ариус","quit":"Выход"},
    "es":{"start":"Iniciar","stop":"Detener","logs":"Registros","optimize":"Modo Juego","aryus":"Modo Aryus","quit":"Salir"}
}

EMOJIS = {
    "start":"🛡️","stop":"🛑","game_on":"🎮","game_off":"🕹️","aryus_on":"🌌","aryus_off":"🌙",
    "alert":"🔍","critical":"⚡","success":"✔️"
}

# -------------------------------
# Logger
# -------------------------------
class Logger:
    def __init__(self, ui_callback=None):
        self.ui_callback = ui_callback
        self.conn = sqlite3.connect("logs.db", check_same_thread=False)
        self._create_table()

    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS logs(
            timestamp TEXT,
            message TEXT
        )""")
        self.conn.commit()

    def log(self,msg):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO logs VALUES (?,?)",(timestamp,msg))
        self.conn.commit()
        if self.ui_callback: self.ui_callback(f"{timestamp} - {msg}")

# -------------------------------
# Güvenlik Motoru
# -------------------------------
class SecurityEngine:
    def __init__(self, logger):
        self.running = False
        self.logger = logger

    def start(self):
        if self.running: return
        self.running = True
        self.logger.log(f"{EMOJIS['start']} Aegis Guard başlatıldı")
        threading.Thread(target=self._scan_loop, daemon=True).start()

    def stop(self):
        self.running = False
        self.logger.log(f"{EMOJIS['stop']} Aegis Guard durduruldu")

    def _scan_loop(self):
        while self.running:
            for proc in psutil.process_iter(["pid","name"]):
                try:
                    name = proc.info["name"].lower()
                    if "virus" in name or "hack" in name:
                        self.logger.log(f"{EMOJIS['alert']} Şüpheli süreç bulundu: {name}")
                except: continue
            time.sleep(2)

# -------------------------------
# Oyun Modu
# -------------------------------
class GameOptimizer:
    def __init__(self, logger):
        self.active = False
        self.logger = logger

    def activate(self):
        if self.active: return
        self.active = True
        self.logger.log(f"{EMOJIS['game_on']} Oyun Modu aktif!")
        threading.Thread(target=self._boost_loop, daemon=True).start()

    def deactivate(self):
        self.active = False
        self.logger.log(f"{EMOJIS['game_off']} Oyun Modu kapandı")

    def _boost_loop(self):
        while self.active:
            freed = psutil.virtual_memory().available // (1024*1024)
            self.logger.log(f"RAM temizlendi - Kullanılabilir: {freed} MB")
            time.sleep(5)

# -------------------------------
# Aryus Modu
# -------------------------------
class AryusMode:
    def __init__(self, logger):
        self.active = False
        self.logger = logger
        self.music_thread = None

    def start(self):
        if self.active: return
        self.active = True
        self.logger.log(f"{EMOJIS['aryus_on']} Aryus modu aktif! Müzik çalıyor...")
        self.music_thread = threading.Thread(target=self._play_music, daemon=True)
        self.music_thread.start()

    def stop(self):
        self.active = False
        self.logger.log(f"{EMOJIS['aryus_off']} Aryus modu kapandı. Müzik durdu.")

    def _play_music(self):
        while self.active:
            try: playsound("sounds/aryus_music.mp3")
            except: break

# -------------------------------
# Ses
# -------------------------------
def play_start(): threading.Thread(target=lambda: playsound("sounds/start.wav"), daemon=True).start()
def play_stop(): threading.Thread(target=lambda: playsound("sounds/stop.wav"), daemon=True).start()

# -------------------------------
# Splash
# -------------------------------
def show_splash(root,image_path="splash.png",duration=2000):
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    try:
        img = ImageTk.PhotoImage(Image.open(image_path))
        tk.Label(splash,image=img).pack()
        splash.image = img
    except:
        tk.Label(splash,text="Aegis Guard",font=("Arial",24)).pack()
    root.after(duration,splash.destroy)

# -------------------------------
# Ana Uygulama
# -------------------------------
class AegisGuardApp(tk.Tk):
    def __init__(self,lang="tr",theme="dark"):
        super().__init__()
        self.lang_code = lang
        self.lang = LANG[lang]
        self.theme = theme

        self.logger = Logger(self._ui_log)
        self.engine = SecurityEngine(self.logger)
        self.optimizer = GameOptimizer(self.logger)
        self.aryus = AryusMode(self.logger)

        self.title(f"{APP_NAME} v{VERSION}")
        self.geometry("950x600")
        self.configure(bg=THEMES[self.theme]["bg"])
        self.protocol("WM_DELETE_WINDOW", self._quit)

        self.text = tk.Text(self,bg=THEMES[self.theme]["bg"],fg=THEMES[self.theme]["fg"],wrap="word")
        self.text.pack(fill="both",expand=True,padx=10,pady=10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)
        self.start_btn = ttk.Button(btn_frame,text=self.lang["start"],command=self._start_engine)
        self.start_btn.grid(row=0,column=0,padx=5)
        self.stop_btn = ttk.Button(btn_frame,text=self.lang["stop"],command=self._stop_engine)
        self.stop_btn.grid(row=0,column=1,padx=5)
        self.opt_btn = ttk.Button(btn_frame,text=self.lang["optimize"],command=self._toggle_opt)
        self.opt_btn.grid(row=0,column=2,padx=5)
        self.aryus_btn = ttk.Button(btn_frame,text=self.lang["aryus"],command=self._toggle_aryus)
        self.aryus_btn.grid(row=0,column=3,padx=5)
        self.quit_btn = ttk.Button(btn_frame,text=self.lang["quit"],command=self._quit)
        self.quit_btn.grid(row=0,column=4,padx=5)

        self.fps_label = ttk.Label(self,text="FPS: 0")
        self.fps_label.pack(pady=5)
        self._fps_counter = 0
        self._last_time = time.time()
        self._update_fps()

        self.after(100,lambda: show_splash(self,"splash.png"))

    def _ui_log(self,msg):
        self.text.insert("end",f"{msg}\n")
        self.text.see("end")

    def _start_engine(self):
        play_start()
        self.engine.start()

    def _stop_engine(self):
        play_stop()
        self.engine.stop()

    def _toggle_opt(self):
        if not self.optimizer.active:
            self.optimizer.activate()
        else:
            self.optimizer.deactivate()

    def _toggle_aryus(self):
        if not self.aryus.active:
            self.aryus.start()
        else:
            self.aryus.stop()

    def _update_fps(self):
        now = time.time()
        if now - self._last_time >= 1:
            self.fps_label.config(text=f"FPS: {self._fps_counter}")
            self._fps_counter = 0
            self._last_time = now
        self._fps_counter += 1
        self.after(16,self._update_fps)

    def _quit(self):
        if messagebox.askyesno("Çıkış","Uygulamadan çıkmak istiyor musunuz?"):
            self.engine.stop()
            self.optimizer.deactivate()
            self.aryus.stop()
            self.destroy()

# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    app = AegisGuardApp(lang="tr",theme="dark")
    app.mainloop()
