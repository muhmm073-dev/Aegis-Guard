#======================================================================
# Güvenlik Çekirdeği - v3.0
#======================================================================

import psutil

class SecurityCore:
    def __init__(self):
        self.alerts = []

    def monitor_processes(self):
        suspicious = []
        for proc in psutil.process_iter(['pid', 'name']):
            name = proc.info['name'].lower()
            if any(x in name for x in ['hack', 'cheat', 'malware']):
                suspicious.append(proc.info['name'])
        if suspicious:
            alert_msg = f"⚠ Şüpheli uygulamalar tespit edildi: {suspicious}"
            self.alerts.append(alert_msg)
            return alert_msg
        return "Sistem güvenli."
