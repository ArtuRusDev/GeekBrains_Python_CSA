import sys
from subprocess import Popen, CREATE_NEW_CONSOLE

while True:
    CLIENTS_COUNT = 5
    pope_list = []

    usr_answer = input('Запустить 5 клиентов - "s" \n'
                       'Закрыть всех клиентов - "c" \n'
                       'Запустить сервер - "s" \n'
                       'Выход - "q" \n'
                       '>> ')
    if usr_answer == 's':
        for _ in range(CLIENTS_COUNT):
            pope_list.append(Popen('python client.py', creationflags=CREATE_NEW_CONSOLE))

        print('*** Started 10 clients ***')

    elif usr_answer == 'c':
        print(pope_list)
        for item in pope_list:
            print(item)
            item.kill()

        print('*** Clients killed ***')
    elif usr_answer == 's':
        server = Popen('python3 server.py', creationflags=CREATE_NEW_CONSOLE)
        print('*** Started server ***')

    elif usr_answer == 'q':
        sys.exit(1)
