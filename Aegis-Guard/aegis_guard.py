#======================================================================
# AEGIS GUARD v66 PRO
#======================================================================
import tkinter as tk
from tkinter import ttk, font, messagebox
import psutil
import threading
import time
import yaml
import os

#======================================================================
# THEME
#======================================================================
class Theme:
    BG_PRIMARY = "#1E1E1E"
    BG_SECONDARY = "#2D2D2D"
    TEXT_PRIMARY = "#EAEAEA"
    ACCENT_PRIMARY = "#00BFFF"
    DANGER_COLOR = "#FF4500"
    FONT_DEFAULT = ("Segoe UI", 10)
    FONT_BOLD = ("Segoe UI", 10, "bold")
    FONT_LARGE = ("Segoe UI", 14)
    FONT_XLARGE = ("Segoe UI", 20, "bold")

#======================================================================
# SYSTEM SERVICE (CPU/RAM MONITOR)
#======================================================================
class SystemService:
    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=0.5)

    def get_ram_usage(self):
        return psutil.virtual_memory().percent

#======================================================================
# MAIN WINDOW
#======================================================================
class MainWindow(tk.Tk):
    def __init__(self, config):
        super().__init__()
        self.config_data = config
        self.title(f"{config.get('app', {}).get('name','Aegis Guard')} v66 PRO")
        self.geometry("900x700")
        self.configure(bg=Theme.BG_PRIMARY)
        self.system_service = SystemService()
        self._setup_ui()
        self.update_stats_loop()

    def _setup_ui(self):
        self.cpu_var = tk.StringVar(value="CPU: 0%")
        self.ram_var = tk.StringVar(value="RAM: 0%")

        # CPU Label
        self.cpu_label = tk.Label(self, textvariable=self.cpu_var, font=Theme.FONT_LARGE, bg=Theme.BG_PRIMARY, fg=Theme.TEXT_PRIMARY)
        self.cpu_label.pack(pady=20)

        # RAM Label
        self.ram_label = tk.Label(self, textvariable=self.ram_var, font=Theme.FONT_LARGE, bg=Theme.BG_PRIMARY, fg=Theme.TEXT_PRIMARY)
        self.ram_label.pack(pady=20)

        # Log Panel
        self.log_text = tk.Text(self, height=15, bg=Theme.BG_SECONDARY, fg=Theme.TEXT_PRIMARY, font=Theme.FONT_DEFAULT)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def log(self, message):
        self.log_text.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.log_text.see(tk.END)

    def update_stats_loop(self):
        cpu = self.system_service.get_cpu_usage()
        ram = self.system_service.get_ram_usage()

        cpu_threshold = self.config_data.get('core_settings', {}).get('cpu_danger_threshold', 75)
        ram_threshold = self.config_data.get('core_settings', {}).get('ram_danger_threshold', 80)

        self.cpu_var.set(f"CPU: {cpu}%")
        self.ram_var.set(f"RAM: {ram}%")

        if cpu > cpu_threshold:
            self.cpu_label.config(fg=Theme.DANGER_COLOR)
            self.log("CPU usage high! Optimizasyon önerisi uygulanabilir.")
        else:
            self.cpu_label.config(fg=Theme.TEXT_PRIMARY)

        if ram > ram_threshold:
            self.ram_label.config(fg=Theme.DANGER_COLOR)
            self.log("RAM usage high! Gereksiz işlemler kapatılabilir.")
        else:
            self.ram_label.config(fg=Theme.TEXT_PRIMARY)

        # 1 saniyede bir güncelle
        self.after(1000, self.update_stats_loop)

#======================================================================
# APP START
#======================================================================
def load_config():
    try:
        with open("app.yml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"HATA: YAML okunamadı: {e}")
        return {}

if __name__ == "__main__":
    config = load_config()
    app = MainWindow(config)
    app.mainloop()
