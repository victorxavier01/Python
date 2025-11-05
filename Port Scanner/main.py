import socket

def scan(targets, ports):
    print(f"\n Scanning {str(targets)}")
    for port in range(1, ports):
        scan_port(targets, port)

def scan_port(ipaddress, port):
    try:
        sock = socket.socket
        sock.connect((ipaddress, port)) #2 pam: ipaddress and port
        print(f"[+]Port {str(port)} Opened")
        sock.close()
    except:
        pass

targets = input("[*] Enter Targets To Scan: ")
ports = int(input("[*] Enter How Many Ports You Want To Scan: "))
if ',' in targets:
    print(("[*] Scanning Multiple Targets"))
    for ip_addr in targets.split(','):
        scan(ip_addr.strip(' '), ports)
else:
    scan(targets, ports)
