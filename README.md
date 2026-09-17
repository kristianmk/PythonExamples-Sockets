# PythonExamples-Sockets

A small, self-contained TCP sockets example for Python.

The code is intentionally simple enough for students to read in one sitting while still showing an important TCP detail: **TCP is a byte stream, not a message queue**. A single `send()` on one side does not guarantee that a single `recv()` on the other side contains the whole message.

Another Python implementation (C-style) lives here: <https://github.com/kristianmk/PythonExamples-SocketsCStyle>

## Prerequisites

- Python 3.9 or newer
- Two terminals on the same machine
- The default host/port (`127.0.0.1:55556`) must be free

## Files

- `server.py` - accepts TCP connections and replies once per connection
- `client.py` - connects to the server, sends one UTF-8 request, and prints the UTF-8 response

## Run the example

Open two terminals in the repository directory.

### Terminal 1: start the server

```bash
python server.py
```

Expected startup output:

```text
Listening on 127.0.0.1:55556. Press Ctrl+C to stop.
```

The server keeps running and can accept repeated client connections until you stop it with `Ctrl+C`.

### Terminal 2: run the client

```bash
python client.py
```

Expected client output:

```text
Connecting to 127.0.0.1:55556 ...
Server replied: Hello world from server too!
```

Expected server output after the client connects:

```text
Accepted connection from 127.0.0.1:<port>
Received 11 bytes: 'Hello world'
Sent response: 'Hello world from server too!'
```

You can run `python client.py` multiple times while the server stays open.

## Protocol notes

This example uses a deliberately small request/response protocol:

1. The client sends exactly one **non-empty UTF-8 request**.
2. The client then calls `shutdown(socket.SHUT_WR)` to say, "I am done sending request bytes on this connection."
3. The server reads until end-of-file instead of assuming one `recv()` call equals one complete message.
4. The server replies with the original text plus `" from server too!"` encoded as UTF-8.
5. The server closes the connection after sending the response, and the client reads until end-of-file.

To keep the example simple and explicit, the request is limited to 4096 bytes.

## Scope and limitations

- This is a localhost teaching example, not a production network service.
- It handles one client at a time.
- It does not use TLS, authentication, retries, timeouts, or structured message formats.
- For real applications, you would normally define a stronger framing protocol (for example a length prefix or newline-delimited messages) and consider security, validation, and network errors in more depth.
