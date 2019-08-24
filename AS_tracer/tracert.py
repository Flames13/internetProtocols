from subprocess import check_output
import argparse
import json
import re
import requests
import sys


IP_RE = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
AS_RE = re.compile(r'AS\d+')


def create_parser():
    parser = argparse.ArgumentParser(description='Трассировка автономных систем')
    parser.add_argument('address', type=str,
                        help='IP-адрес или доменное имя, до которого осуществляется трассировка')
    return parser


def trace(address):
    try:
        result = check_output(['tracert', address]).decode('cp866').split('\n')
        addresses = []
        for line in result:
            ip = re.search(IP_RE, line)
            if ip:
                addresses.append(ip.group(0))
        addresses.pop(0)
    except Exception as e:
        print(e)
        sys.exit(1)
    return addresses


def get_ip_data(addresses):
    result = []
    for ip in addresses:
        response = requests.get('http://ip-api.com/json/' + ip)
        answer = json.loads(response.content)
        ip_info = []
        if answer['status'] == 'success':
            auto_sys = re.search(AS_RE, answer['as'])
            country = answer['country']
            provider = answer['isp']
            ip_info.append(ip)
            ip_info.append(auto_sys.group(0) if auto_sys else '—')
            ip_info.append(country if country else '—')
            ip_info.append(provider if provider else '—')
        else:
            ip_info = [ip, '—', '—', '—']
        result.append(ip_info)
    return result


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    ip_addresses = trace(namespace.address)
    if len(ip_addresses) < 3:
        print('Не удалось выполнить трассировку')
        sys.exit(1)

    ip_data = get_ip_data(ip_addresses)
    i = 0
    for ip in ip_data:
        i += 1
        print('№{} IP {} AS {} COUNTRY {} PROVIDER {}'.format(i, ip[0], ip[1], ip[2], ip[3]))
