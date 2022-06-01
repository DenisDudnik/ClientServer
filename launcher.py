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

        process_lst.append(subprocess.Popen(
            'python client.py -n User1', creationflags=subprocess.CREATE_NEW_CONSOLE))
        process_lst.append(subprocess.Popen(
            'python client.py -n User2', creationflags=subprocess.CREATE_NEW_CONSOLE))
        process_lst.append(subprocess.Popen(
            'python client.py -n User3', creationflags=subprocess.CREATE_NEW_CONSOLE))
