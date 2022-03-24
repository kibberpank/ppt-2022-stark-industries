import socket
import json
import os


def envFind():
    for key in os.environ:
        if key == 'host':
            ip = os.environ[key]
        if key == 'port':
            port = int(os.environ[key])
        return ip, port


def main():
    socket_address = envFind()
    BUFF_SIZE = 65536
    timeout = 5
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    server_socket.bind(socket_address)
    server_socket.sendto(b'INIT_CIRC')
    server_socket.settimeout(timeout)
    try:
        msg, addr = server_socket.recvfrom(BUFF_SIZE)
    except socket.timeout:
        print('Не удалось установить подключение')
        return
    while True:
        server_socket.sendto(b'CIRC_STATE')
        server_socket.settimeout(timeout)
        try:
            msg, addr = server_socket.recvfrom(BUFF_SIZE)
        except socket.timeout:
            print('Превышено время ожидания')
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
            return


if __name__ == '__main__':
    main()
