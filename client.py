"""Simple educational TCP client example matching server.py."""

import socket
import sys
from typing import Final

HOST: Final[str] = "127.0.0.1"
PORT: Final[int] = 55556
BUFFER_SIZE: Final[int] = 1024
MAX_MESSAGE_BYTES: Final[int] = 4096
REQUEST_TEXT: Final[str] = "Hello world"
RESPONSE_SUFFIX: Final[str] = " from server too!"
MAX_RESPONSE_BYTES: Final[int] = MAX_MESSAGE_BYTES + len(RESPONSE_SUFFIX.encode("utf-8"))


def receive_until_eof(sock: socket.socket, *, max_bytes: int) -> bytes:
    """Read from *sock* until the server closes the connection."""
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


def main() -> int:
    """Send one UTF-8 request and print the UTF-8 response."""
    try:
        request_bytes = REQUEST_TEXT.encode("utf-8")
        if not request_bytes:
            raise ValueError("REQUEST_TEXT must not be empty for this example protocol")
        if len(request_bytes) > MAX_MESSAGE_BYTES:
            raise ValueError(f"REQUEST_TEXT must be at most {MAX_MESSAGE_BYTES} UTF-8 bytes")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            print(f"Connecting to {HOST}:{PORT} ...")
            client_socket.connect((HOST, PORT))
            client_socket.sendall(request_bytes)
            client_socket.shutdown(socket.SHUT_WR)

            response_bytes = receive_until_eof(client_socket, max_bytes=MAX_RESPONSE_BYTES)
            if not response_bytes:
                raise RuntimeError("Server closed the connection without sending a response")

        response_text = response_bytes.decode("utf-8")
        print(f"Server replied: {response_text}")
        return 0
    except (OSError, UnicodeDecodeError, ValueError, RuntimeError) as exc:
        print(f"Client error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
