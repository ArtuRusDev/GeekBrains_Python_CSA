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
        PROCESS.append(subprocess.Popen('python3 server.py', shell=True))

        for _ in range(3):
            PROCESS.append(subprocess.Popen('python3 client.py', shell=True))
    elif ACTION == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()