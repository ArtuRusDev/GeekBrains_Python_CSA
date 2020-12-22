from socket import socket, AF_INET, SOCK_STREAM


def send_msg():
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect(('localhost', 8888))
        while True:
            message = input('Enter your message: ')
            if message.lower() == 'exit':
                break
            sock.send(message.encode('utf-8'))
            response = sock.recv(1024)
            print(response.decode('utf-8'))


if __name__ == '__main__':
    send_msg()
