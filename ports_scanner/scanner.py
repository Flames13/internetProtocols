import argparse
import socket
import time
from functools import partial
from multiprocessing.dummy import Pool

UDP_MESSAGE = b'Hello, World!'


def create_parser():
    parser = argparse.ArgumentParser(description='Сканер TCP и UDP портов')
    parser.add_argument('host', type=str, help='Хост')
    parser.add_argument('start', type=int, help='Порт, с которого начать сканирование')
    parser.add_argument('end', type=int, help='Порт, до которого продолжать сканирование')
    return parser


def scan_tcp(host, port):
    socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_.settimeout(1)
    result = socket_.connect_ex((host, port))
    if not result:
        print('Open TCP port {}'.format(port))
    socket_.close()


def scan_udp(host, port):
    socket_ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        socket_.sendto(UDP_MESSAGE, (host, port))
        socket_.settimeout(1)
        socket_.recvfrom(512)
    except socket.error:
        pass
    else:
        print('Open UDP port {}'.format(port))
    finally:
        socket_.close()
        time.sleep(1)


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    host_ip = socket.gethostbyname(namespace.host)
    start = namespace.start
    end = namespace.end
    if end < start:
        start, end = end, start
    pool = Pool(700)
    pool.map(partial(scan_tcp, host_ip), range(start, end + 1))
    for port in range(start, end + 1):
        scan_udp(host_ip, port)
    pool.close()
