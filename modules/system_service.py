import psutil

class SystemService:
    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=0.5)

    def get_ram_usage(self):
        return psutil.virtual_memory().percent
