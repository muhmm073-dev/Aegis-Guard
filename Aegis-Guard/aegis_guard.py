#======================================================================
# GEREKLİ KÜTÜPHANELER
#======================================================================
import tkinter as tk
from tkinter import ttk, messagebox
import threading, time, os
import psutil, yaml, json
from modules.logger import Logger
from modules.system_service import SystemService
from modules.optimus import OptimusHybrid
from modules.ai_core import AI_Core
from PIL import Image, ImageTk

#======================================================================
# TEMA VE FONLAR
#======================================================================
class Theme:
    BG_PRIMARY = "#1E1E1E"
    BG_SECONDARY = "#2D2D2D"
    BG_WIDGET = "#121212"
    TEXT_PRIMARY = "#EAEAEA"
    TEXT_SECONDARY = "#A9A9A9"
    ACCENT_PRIMARY = "#007ACC"
    ACCENT_SECONDARY = "#00FF41"
    DANGER_COLOR = "#FF5555"
    FONT_DEFAULT = ("Segoe UI", 10)
    FONT_BOLD = ("Segoe UI", 10, "bold")
    FONT_LARGE = ("Segoe UI", 14)
    FONT_XLARGE_BOLD = ("Segoe UI", 24, "bold")
    FONT_MONO = ("Consolas", 11)

#======================================================================
# ANA PENCERE
#======================================================================
class MainWindow(tk.Tk):
    def __init__(self, config, logger, system_service, optimus, ai_core):
        super().__init__()
        self.config = config
        self.logger = logger
        self.system_service = system_service
        self.optimus = optimus
        self.ai_core = ai_core

        # Pencere başlığı ve boyut
        app_cfg = config.get("app", {})
        title = app_cfg.get("name", "Aegis X")
        version = app_cfg.get("version", "1.0")
        self.title(f"{title} (v{version})")
        self.geometry("950x750")
        self.configure(bg=Theme.BG_PRIMARY)

        # CANLI DEĞERLER
        self.cpu_var = tk.StringVar()
        self.ram_var = tk.StringVar()

        # UI ELEMENTLERİ
        self._create_widgets()

        # CANLI GÜNCELLEME
        self.update_stats()

    def _create_widgets(self):
        # Başlık
        title_lbl = tk.Label(self, text="Aegis Guardian", fg=Theme.TEXT_PRIMARY,
                             bg=Theme.BG_PRIMARY, font=Theme.FONT_XLARGE_BOLD)
        title_lbl.pack(pady=20)

        # CPU/RAM göstergeleri
        cpu_frame = ttk.LabelFrame(self, text="Performans", style="TLabelframe")
        cpu_frame.pack(pady=10, fill="x", padx=20)

        self.cpu_label = tk.Label(cpu_frame, textvariable=self.cpu_var,
                                  fg=Theme.ACCENT_PRIMARY, bg=Theme.BG_WIDGET,
                                  font=Theme.FONT_LARGE)
        self.cpu_label.pack(pady=5, padx=10, fill="x")

        self.ram_label = tk.Label(cpu_frame, textvariable=self.ram_var,
                                  fg=Theme.ACCENT_SECONDARY, bg=Theme.BG_WIDGET,
                                  font=Theme.FONT_LARGE)
        self.ram_label.pack(pady=5, padx=10, fill="x")

        # Log ekranı
        log_frame = ttk.LabelFrame(self, text="Loglar", style="TLabelframe")
        log_frame.pack(pady=10, fill="both", expand=True, padx=20)
        self.log_text = tk.Text(log_frame, bg=Theme.BG_WIDGET, fg=Theme.TEXT_SECONDARY,
                                font=Theme.FONT_MONO, state="disabled")
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)

    def update_stats(self):
        try:
            cpu = self.system_service.get_cpu_usage()
            ram = self.system_service.get_ram_usage()
            self.cpu_var.set(f"CPU Kullanımı: {cpu}%")
            self.ram_var.set(f"RAM Kullanımı: {ram}%")

            # Kritik durum kontrolü
            if cpu > self.config.get("core_settings", {}).get("cpu_danger_threshold", 75):
                self.cpu_label.config(fg=Theme.DANGER_COLOR)
                self.logger.warning(f"CPU tehlike eşiğini geçti: {cpu}%")
            else:
                self.cpu_label.config(fg=Theme.ACCENT_PRIMARY)

        except Exception as e:
            self.logger.error(f"Performans güncelleme hatası: {e}")

        self.after(self.config.get("core_settings", {}).get("update_interval_ms", 1000),
                   self.update_stats)

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert("end", f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

#======================================================================
# PROGRAM GİRİŞ NOKTASI
#======================================================================
if __name__ == "__main__":
    # YAML ayar dosyası
    try:
        with open("app.yml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"app.yml yüklenemedi: {e}")
        config = {"app":{"name":"Aegis X","version":"1.0"}, "core_settings":{"cpu_danger_threshold":75, "update_interval_ms":1000}}

    # LOGER
    logger = Logger()

    # SERVİSLER
    system_service = SystemService()
    optimus = OptimusHybrid()
    ai_core = AI_Core()

    # ANA PENCERE
    app = MainWindow(config, logger, system_service, optimus, ai_core)
    app.mainloop()
