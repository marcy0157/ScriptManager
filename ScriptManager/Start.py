import platform
import subprocess
import sys

def main():
    current_os = platform.system()

    if current_os == 'Windows':
        # Esegui il main per Windows
        subprocess.run([sys.executable, "Main.py"])
    elif current_os in ['Linux', 'Darwin']:  # Darwin è per macOS
        # Esegui il main per Unix (Linux/macOS)
        subprocess.run([sys.executable, "MainUnix.py"])
    else:
        print(f"Errore: Sistema operativo {current_os} non supportato.")

if __name__ == "__main__":
    main()
