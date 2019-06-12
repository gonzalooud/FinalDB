import cx_Oracle
import configparser
from bottle import *
from passlib.hash import pbkdf2_sha256

CONFIG = configparser.ConfigParser()
CONFIG.read('hello_world.conf')
USER = CONFIG['hello_world']['user']
PASS = CONFIG['hello_world']['pass']
HOST = CONFIG['bottle']['host']
PORT = CONFIG['bottle']['port']
DEBUG = CONFIG['bottle']['debug']

@route('/salarios')
def get_all_salaries():
    CONNECTION = cx_Oracle.connect(USER, PASS)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute("""SELECT ename, sal FROM emp""")
    result = CURSOR.fetchall()
    col_names = [row[0] for row in CURSOR.description]
    CURSOR.close()
    return template("views/all_salaries", col_names=col_names, rows=result)

@route('/')
@get('/login') # o @route('/login')
def login():
    return template("Views/login")

@post('/login') # o @route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    hash = pbkdf2_sha256.hash(password)
    print(hash)
    if check_login(username, password):
        return "Login correct"
    else:
        return "Login failed"

def check_login(user, password):
    CONNECTION = cx_Oracle.connect(USER, PASS)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute("""SELECT Usuario FROM Usuario Where Usuario = :username """, username=user)
    result = CURSOR.fetchone()
    if result is None:
        CURSOR.close()
        return False
    else:
        CURSOR.execute("""SELECT password FROM Usuario WHERE Usuario= :username""", username=user)
        result = CURSOR.fetchone()
        if pbkdf2_sha256.verify(password, result[0]):
            CURSOR.close()
            return True
        else:
            CURSOR.close()
            return False

@error(404)
def error404(error):
    return 'Nothing here, sorry'


run(host=HOST, port=PORT, debug=DEBUG)
