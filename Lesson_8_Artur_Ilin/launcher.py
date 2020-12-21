import subprocess

PROCESSES = []

while True:
    ACTION = input('Выберите действие:'
                   '\n s - запустить сервер и клиенты'
                   '\n x - Закрыть все процессы'
                   '\n q - Выход'
                   '\n >> ')
    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESSES.append(subprocess.Popen('python server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))

        for num in range(3):
            PROCESSES.append(subprocess.Popen(f'python client.py -n user_{num + 1}', creationflags=subprocess.CREATE_NEW_CONSOLE))



    elif ACTION == 'x':
        while PROCESSES:
            VICTIM = PROCESSES.pop()
            VICTIM.kill()
