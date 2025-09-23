#======================================================================
# Aegis-Guard v1.2.0 - Profesyonel Sürüm
#======================================================================
import tkinter as tk
from tkinter import ttk, messagebox
import psutil, threading, time, yaml, os
import random

#======================================================================
# Tema ve Arayüz Ayarları
#======================================================================
class Theme:
    BG_PRIMARY = "#1B1B2F"
    BG_SECONDARY = "#162447"
    TEXT_PRIMARY = "#EAEAEA"
    ACCENT = "#E94560"
    FONT_DEFAULT = ("Segoe UI", 10)
    FONT_LARGE = ("Segoe UI", 14, "bold")

#======================================================================
# Sistem Servisi
#======================================================================
class SystemService:
    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=0.5)
    
    def get_ram_usage(self):
        return psutil.virtual_memory().percent

#======================================================================
# AI & Optimus Çekirdeği
#======================================================================
class OptimusAI:
    def __init__(self):
        self.cpu_history, self.ram_history = [], []

    def predict_cpu(self, cpu_val):
        self.cpu_history.append(cpu_val)
        if len(self.cpu_history) > 10: self.cpu_history.pop(0)
        return sum(self.cpu_history)/len(self.cpu_history)

    def predict_ram(self, ram_val):
        self.ram_history.append(ram_val)
        if len(self.ram_history) > 10: self.ram_history.pop(0)
        return sum(self.ram_history)/len(self.ram_history)

    def optimize_system(self):
        # Basit optimizasyon simülasyonu
        print("[OptimusAI] Sistemi optimize ediyor...")
        time.sleep(0.1)

#======================================================================
# Güvenlik Çekirdeği
#======================================================================
class SecurityCore:
    def monitor_system(self):
        # Örnek şüpheli süreç kontrolü
        suspicious = ["hacktool.exe", "keylogger.exe"]
        running = [p.name() for p in psutil.process_iter()]
        for proc in suspicious:
            if proc in running:
                print(f"[SecurityCore] Tehlike tespit edildi: {proc}")

#======================================================================
# Ana Pencere
#======================================================================
class MainWindow(tk.Tk):
    def __init__(self, config):
        super().__init__()
        self.config_data = config
        self.title(f"{config.get('app', {}).get('name','Aegis X')} v{config.get('app', {}).get('version','1.2.0')}")
        self.geometry("900x600")
        self.configure(bg=Theme.BG_PRIMARY)

        # Servis ve çekirdekler
        self.system = SystemService()
        self.ai = OptimusAI()
        self.security = SecurityCore()

        # Değişkenler
        self.cpu_var = tk.StringVar(value="CPU: 0%")
        self.ram_var = tk.StringVar(value="RAM: 0%")
        self.status_var = tk.StringVar(value="Sistem Durumu: Normal")

        # UI Oluştur
        self._create_widgets()

        # Arka plan threadleri
        threading.Thread(target=self._update_stats_loop, daemon=True).start()
        threading.Thread(target=self._security_monitor_loop, daemon=True).start()
        threading.Thread(target=self._ai_optimize_loop, daemon=True).start()

    def _create_widgets(self):
        ttk.Label(self, textvariable=self.cpu_var, font=Theme.FONT_LARGE, foreground=Theme.ACCENT, background=Theme.BG_PRIMARY).pack(pady=10)
        ttk.Label(self, textvariable=self.ram_var, font=Theme.FONT_LARGE, foreground=Theme.ACCENT, background=Theme.BG_PRIMARY).pack(pady=10)
        ttk.Label(self, textvariable=self.status_var, font=Theme.FONT_DEFAULT, foreground=Theme.TEXT_PRIMARY, background=Theme.BG_PRIMARY).pack(pady=10)

    def _update_stats_loop(self):
        while True:
            cpu = self.system.get_cpu_usage()
            ram = self.system.get_ram_usage()
            pred_cpu = self.ai.predict_cpu(cpu)
            pred_ram = self.ai.predict_ram(ram)
            self.cpu_var.set(f"CPU: {cpu:.1f}% | Tahmin: {pred_cpu:.1f}%")
            self.ram_var.set(f"RAM: {ram:.1f}% | Tahmin: {pred_ram:.1f}%")
            time.sleep(1)

    def _security_monitor_loop(self):
        while True:
            self.security.monitor_system()
            time.sleep(5)

    def _ai_optimize_loop(self):
        while True:
            self.ai.optimize_system()
            time.sleep(10)

#======================================================================
# Platform Başlatıcı
#======================================================================
class AegisPlatform:
    def __init__(self):
        try:
            with open("app.yml","r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f)
        except:
            self.config = {"app":{"name":"Aegis X","version":"1.2.0"}}
        self.main_window = MainWindow(self.config)

    def start(self):
        self.main_window.mainloop()

#======================================================================
# Program Girişi
#======================================================================
if __name__ == "__main__":
    platform = AegisPlatform()
    platform.start()
