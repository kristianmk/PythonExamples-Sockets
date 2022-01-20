# Written by K. M. Knausgård 2022-01
#
# Python socket documentation: https://docs.python.org/3/library/socket.html


import socket


HOST = "127.0.0.1"  # localhost
PORT = 55556


def main():
    # Create socket for address family IPv4 (AF_INET), type stream (almost always means TCP).
    # Alternative address families could be AF_INET6 for IPv6, AF_BTH for bluetooth and more..
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # Connect to server (block until accepted).
        s.connect((HOST, PORT))

        # Send encoded data.
        s.sendall(b"Hello world")

        # Receive response.
        data = s.recv(1024)

        # Print result.
        print(data.decode())


if __name__ == '__main__':
    main()

