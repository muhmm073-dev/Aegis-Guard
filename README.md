# 🛡️ Aegis Guard v7.0 – Büyük Güçlü Sürüm

**Aegis Guard**, sisteminizi güvenli, hızlı ve kullanıcı dostu hale getirmek için geliştirilmiş profesyonel bir güvenlik ve optimizasyon yazılımıdır.  
Bu sürüm, **güvenlik + optimizasyon + kişisel asistan** özelliklerini tek bir pakette sunar.  

---

## 🚀 Yeni Özellikler (v7.0)

### 🔒 Güvenlik Motoru 2.0
- Gerçek zamanlı dosya taraması (watchdog ile sürekli izleme)  
- Hash kontrolü (SHA256 / MD5) ile zararlı dosya tespiti  
- Ağ bağlantılarını izleme (şüpheli IP ve port tespiti)  
- Şüpheli işlemleri karantinaya alma  
- AES-256 ile şifrelenmiş log sistemi  
- Yönetici modunda parola koruması  

### 🎮 Optimus 2.0 (Oyun Performans Modu)
- RAM ve CPU önbellek temizleme  
- Oyun sürecine yüksek öncelik atama  
- Gerçek FPS ölçümü ve canlı izleme  
- CPU, GPU, RAM grafik gösterimi  
- Oyun profilleri kaydedebilme  

### 🌌 Aryus 2.0 (Rahatlama Modu)
- Playlist desteği (çoklu mp3 dosyası oynatma)  
- Doğa sesleri (yağmur, rüzgar, orman)  
- Zamanlayıcı (30 dk sonra otomatik kapanma)  
- Ses seviyesi kontrolü  
- En son çalınan müzik & ses seviyesini hatırlama  

### 🌍 Dil Desteği
- 10+ dil (TR, EN, RU, ES, FR, DE, IT, PT, JP, ZH)  
- UI üzerinden anında dil değiştirme  
- Topluluk tarafından kolay çeviri ekleme  

### 🛡️ Veri Güvenliği
- AES-256 şifreleme ile güvenli log ve ayar dosyaları  
- PIN / parola korumalı uygulama açılışı  
- Anti-Tamper sistemi (dosya hash doğrulama)  
- Otomatik yedekleme ve sıkıştırma (AES destekli ZIP)  
- Dosya hareketlerinde veri sızıntısı engelleme  

### 🖥️ Yeni Arayüz
- Modern tasarım (customtkinter + ttkbootstrap)  
- Dark / Light mod  
- Performans grafikleri (CPU, RAM, FPS canlı izleme)  
- Sekmeli yapı: Güvenlik, Optimus, Aryus, Loglar, Ayarlar  
- Gelişmiş log arama & filtreleme  

---

## 📊 Teknoloji Yığını
- **psutil** → Sistem & ağ izleme  
- **watchdog** → Dosya olayları takibi  
- **cryptography** → AES-256 şifreleme  
- **gettext** → Çoklu dil desteği  
- **pydub + simpleaudio** → Aryus müzik sistemi  
- **matplotlib** → Canlı performans grafikleri  
- **customtkinter** → Modern UI  

---

## ⚡ Kurulum
```bash
git clone https://github.com/kullanici/Aegis-Guard.git
cd Aegis-Guard
pip install -r requirements.txt
python main.py
## Kurulum
1. Python 3.10+ kurulu olmalı.
2. Paketleri kur:
```bash
pip install pyinstaller playsound pillow psutil

- name: Install dependencies
  run: pip install -r path/to/your/requirements.txt