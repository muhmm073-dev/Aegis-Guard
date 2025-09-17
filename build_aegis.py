#!/usr/bin/env python3
import platform, subprocess

MAIN_FILE = "neox45_v6.py"
ICON = "icon.ico"
SOUNDS = "sounds"
SPLASH = "splash.png"

def build_windows():
    cmd = [
        "pyinstaller", "--onefile", "--noconsole",
        f"--icon={ICON}",
        f"--add-data={SOUNDS};{SOUNDS}",
        f"--add-data={SPLASH};{SPLASH}",
        MAIN_FILE
    ]
    subprocess.run(cmd)
    print("✅ Windows EXE hazır -> dist/neox45_v6.exe")

def build_linux():
    cmd = [
        "pyinstaller", "--onefile",
        f"--add-data={SOUNDS}:{SOUNDS}",
        f"--add-data={SPLASH}:{SPLASH}",
        MAIN_FILE
    ]
    subprocess.run(cmd)
    print("✅ Linux çalıştırılabilir -> dist/neox45_v6")

if __name__ == "__main__":
    os_name = platform.system()
    if os_name == "Windows": build_windows()
    elif os_name == "Linux": build_linux()
    else: print(f"❌ Desteklenmeyen OS: {os_name}")
