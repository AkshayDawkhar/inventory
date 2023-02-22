import random
import string


def generate_username(f_name, l_name):
    username = f_name + l_name + str(random.randint(a=0, b=100))
    return username


if __name__ == '__main__':
    print(generate_username('a', 'b'))
