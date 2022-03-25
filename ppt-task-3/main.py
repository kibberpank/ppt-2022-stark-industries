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


def coordinateFind(js):
    data = json.load(js)
    x = data['X']
    y = data['Y']
    z = data['Z']
    return x, y, z


def moving(server_socket, x, y, adr, BUFF_SIZE, control):
    string = str(x)+':'+str(y) + ':' + '8,5'
    bit = string.encode('UTF-8')
    server_socket.sendto(b'YOUNG_LMOVE:' + bit, adr)
    server_socket.sendto(b'YOUNG_TPOS', adr)
    msg, adr = server_socket.recvfrom(BUFF_SIZE)
    while int(coordinateFind(msg)[control]) != int((x, y, z)[control]):
        server_socket.sendto(b'YOUNG_TPOS', adr)
        msg, adr = server_socket.recvfrom(BUFF_SIZE)


def curveMoving(server_socket, xs, x, ys, y, num, adr, BUFF_SIZE):
    for i in range(num):
        a = [abs(xs[i]-x), abs(ys[i]-y)]
        moving(server_socket, xs[i], ys[i], adr, BUFF_SIZE, a.index(max(a)))
        x, y = xs[i], ys[i]


def main():
    socket_address = ('127.0.0.1', 80)
    a = envFind()
    if len(a) == 2:
        socket_address = (a[0], a[1])
    BUFF_SIZE = 65536
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    server_socket.sendto(b'YOUNG_INIT', socket_address)
    msg, adr = server_socket.recvfrom(BUFF_SIZE)
    if msg == b'YOUNG_START':
        moving(server_socket, -34.378, -42.183, adr, BUFF_SIZE, 1)
        server_socket.sendto(b'GLUE_PUMP_ON', adr)
        xs = [-34.964, -46.379, -46.379, -34.964, -34.964, -46.379, -46.379, -34.964, -34.964, -46.379, -46.379, -34.964, -34.964, -46.379, -46.379, -34.964, -34.964, -46.379, -46.379, -27.330, -19.642, -13.509, -10.254, -7.158, -3.016, 0, 4.505, 9.843, 15, 19.363, 22.013, 24.285, 25.202, 25.202, 25.5, 28.5, 33.174, 33.174, 2.3, -0.569, -7.309, -12.044, -15.826, -33.671, -34.378]
        points = [-32.769, -32.769, -26.789, -26.789, -12.769, -12.769, -6.789, -6.789, 7.231, 7.231, 13.231, 13.231, 27.231, 27.231, 33.231, 33.231, 47.817, 47.817, 53.231, 53.523, 51.860, 46.623, 39.723, 34.582, 30.466, 28.794, 21.110, 26.484, 25, 21.903, 19.281, 14.675, 8.624, 3, -4, -10.5, -16.586, -19.233, -50.428, -50.73, -45.36, -43.365, -42.561, -42.561, -42.183]
        curveMoving(server_socket, xs, xs[-1], points, points[-1], len(xs), adr, BUFF_SIZE)
        server_socket.sendto(b'GLUE_PUMP_OFF', adr)
        server_socket.sendto(b'YOUNG_HOME', adr)
        server_socket.sendto(b'YOUNG_TPOS', adr)
        msg, adr = server_socket.recvfrom(BUFF_SIZE)
        while int(coordinateFind(msg)[0]) != 0 and int(coordinateFind(msg)[1]) != 0 and int(coordinateFind(msg)[2]) != 50:
            server_socket.sendto(b'YOUNG_TPOS', adr)
            msg, adr = server_socket.recvfrom(BUFF_SIZE)
        server_socket.sendto(b'YOUNG_DISCONNECT', adr)
        server_socket.close()


if __name__ == '__main__':
    main()
