import subprocess

process_lst = []

while True:
    action = input(
        'Choose: q - quit, x - close all windows, s - run server and clients: ')

    if action == 'q':
        break
    elif action == 'x':
        for process in process_lst:
            process.kill()
        process_lst = []
    elif action == 's':
        process_lst.append(subprocess.Popen(
            'python server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))

        for _ in range(2):
            process_lst.append(subprocess.Popen(
                'python client.py -m send', creationflags=subprocess.CREATE_NEW_CONSOLE))

        for _ in range(5):
            process_lst.append(subprocess.Popen(
                'python client.py', creationflags=subprocess.CREATE_NEW_CONSOLE))
