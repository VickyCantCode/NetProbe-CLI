import socket
import subprocess
import re
import time
from concurrent.futures import ThreadPoolExecutor

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "TELNET", 53: "DNS", 80: "HTTP",
    139: "NETBIOS", 443: "HTTPS", 445: "SMB", 3000: "DEV",
    3306: "MYSQL", 4321: "PORTFOLIO", 5000: "FLASK", 8000: "HTTP-ALT",
    8080: "HTTP-PROXY", 8443: "HTTPS-ALT"
}

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()

def trigger_arp(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.06)
    try:
        s.connect_ex((ip, 445))
    except Exception:
        pass
    finally:
        s.close()

def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return ""

def scan_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.15)
    try:
        if s.connect_ex((ip, port)) == 0:
            return port
    except Exception:
        pass
    finally:
        s.close()
    return None

def scan_device_ports(ip):
    open_ports = []
    with ThreadPoolExecutor(max_workers=15) as ex:
        results = ex.map(lambda p: scan_port(ip, p), COMMON_PORTS.keys())
        for r in results:
            if r:
                open_ports.append(f"{r}/{COMMON_PORTS[r]}")
    return open_ports

def main():
    local_ip = get_local_ip()
    if local_ip == "127.0.0.1":
        print("No active network connection detected.")
        return

    subnet = ".".join(local_ip.split(".")[:3])
    print("=" * 64)
    print("  NETPROBE v1.0 - Local Network & Port Discovery")
    print(f"  Subnet: {subnet}.0/24 | Host IP: {local_ip}")
    print("  Made with ♥ by Vicky.")
    print("=" * 64)
    print("\nScanning Ethernet and Wi-Fi devices...")

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=100) as ex:
        ex.map(trigger_arp, [f"{subnet}.{i}" for i in range(1, 255)])

    arp_data = subprocess.check_output(["arp", "-a"], text=True)
    devices = {}

    for line in arp_data.splitlines():
        match = re.search(r"([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\s+([0-9a-fA-F-]+)\s+(\w+)", line)
        if match:
            ip, mac, kind = match.groups()
            if ip.startswith(subnet) and not ip.endswith(".255") and mac.lower() != "ff-ff-ff-ff-ff-ff":
                devices[ip] = mac.upper()

    devices[local_ip] = "LOCAL-HOST"

    sorted_ips = sorted(devices.keys(), key=lambda x: [int(p) for p in x.split(".")])
    print(f"\nDiscovered {len(sorted_ips)} active device(s):\n")

    for idx, ip in enumerate(sorted_ips, 1):
        mac = devices[ip]
        hostname = get_hostname(ip)
        tag = " (This PC)" if ip == local_ip else (" (Gateway)" if ip.endswith(".1") else "")
        host_info = f" - {hostname}" if hostname else ""
        print(f"[{idx}] {ip:<15} [{mac}]{tag}{host_info}")

        ports = scan_device_ports(ip)
        if ports:
            print(f"    Open Ports: {', '.join(ports)}")
        else:
            print("    Open Ports: None detected on common list")
        print()

    duration = time.time() - start_time
    print(f"Scan finished in {duration:.2f}s.")
    print("Made with ♥ by Vicky.\n")

if __name__ == "__main__":
    main()
