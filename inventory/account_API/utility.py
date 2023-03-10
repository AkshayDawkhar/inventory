import random
from . import cqlqueries as accountCQL


def generate_username(f_name, l_name, b):
    username = f_name + l_name + str(random.randint(a=0, b=b))
    return username


def generate_unique_usernames(f_name, l_name):
    username = f_name + l_name
    b = 0
    while accountCQL.get_worker_username(username):
        b = b+10
        username = generate_username(f_name, l_name, b=b)
    return username


def generate_unique_admin_usernames(f_name, l_name):
    username = f_name + l_name
    b = 0
    while accountCQL.get_admin_username(username):
        b = b+10
        username = generate_username(f_name, l_name, b=b)
    return username


if __name__ == '__main__':
    # print(generate_username('a', 'b', 12))
    print(generate_unique_usernames('mongo', 'db'))
