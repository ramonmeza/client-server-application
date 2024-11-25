import argparse
import logging
import socketserver

from protocols import parse_protocol, parse_echo


class Server(socketserver.ThreadingTCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)


class ProtocolHandler(socketserver.StreamRequestHandler):
    def handle(self):
        logging.debug(f"handling request from client {self.client_address[0]}")

        data = self.request.recv(1024).strip()
        logging.debug(f"data received from client {self.client_address[0]}: {data}")

        try:
            protocol = parse_protocol(data)
            print(f"protocol: {protocol}")

            if protocol.header.message_id == 0x00:
                echo = parse_echo(protocol.data)

                self.request.sendall(echo.text.encode("utf-8"))

        except Exception as e:
            print("failed to parse message, ignoring")

        return super().handle()


def run_server(host: str, port: int) -> None:
    addr = (host, port)
    with Server(addr, ProtocolHandler) as server:
        print("Server starting on {}:{}".format(*server.server_address))
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("Server closing")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host",
        action="store",
        type=str,
        default="127.0.0.1",
        required=False,
        help="Address for the server.",
    )
    parser.add_argument(
        "--port",
        "-p",
        action="store",
        type=int,
        required=True,
        help="Port for the server.",
    )
    args = parser.parse_args()

    run_server(args.host, args.port)
