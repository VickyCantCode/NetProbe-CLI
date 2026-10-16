# NetProbe

A simple, fast python script to discover active devices and open ports on your local ethernet / wi-fi network. Zero pip dependencies needed.

## Why I made this

Honestly speaking, whenever i connect my phone, laptop or raspberry pi to the home wifi, i always struggle to find what local ip address it got assigned. Opening router admin page every time is pure headache, and tools like nmap are too heavy with so many complex flags that i always forget.

So i just thought of writing this small python utility for myself only. It quickly pings the subnet using raw sockets to trigger the arp cache in few milliseconds, reads active devices, and checks common listening ports like ssh, http, and mysql.

## Features

- Zero third-party packages needed.
- Fast multithreaded scanning, finishes in less than a second on normal home LANs.
- Lists out IP addresses, MAC addresses, device hostnames, and detects listening open ports.
- Works straightforwardly on Windows and Linux both.

## How to run it

Just clone the repository and run it with python:

```bash
git clone https://github.com/VickyCantCode/netprobe.git
cd netprobe
py netprobe.py
```

(On Linux / Mac you can use `python3 netprobe.py`)

## Sample Output

```text
================================================================
  NETPROBE v1.0 - Local Network & Port Discovery
  Subnet: 192.168.1.0/24 | Host IP: 192.168.1.14
  Made with ♥ by Vicky.
================================================================

Scanning Ethernet and Wi-Fi devices...

Discovered 3 active device(s):

[1] 192.168.1.1     [70-4F-57-B2-11-AA] (Gateway) - router.home
    Open Ports: 53/DNS, 80/HTTP, 443/HTTPS

[2] 192.168.1.14    [LOCAL-HOST] (This PC)
    Open Ports: 4321/PORTFOLIO

[3] 192.168.1.38    [3C-22-FB-D4-88-12] - smart-tv.local
    Open Ports: 8008/HTTP-ALT, 8009/HTTP-ALT

Scan finished in 0.42s.
Made with ♥ by Vicky.
```

If you find any bugs or have suggestions, feel free to open an issue or pull request!
