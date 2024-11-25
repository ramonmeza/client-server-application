import cmd
import logging
import socket
import struct

# readline is available on Unix and provides bash-like history editing to cmd
try:
    import readline

    logging.info("readline module imported.")
except ImportError:
    logging.info("readline module not found.")


CLIENT_ADDR = ("127.0.0.1", 0)


class ClientShell(cmd.Cmd):
    intro = "\033[34mwelcome to the client's shell interface\033[0m"
    prompt = "\033[33m>\033[0m "
    use_rawinput = False

    # commands
    def do_echo(self, args: str):
        """
            \033[32mcommand:\033[0m  \033[36mecho\033[0m
        \033[32mdescription:\033[0m  have the server echo a given message
              \033[32musage:\033[0m  \033[36mecho\033[0m [server_ip] [server_port] [message]
            \033[32mexample:\033[0m  \033[36mecho\033[0m 127.0.0.1 5000 hello, world!
        """
        # split args
        try:
            args_split = args.split(" ")
            server_addr = str(args_split[0]), int(args_split[1])
            message = str(" ".join(args_split[2:]))
        except IndexError:
            logging.error(f"improper command arguments passed to echo command: {args}")
            print(
                "\033[31mcommand failed due to improper arguments, please try again\033[0m"
            )
            return

        with socket.socket() as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(CLIENT_ADDR)
            client_addr = sock.getsockname()

            logging.info(
                f"client {client_addr} to server {server_addr}: echo {message}"
            )
            try:
                # construct message
                # protocol(message_id, message_length, echo(length of text, text))
                msg = struct.pack(
                    f"!BIH{len(message)}s",
                    0x00,
                    (2 + len(message)),
                    len(message),
                    message.encode(),
                )

                sock.connect(server_addr)
                sock.sendall(msg)
                resp = sock.recv(1024)
                logging.info(
                    f"server {server_addr} to client {client_addr}: echoed {message}"
                )
                print(resp.decode())

            except TimeoutError:
                logging.error(f"failed to connect to server({server_addr})")
                print("\033[31mcommand failed, please try again\033[0m")

    def do_quit(self, args: str):
        """
            \033[32mcommand:\033[0m  \033[36mquit\033[0m
        \033[32mdescription:\033[0m  quit the client application
        """
        return True

    def do_exit(self, args: str):
        """
            \033[32mcommand:\033[0m  \033[36mexit\033[0m
        \033[32mdescription:\033[0m  exit the client application
        """
        return True

    def do_shell(self, args: str):
        "for advanced usage"
        command_scrubbed = args.lower().strip()
        if (
            command_scrubbed == "q"
            or command_scrubbed == "quit"
            or command_scrubbed == "exit"
        ):
            return True


def run_client() -> None:
    client = ClientShell()
    try:
        client.cmdloop()
    except KeyboardInterrupt:
        pass
    finally:
        print("client shell exited.")
        quit()


if __name__ == "__main__":
    run_client()
