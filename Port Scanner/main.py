import socket

def scan(targets, ports):
    print(f"\n Scanning {str(targets)}")
    for port in range(1, ports+1):
        scan_port(targets, port)

def scan_port(ipaddress, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.6)
        result = sock.connect_ex((ipaddress, port))
        if result == 0:
            print(f"[+] Port {port} Opened")
        sock.close()
    except Exception:
        pass

targets = input("[*] Enter Targets To Scan: ")
ports = int(input("[*] Enter How Many Ports You Want To Scan: "))
if ',' in targets:
    print(("[*] Scanning Multiple Targets"))
    for ip_addr in targets.split(','):
        scan(ip_addr.strip(' '), ports)
else:
    scan(targets, ports)
