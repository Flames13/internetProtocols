import argparse
import requests


TOKEN = ''  # here must be token from vk.com


def create_parser():
    parser = argparse.ArgumentParser(description='Generate fictious data',
                                     epilog='(c) Piskunova Victoria 2018')
    parser.add_argument('id', type=str, help='Id of user')
    parser.add_argument('-g', '--groups', action='store_true',
                        help='Show groups of this user')
    parser.add_argument('-f', '--friends', action='store_true',
                        help='Show friends of this user')
    parser.add_argument('-i', '--info', action='store_true',
                        help='Show info about user who token used')
    return parser


def get_user_info():
    response = requests.get(
        'https://api.vk.com/method/account.getProfileInfo?user_id={}&access_token={}&v=5.52'.format(
            '', TOKEN)).json()['response']
    print('{} {}'.format(response['first_name'], response['last_name']))
    print('Никнейм: {}'.format(response['screen_name']))
    print('Дата рождения: {}'.format(response['bdate']))
    print('Страна: {}, город: {}'.format(response['country']['title'], response['city']['title']))


def get_user_friends(id_):
    friends = requests.get(
        'https://api.vk.com/method/friends.get?user_id={}&order=name&fields=city&access_token={}&v=5.95'.format(
            id_, TOKEN)).json()['response']
    print('Список друзей [{}]'.format(friends['count']))
    for friend in friends['items']:
        status = 'online' if friend['online'] == 1 else 'offline'
        city = '' if 'city' not in friend.keys() else ' Город: {}'.format(friend['city']['title'])
        print('{} {} Статус: {}{}'.format(friend['first_name'], friend['last_name'], status, city))


def get_user_groups(id_):
    groups = requests.get(
        'https://api.vk.com/method/groups.get?user_id={}&extended=1&access_token={}&v=5.95'.format(
            id_, TOKEN)).json()['response']
    print('Список групп [{}]'.format(groups['count']))
    for group in groups['items']:
        print(group['name'])


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    if namespace.info:
        get_user_info()
    if namespace.friends:
        try:
            get_user_friends(namespace.id)
        except KeyError:
            print('У данного пользователя закрытый профиль или такого пользователя не сушествует')
    if namespace.groups:
        try:
            get_user_groups(namespace.id)
        except KeyError:
            print('У данного пользователя закрытый профиль или такого пользователя не сушествует')
