import subprocess
import re
import platform
import time

def scan_wifi_networks():
    if platform.system() == "Darwin":
        # Command to scan Wi-Fi networks on macOS
        command = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s | awk 'NR>0{print substr($0, index($0, $1))}'"
        output = subprocess.check_output(command, shell=True)
        networks = output.decode('utf-8').strip().split('\n')
        return networks
    elif platform.system() == "Windows":
        # Command to scan Wi-Fi networks on Windows
        command = 'netsh wlan show networks mode=Bssid'
        output = subprocess.check_output(command, shell=True)
        networks = re.findall(r"SSID [0-9]+ : (.*)", output.decode('utf-8'))
        return networks
    elif platform.system() == "Linux":
        # Command to scan Wi-Fi networks on Linux (Ubuntu)
        command = 'nmcli -t -f ssid dev wifi list'
        output = subprocess.check_output(command, shell=True)
        networks = output.decode('utf-8').split('\n')
        networks = [network.split(':')[1] for network in networks if network != '']
        return networks

def check_connected_devices():
    if platform.system() == "Darwin":
        # Command to check connected devices on macOS
        command = "arp -a"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        devices = result.stdout.strip().split("\n")
        return devices
    elif platform.system() == "Windows":
        # Command to check connected devices on Windows
        command = 'arp -a'
        output = subprocess.check_output(command, shell=True)
        devices = re.findall(r"(([0-9a-fA-F]{2}-){5}[0-9a-fA-F]{2})", output.decode('utf-8'))
        return devices
    elif platform.system() == "Linux":
        # Command to check connected devices on Linux (Ubuntu)
        command = 'arp -a'
        output = subprocess.check_output(command, shell=True)
        devices = re.findall(r"(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})", output.decode('utf-8'))
        return devices

def run_wifi_guard():
    print("WiFi Guard is running...")
    
    while True:
        # Get scanned Wi-Fi networks
        networks = scan_wifi_networks()
        print("Detected Wi-Fi Networks:")
        for network in networks:
            print(network)
        
        print("\n----------------------------------")

        # Check connected devices
        devices = check_connected_devices()
        print("\nConnected Devices:")
        for device in devices:
            print(device)
        
        print("\n----------------------------------")

        # Countdown display
        for countdown in range(10, 0, -1):
            print(f"Next iteration in {countdown} seconds...", end="\r")
            time.sleep(1)
        print("Next iteration in 0 seconds!")

        print("\n----------------------------------")
