import typer
import socket
import json
import pyperclip
import time
import os
from tabulate import tabulate
import wcwidth


HOST = "localhost"
PC_PORT = 19091
FIRST_TASK_TAG = 'Zmlyc3QgdGFzaw=='

app = typer.Typer()

def start():
    print("Hello")


@app.command(name="list")
def list(search: str = typer.Argument("")):
    os.system('source ~/.bash_profile')
    # 这里暂存到临时文件中，避免控制台输出
    os.system('adb forward tcp:19091 tcp:19191 > temp.log')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PC_PORT))
    sock.send("\n".encode())
    response = get_all_data(sock)
    sock.close()
    tasks = json.loads(response.decode('utf-8'))

    print_list = []
    for index, task in enumerate(tasks, 1):
        print_item = [index, task['title'], task['ownerName'], task['emailPrefix']]
        print_list.append(print_item)
    typer.secho(tabulate(print_list, headers=["ID", "TITLE", "AUTHOR", "Email"], tablefmt='pretty'), fg=typer.colors.BLUE, bold=True)
    typer.secho("\n")

    task_id = typer.prompt("需要执行哪个任务? (输入ID)")
    task = tasks[int(task_id) - 1]
    params_hint = task['method']['paramsHint']
    for index, paramHint in enumerate(params_hint, 0):
        task['method']['params'].append(typer.prompt(task['method']['paramsHint'][index]))
    rsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rsock.connect((HOST, PC_PORT))
    rsock.send(FIRST_TASK_TAG.encode())
    rsock.send("\n".encode())
    rsock.send(json.dumps(task).encode())
    rsock.send("\n".encode())
    response = get_all_data(rsock)
    rsock.close()
    if task['outputType'] == 0:
        pyperclip.copy(response.decode("utf-8"))
        typer.secho(str(response.decode('utf-8')), fg=typer.colors.BLUE, bold=True)
    elif task['outputType'] == 2:
        time_str = time.strftime("%Y-%m-%d-%H_%M_%S")
        # TODO 这里需要配置成用户目录
        file_name = str("/Users/hander/Downloads/") + time_str + ".json"

        f = open(file_name, 'w')
        f.write(json.dumps(json.loads(response)))
        f.close()

        os.system("open " + file_name)
    else:
        # 列表结果
        list_tasks = json.loads(response.decode('utf-8'))

        print_list = []
        for index, task in enumerate(list_tasks, 1):
            print_item = [index, task['title'], task['subTitle']]
            print_list.append(print_item)
        typer.secho(tabulate(print_list, headers=["ID", "TITLE", "SUBTITLE"], tablefmt='simple'),
                    fg=typer.colors.BLUE, bold=True)
        typer.secho("\n")

        selected_index = typer.prompt("选择其中一个选项(输入ID)")
        selected_task = list_tasks[int(selected_index) - 1]

        print_list = []
        for index, task in enumerate(selected_task['options'], 1):
            print_item = [index, task['title'], task['subTitle']]
            print_list.append(print_item)
        typer.secho(tabulate(print_list, headers=["ID", "TITLE", "SUBTITLE"], tablefmt='simple'),
                    fg=typer.colors.BLUE, bold=True)
        typer.secho("\n")

        option_index = int(typer.prompt("选择操作项(输入ID)")) - 1
        exected_method(json.dumps(selected_task['options'][option_index]))


def exected_method(task_str):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PC_PORT))
    sock.send(FIRST_TASK_TAG.encode())
    sock.send("\n".encode())
    sock.send(task_str.encode())
    sock.send("\n".encode())
    response = get_all_data(sock)
    sock.close()
    typer.secho(response, fg=typer.colors.GREEN, bold=True)


def get_all_data(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data
