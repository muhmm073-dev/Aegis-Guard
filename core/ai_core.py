#======================================================================
# AI Çekirdeği - v3.0
#======================================================================

class AICore:
    def __init__(self):
        self.history = []

    def get_suggestion(self, cpu, ram):
        suggestion = ""
        if cpu > 80:
            suggestion += "⚠ CPU kullanımı yüksek! Gereksiz uygulamaları kapatın.\n"
        elif cpu > 50:
            suggestion += "CPU kullanımınız orta seviyede.\n"
        else:
            suggestion += "CPU kullanımı normal.\n"

        if ram > 80:
            suggestion += "⚠ RAM kullanımı yüksek! Bellek temizleme önerilir.\n"
        elif ram > 50:
            suggestion += "RAM kullanımınız orta seviyede.\n"
        else:
            suggestion += "RAM kullanımı normal.\n"

        self.history.append({'cpu': cpu, 'ram': ram, 'suggestion': suggestion})
        return suggestion
