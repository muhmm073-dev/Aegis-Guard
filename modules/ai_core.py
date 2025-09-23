class AI_Core:
    def __init__(self):
        self.active = True

    def analyze(self, cpu, ram):
        # Basit öneri sistemi
        if cpu > 75:
            return "CPU kullanımı yüksek, bazı uygulamaları kapatabilirsiniz."
        if ram > 80:
            return "RAM kullanımı yüksek, bellek temizleyin."
        return "Sistem normal."
