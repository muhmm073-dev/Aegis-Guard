#Aegis Guard – Gelişmiş ve Güncel

## Yenilikler (v2.1.0)
- Otomatik versiyon takibi
- Zengin analiz: Ortalama, medyan, maksimum, minimum, toplam
- Otomatik grafik üretimi
- Web arayüzü: dosya yükle, analiz et, grafik ve JSON/PDF indir
- PDF raporu oluşturma
- Gelişmiş testler
- Kolay kurulum: `setup.sh` ile tek komut
- Bağımlılık dosyası: `requirements.txt`

## Hızlı Kurulum

1. Depoyu klonla:
   ```bash
   git clone https://github.com/muhmm073-dev/Uglam.git
   cd Uglam
   ```

2. Tek komutla kurulum ve başlatma:
   ```bash
   bash setup.sh
   ```

## Kullanım

- Web arayüzü ile analiz ve grafik:
  ```bash
  python src/web.py
  ```
  Sonra tarayıcıda `http://localhost:8080` adresine git!

- Komut satırı ile analiz:
  ```bash
  python src/analyze.py --input data/input.csv --output static/result.json
  ```

- Grafik oluşturmak için:
  ```bash
  python src/visualize.py --input data/input.csv --output static/plot.png
  ```

- PDF rapor almak için:
  ```bash
  python src/pdf_report.py --input_json static/result.json --output_pdf static/report.pdf
  ```

## Katkı ve Geliştirme

PR, Issue veya önerilerinizi bekliyoruz!
