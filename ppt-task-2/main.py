import socket
import json
import os


def envFind():
    a = []
    for key in os.environ:
        if key == 'host':
            a.append(os.environ[key])
            print(key)
        if key == 'port':
            a.append(int(os.environ[key]))
            print(key)
    return a


def main():
    socket_address = ('127.0.0.1', 80)
    a = envFind()
    if len(a) == 2:
        socket_address = a
    BUFF_SIZE = 65536
    timeout = 5
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    server_socket.sendto(b'INIT_CIRC', socket_address)
    server_socket.settimeout(timeout)
    try:
        msg, addr = server_socket.recvfrom(BUFF_SIZE)
    except socket.timeout:
        print('Не удалось установить подключение')
        server_socket.close()
        return
    while True:
        server_socket.sendto(b'CIRC_STATE', socket_address)
        server_socket.settimeout(timeout)
        try:
            msg, addr = server_socket.recvfrom(BUFF_SIZE)
        except socket.timeout:
            print('Превышено время ожидания')
            server_socket.close()
            return
        if msg == b'SOLID':
            continue
        elif msg == b'BREAK':
            while msg != b'STOPPED':
                server_socket.sendto(b'ALARM', addr)
                msg, addr = server_socket.recvfrom(BUFF_SIZE)
            server_socket.sendto(b'CIRC_ALL_STATE', addr)
            try:
                msg, addr = server_socket.recvfrom(BUFF_SIZE)
            except socket.timeout:
                print('Превышено время ожидания')
                server_socket.close()
                return
            data = json.loads(msg)
            if data['ebuttom'] == True:
                print('Нажата кнопка экстренной остановки')
            if data['end_cap'] == True:
                print('Достигнута предельная деформация демпфера')
            for i in data['dist']:
                if i < 50:
                    print('Превышена предельная дистанция дальномера')
                    break
            server_socket.close()
            return


if __name__ == '__main__':
    main()
