#!/usr/bin/env python3
"""
Aegis Guard - basit CLI iskeleti
"""

from __future__ import annotations
import argparse
import logging
import sys
import time
from typing import Optional

try:
    import psutil
except Exception:  # psutil opsiyonel; hata varsa uyarı ver
    psutil = None

LOG = logging.getLogger("aegis_guard")

def setup_logging(level: int = logging.INFO) -> None:
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    LOG.addHandler(handler)
    LOG.setLevel(level)

def check_system(threshold: float = 80.0) -> dict:
    """Basit sistem kontrolü: CPU ve RAM kullanımı (psutil varsa)."""
    data = {"cpu": None, "ram": None}
    if psutil:
        data["cpu"] = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        data["ram"] = mem.percent
    else:
        LOG.warning("psutil bulunamadı; sistem verisi alınamıyor.")
    return data

def run_monitor(interval: float = 5.0, threshold: float = 80.0) -> None:
    LOG.info("Monitor başlatıldı (interval=%s threshold=%s)", interval, threshold)
    try:
        while True:
            data = check_system(threshold)
            if data["cpu"] is not None:
                LOG.info("CPU: %.1f%% | RAM: %.1f%%", data["cpu"], data["ram"])
                if data["cpu"] > threshold or data["ram"] > threshold:
                    LOG.warning("Sistem eşiğini aştı! (threshold=%s)", threshold)
            else:
                LOG.debug("Sistem verisi yok.")
            time.sleep(interval)
    except KeyboardInterrupt:
        LOG.info("Monitor durduruldu (CTRL+C).")

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="aegis_guard", description="Aegis Guard CLI")
    p.add_argument("--interval", "-i", type=float, default=5.0, help="Monitor aralığı (saniye)")
    p.add_argument("--threshold", "-t", type=float, default=80.0, help="Uyarı eşiği (%)")
    p.add_argument("--debug", action="store_true", help="Debug logging aç")
    p.add_argument("--once", action="store_true", help="Sadece bir kere çalıştır (test amaçlı)")
    return p

def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    setup_logging(logging.DEBUG if args.debug else logging.INFO)
    if args.once:
        data = check_system(args.threshold)
        if data["cpu"] is not None:
            LOG.info("Tek seferlik kontrol -> CPU: %.1f%% RAM: %.1f%%", data["cpu"], data["ram"])
        return 0
    run_monitor(interval=args.interval, threshold=args.threshold)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
