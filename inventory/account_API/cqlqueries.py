import uuid

from cassandra.cluster import Cluster
from cassandra.cluster import dict_factory

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('model1')
session.row_factory = dict_factory
get_workers_query = session.prepare("SELECT username , fname , lname, mail FROM user_worker ;")
get_admins_query = session.prepare("SELECT username , fname , lname, mail FROM user_admin ;")
create_worker_query = session.prepare(
    "INSERT INTO user_worker (username , fname , lname , password , mail ) VALUES ( ?, ?,?, ?,?) IF NOT EXISTS;")
create_admin_query = session.prepare(
    "INSERT INTO user_admin (username , fname , lname , password , mail  ) VALUES (?, ?, ?,?, ?) IF NOT EXISTS;")
get_worker_query = session.prepare("SELECT username , fname , lname,mail FROM user_worker WHERE username = ? LIMIT 1; ")
get_admin_query = session.prepare("SELECT username , fname , lname,mail FROM user_admin WHERE username = ? LIMIT 1; ")
update_worker_query = session.prepare("UPDATE user_worker SET fname = ? , lname = ? WHERE username = ? IF EXISTS ;")
update_admin_query = session.prepare("UPDATE user_admin SET fname = ? , lname = ? WHERE username = ? IF EXISTS ;")
update_worker_password_query = session.prepare("UPDATE user_worker SET password = ? WHERE username = ? IF EXISTS ;")
update_admin_password_query = session.prepare("UPDATE user_admin SET password = ? WHERE username = ? IF EXISTS ;")
get_admin_password_query = session.prepare("SELECT password FROM user_admin WHERE username = ? LIMIT 1;")
get_worker_password_query = session.prepare("SELECT password FROM user_worker WHERE username = ? LIMIT 1;")
delete_worker_query = session.prepare("DELETE from user_worker WHERE username = ? IF EXISTS;")
delete_admin_query = session.prepare("DELETE from user_admin WHERE username = ? IF EXISTS;")
get_worker_username_query = session.prepare("SELECT username FROM user_worker WHERE username = ?;")
get_admin_username_query = session.prepare("SELECT username FROM user_admin WHERE username = ?;")
register_mail_worker_query = session.prepare("INSERT INTO reg_mail_worker (mail) VALUES (?) IF NOT EXISTS;")
get_all_mail_worker_query = session.prepare("SELECT * FROM reg_mail_worker ;")
get_mail_worker_query = session.prepare("SELECT * FROM reg_mail_worker WHERE mail = ? LIMIT 1;")
remove_mail_worker_query = session.prepare("DELETE from reg_mail_worker  WHERE mail = ? IF EXISTS;")

register_mail_admin_query = session.prepare("INSERT INTO reg_mail_admin (mail) VALUES (?) IF NOT EXISTS;")
get_all_mail_admin_query = session.prepare("SELECT * FROM reg_mail_admin ;")
get_mail_admin_query = session.prepare("SELECT * FROM reg_mail_admin WHERE mail = ? LIMIT 1;")
remove_mail_admin_query = session.prepare("DELETE from reg_mail_admin  WHERE mail = ? IF EXISTS;")
create_session_query = session.prepare(
    "INSERT INTO auth (key , admin , name ) VALUES ( ?,?,?) IF NOT EXISTS using TTL 864000;")


class AlreadyExists(Exception):
    pass


class EmailAlreadyExists(AlreadyExists):
    pass


def get_workers(username=None):
    if username is None:
        workers = session.execute(get_workers_query)
        return workers.all()
    else:
        worker = session.execute(get_worker_query, (username,)).one()
        return worker


def get_worker_username(username):
    username = session.execute(get_worker_username_query, (username,)).one()
    if username is None:
        return None
    return username.get('username')
    # return username
    # return None if 'username' in  username else username['username']


def create_worker(f_name, l_name, password, mail, username=None, ):
    if get_mail_worker(mail):
        raise EmailAlreadyExists
    applied = session.execute(create_worker_query, (username, f_name, l_name, password, mail)).was_applied
    if applied:
        if not register_mail_worker(mail):
            raise EmailAlreadyExists
    return applied


def update_worker(f_name, l_name, username):
    return session.execute(update_worker_query, (f_name, l_name, username)).was_applied


def update_worker_password(username, password):
    return session.execute(update_worker_password_query, (password, username)).was_applied


def get_worker_password(username):
    password = session.execute(get_worker_password_query, (username,)).one()
    if password is None:
        return None
    return password.get('password')


def delete_worker(username):
    worker = get_workers(username=username)
    remove_mail_worker(worker['mail'])
    return session.execute(delete_worker_query, (username,)).was_applied


def register_mail_worker(mail):
    return session.execute(register_mail_worker_query, (mail,)).was_applied


def get_mail_worker(mail=None):
    if mail is None:
        return session.execute(get_all_mail_worker_query).all()
    return session.execute(get_mail_worker_query, (mail,)).one()


def remove_mail_worker(mail):
    return session.execute(remove_mail_worker_query, (mail,)).was_applied


def get_admins(username=None):
    if username is None:
        admin = session.execute(get_admins_query)
        return admin.all()
    else:
        admin = session.execute(get_admin_query, (username,)).one()
        return admin


def create_admin(f_name, l_name, password, mail, username=None):
    if get_mail_admin(mail):
        raise EmailAlreadyExists
    applied = session.execute(create_admin_query, (username, f_name, l_name, password, mail)).was_applied
    if applied:
        if not register_mail_admin(mail):
            raise EmailAlreadyExists
    return applied


def update_admin(f_name, l_name, username):
    return session.execute(update_admin_query, (f_name, l_name, username)).was_applied


def update_admin_password(username, password):
    return session.execute(update_admin_password_query, (password, username)).was_applied


def get_admin_password(username):
    password = session.execute(get_admin_password_query, (username,)).one()
    if password is None:
        return None
    return password.get('password')


def delete_admin(username):
    admin = get_admins(username=username)
    if admin is None:
        return None
    remove_mail_admin(admin['mail'])
    return session.execute(delete_admin_query, (username,)).was_applied


def get_admin_username(username):
    username = session.execute(get_admin_username_query, (username,)).one()
    if username is None:
        return None
    return username.get('username')


def register_mail_admin(mail):
    return session.execute(register_mail_admin_query, (mail,)).was_applied


def get_mail_admin(mail=None):
    if mail is None:
        return session.execute(get_all_mail_admin_query).all()
    return session.execute(get_mail_admin_query, (mail,)).one()


def remove_mail_admin(mail):
    return session.execute(remove_mail_admin_query, (mail,)).was_applied


def generate_token(is_admin, username):
    uid = uuid.uuid4()
    a = session.execute(create_session_query, (uid, bool(is_admin), username)).was_applied
    print(a)
    return uid


if __name__ == '__main__':
    # print(get_workers())
    # print(update_worker('a', 'a', 'a'))
    # print(update_admin('a', 'a', 'ankitad1'))
    # print(update_worker_password(username='a', password='2222w'))
    # print(update_admin_password(username='an1', password='2222w'))
    # print(get_admin_password('m'))
    # print(get_worker_password('m'))
    # print(delete_worker(username='a'))
    # print(delete_admin(username='a'))
    # print(bool(get_worker_username('mongodb')))
    # print(register_mail_worker('akshay'))
    # print(get_mail_worker(mail='akshay'))
    # print(remove_mail_worker('aayush12'))
    # id = uuid.uuid4()
    # a = session.prepare("INSERT INTO auth (key , admin , name ) VALUES ( ?,?,?) using TTL 864000;")
    # b = session.execute(a, (id, True, 'me'))
    a = generate_token(True, 'akshay')
    print(a)
