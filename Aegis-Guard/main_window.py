import tkinter as tk
from tkinter import ttk
from core.system_service import SystemService
from core.ai_core import AICore
from core.security_core import SecurityCore
from core.optimus_hybrid import OptimusHybrid
from core.logger import Logger

class MainWindow(tk.Tk):
    def __init__(self, system_service, optimus, ai_core, security, logger, config):
        super().__init__()
        self.system_service = system_service
        self.optimus = optimus
        self.ai_core = ai_core
        self.security = security
        self.logger = logger
        self.config = config

        self.title(f"{config['app']['name']} - v{config['app']['version']}")
        self.geometry("1000x700")
        self.configure(bg="#1E1E1E")

        # Sekmeli arayüz
        self.tab_control = ttk.Notebook(self)
        self.tab_cpu = ttk.Frame(self.tab_control)
        self.tab_ai = ttk.Frame(self.tab_control)
        self.tab_log = ttk.Frame(self.tab_control)
        self.tab_security = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_cpu, text="CPU/RAM")
        self.tab_control.add(self.tab_ai, text="AI Öneriler")
        self.tab_control.add(self.tab_log, text="Loglar")
        self.tab_control.add(self.tab_security, text="Güvenlik")
        self.tab_control.pack(expand=1, fill="both")

        self._create_cpu_tab()
        self._create_ai_tab()
        self._create_log_tab()
        self._create_security_tab()
        self._update_loop()

    def _create_cpu_tab(self):
        self.cpu_label = tk.Label(self.tab_cpu, text="CPU: 0%", fg="#EAEAEA", bg="#1E1E1E", font=("Segoe UI", 14))
        self.cpu_label.pack(pady=10)
        self.ram_label = tk.Label(self.tab_cpu, text="RAM: 0%", fg="#EAEAEA", bg="#1E1E1E", font=("Segoe UI", 14))
        self.ram_label.pack(pady=10)

        self.cpu_bar = ttk.Progressbar(self.tab_cpu, length=500, maximum=100)
        self.cpu_bar.pack(pady=5)
        self.ram_bar = ttk.Progressbar(self.tab_cpu, length=500, maximum=100)
        self.ram_bar.pack(pady=5)

    def _create_ai_tab(self):
        self.ai_text = tk.Text(self.tab_ai, bg="#2D2D2D", fg="#00FF41", height=20, font=("Consolas", 11))
        self.ai_text.pack(fill="both", expand=True)

    def _create_log_tab(self):
        self.log_text = tk.Text(self.tab_log, bg="#2D2D2D", fg="#EAEAEA", height=20, font=("Consolas", 11))
        self.log_text.pack(fill="both", expand=True)

    def _create_security_tab(self):
        self.security_text = tk.Text(self.tab_security, bg="#2D2D2D", fg="#FF5555", height=20, font=("Consolas", 11))
        self.security_text.pack(fill="both", expand=True)

    def _update_loop(self):
        cpu = self.system_service.get_cpu_usage()
        ram = self.system_service.get_ram_usage()
        self.cpu_label.config(text=f"CPU: {cpu}%")
        self.ram_label.config(text=f"RAM: {ram}%")
        self.cpu_bar['value'] = cpu
        self.ram_bar['value'] = ram

        # AI Öneri
        suggestion = self.ai_core.get_suggestion(cpu, ram)
        self.ai_text.delete(1.0, tk.END)
        self.ai_text.insert(tk.END, suggestion)

        # Log
        self.logger.log(f"CPU: {cpu}%, RAM: {ram}%")
        logs = self.logger.get_logs()
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, "\n".join(logs[-10:]))

        # Güvenlik
        sec_status = self.security.monitor_processes()
        self.security_text.delete(1.0, tk.END)
        self.security_text.insert(tk.END, sec_status)

        self.after(1000, self._update_loop)
