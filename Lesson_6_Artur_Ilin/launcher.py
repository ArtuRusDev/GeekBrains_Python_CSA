import subprocess

PROCESS = []

while True:
    ACTION = input('Выберите действие:'
                   '\n s - запустить сервер и клиенты'
                   '\n x - Закрыть все процессы'
                   '\n q - Выход'
                   '\n >> ')
    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESS.append(subprocess.Popen('python server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))

        for _ in range(1):
            PROCESS.append(subprocess.Popen('python client.py -m send', creationflags=subprocess.CREATE_NEW_CONSOLE))

        for _ in range(2):
            PROCESS.append(subprocess.Popen('python client.py -m listen', creationflags=subprocess.CREATE_NEW_CONSOLE))

    elif ACTION == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()
