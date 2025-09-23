#======================================================================
# Aegis-Guard v3.0 - Ana Giriş Dosyası
#======================================================================

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import yaml
from core.system_service import SystemService
from core.optimus_hybrid import OptimusHybrid
from core.ai_core import AICore
from core.security_core import SecurityCore
from core.logger import Logger

#======================================================================
# Tema ve Stil
#======================================================================
class Theme:
    BG_PRIMARY = "#1E1E1E"
    BG_SECONDARY = "#2D2D2D"
    TEXT_PRIMARY = "#EAEAEA"
    ACCENT_PRIMARY = "#007ACC"
    FONT_DEFAULT = ("Segoe UI", 10)
    FONT_BOLD = ("Segoe UI", 10, "bold")

#======================================================================
# Ana Pencere
#======================================================================
class MainWindow(tk.Tk):
    def __init__(self, system_service, optimus, ai_core, security, config, logger):
        super().__init__()
        self.system_service = system_service
        self.optimus = optimus
        self.ai_core = ai_core
        self.security = security
        self.config = config
        self.logger = logger

        self.title(f"{self.config['app']['name']} - v{self.config['app']['version']}")
        self.geometry("950x700")
        self.configure(bg=Theme.BG_PRIMARY)

        self._create_widgets()
        self._update_loop()

    def _create_widgets(self):
        # CPU ve RAM göstergeleri
        self.cpu_label = ttk.Label(self, text="CPU: 0%", foreground=Theme.TEXT_PRIMARY, background=Theme.BG_PRIMARY)
        self.cpu_label.pack(pady=10)
        self.ram_label = ttk.Label(self, text="RAM: 0%", foreground=Theme.TEXT_PRIMARY, background=Theme.BG_PRIMARY)
        self.ram_label.pack(pady=10)

        # AI öneri paneli
        self.ai_panel = tk.Text(self, height=10, width=80, bg=Theme.BG_SECONDARY, fg=Theme.TEXT_PRIMARY)
        self.ai_panel.pack(pady=10)

        # Log paneli
        self.log_panel = tk.Text(self, height=10, width=80, bg=Theme.BG_SECONDARY, fg=Theme.TEXT_PRIMARY)
        self.log_panel.pack(pady=10)

    def _update_loop(self):
        cpu = self.system_service.get_cpu_usage()
        ram = self.system_service.get_ram_usage()
        self.cpu_label.config(text=f"CPU: {cpu}%")
        self.ram_label.config(text=f"RAM: {ram}%")

        # AI öneri güncelle
        suggestion = self.ai_core.get_suggestion(cpu, ram)
        self.ai_panel.delete(1.0, tk.END)
        self.ai_panel.insert(tk.END, suggestion)

        # Güvenlik ve log güncelle
        self.logger.log(f"CPU: {cpu}%, RAM: {ram}%")
        logs = self.logger.get_logs()
        self.log_panel.delete(1.0, tk.END)
        self.log_panel.insert(tk.END, "\n".join(logs[-10:]))

        # 1 saniye aralık ile güncelle
        self.after(1000, self._update_loop)

#======================================================================
# Program Başlatıcı
#======================================================================
class AegisXPlatform:
    def __init__(self):
        # Konfigürasyon yükleme
        with open("app.yml", "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        # Modüller
        self.logger = Logger()
        self.system_service = SystemService()
        self.optimus = OptimusHybrid(self.system_service)
        self.ai_core = AICore()
        self.security = SecurityCore()

        # Ana pencere
        self.main_window = MainWindow(
            self.system_service, self.optimus, self.ai_core, self.security, self.config, self.logger
        )

    def start(self):
        self.main_window.mainloop()

#======================================================================
# Programın Giriş Noktası
#======================================================================
if __name__ == "__main__":
    platform = AegisXPlatform()
    platform.start()
