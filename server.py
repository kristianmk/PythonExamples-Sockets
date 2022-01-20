# Written by K. M. Knausgård 2022-01
#
# Simple TCP sockets example.
#
# Python socket documentation: https://docs.python.org/3/library/socket.html

import socket


HOST = "127.0.0.1"  # localhost
PORT = 55556


def main():
    # Create socket for address family IPv4 (AF_INET), type stream (almost always TCP).
    # AF_INET, SOCK_STREAM means reliable, sequenced, two-way, connection-oriented, sequenced, byte streams.
    #
    # Alternative address families could be AF_INET6 for IPv6, AF_BTH for bluetooth and more..
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)

    # Return connection and client address.
    (conn, addr) = s.accept()

    with conn:
        while True:
            # Receive from client, buffer size 1024.
            data = conn.recv(1024)
            if not data: break  # Break out of loop if client stopped.

            client_data = data.decode()
            print(client_data)
            conn.sendall((client_data + " from server too!").encode())


if __name__ == '__main__':
    main()
    
