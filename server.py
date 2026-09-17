"""Simple educational TCP server example.

The protocol is intentionally small: one UTF-8 request per connection and one UTF-8
response. Because TCP is a byte stream, the server reads until the client closes its
writing side instead of assuming a single recv() call is a complete message.
"""

from __future__ import annotations

import socket
import sys
from typing import Final

HOST: Final[str] = "127.0.0.1"
PORT: Final[int] = 55556
BUFFER_SIZE: Final[int] = 1024
MAX_MESSAGE_BYTES: Final[int] = 4096
RESPONSE_SUFFIX: Final[str] = " from server too!"


def receive_until_eof(sock: socket.socket, *, max_bytes: int) -> bytes:
    """Read from *sock* until the peer finishes sending data."""
    chunks: list[bytes] = []
    total_bytes = 0

    while True:
        chunk = sock.recv(BUFFER_SIZE)
        if not chunk:
            return b"".join(chunks)

        total_bytes += len(chunk)
        if total_bytes > max_bytes:
            raise ValueError(f"message exceeded {max_bytes} bytes")

        chunks.append(chunk)


def handle_client(conn: socket.socket, addr: tuple[str, int]) -> None:
    """Receive one request from a client and send one response."""
    print(f"Accepted connection from {addr[0]}:{addr[1]}")

    try:
        request_bytes = receive_until_eof(conn, max_bytes=MAX_MESSAGE_BYTES)
        if not request_bytes:
            print("Client closed the connection without sending a request.")
            return

        request_text = request_bytes.decode("utf-8")
        print(f"Received {len(request_bytes)} bytes: {request_text!r}")

        response_text = f"{request_text}{RESPONSE_SUFFIX}"
        conn.sendall(response_text.encode("utf-8"))
        print(f"Sent response: {response_text!r}")
    except UnicodeDecodeError as exc:
        print(f"Received invalid UTF-8 data from {addr[0]}:{addr[1]}: {exc}", file=sys.stderr)
    except ValueError as exc:
        print(f"Protocol error from {addr[0]}:{addr[1]}: {exc}", file=sys.stderr)
    except OSError as exc:
        print(f"Socket error while handling {addr[0]}:{addr[1]}: {exc}", file=sys.stderr)


def main() -> int:
    """Start the TCP server and handle clients until interrupted."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((HOST, PORT))
            server_socket.listen()
            print(f"Listening on {HOST}:{PORT}. Press Ctrl+C to stop.")

            while True:
                try:
                    conn, addr = server_socket.accept()
                except InterruptedError:
                    continue

                with conn:
                    handle_client(conn, addr)
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
        return 0
    except OSError as exc:
        print(f"Failed to start or run the server on {HOST}:{PORT}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
