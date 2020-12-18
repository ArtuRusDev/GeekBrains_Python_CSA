from select import select
from socket import AF_INET, socket, SOCK_STREAM


def read_clients(clients, all_cln):
    responses = {}

    for sock in clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            responses[sock] = data
            print(data)
            
        except Exception as e:
            print(e)
            print(f'Клиент {sock.fileno()} отключился')
            all_cln.remove(sock)

    return responses


def write_responses(requests, cln_write, all_cln):
    for sock in cln_write:
        if sock in requests:
            try:
                response = requests[sock].upper()
                sock.send(response.encode('utf-8'))
            except Exception as e:
                print(f'Клиент {sock.fileno()} отключился')
                sock.close()
                all_cln.remove(sock)


def main_loop():
    adr = ('', 8888)
    clients = []

    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.bind(adr)
        sock.listen(5)
        sock.settimeout(0.2)

        while True:
            try:
                conn, address = sock.accept()
            except OSError as e:
                pass
            else:
                print(f'Получен запрос на соединение с {str(address)}')
                clients.append(conn)
            finally:
                wait = 0
                r = []
                w = []

                try:
                    r, w, e = select(clients, clients, [], wait)
                    print(f'Чтение - {r}')
                    print(f'Запись - {w}')
                except Exception as e:
                    pass

                requests = read_clients(r, clients)
                # print(requests)
                if requests:
                    print(requests)
                    write_responses(requests, w, clients)


print('Server started!')
main_loop()
