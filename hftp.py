import socket
import os

from multiprocessing import Process


def handle_client(client_socket):
    request_data = client_socket.recv(1024)

    response_start_line = "HTTP/1.1 200 ok\r\n"
    response_headers = "Server: HFTP\r\n"
    response_body = "\n".join(os.listdir("."))
    response = response_start_line + response_headers + "\r\n" + response_body

    client_socket.send(bytes(response, "utf-8"))

    client_socket.close()


if __name__ == "__main__":
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", 80))
    server_socket.listen()

    print("Start working on: " + ip)

    while True:
        client_socket, client_address = server_socket.accept()
        print("[%s, %s] is connected!" % client_address)
        handle_client_process = Process(target=handle_client,args=(client_socket,))
        handle_client_process.start()
        client_socket.close()
