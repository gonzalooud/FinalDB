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
    return template("Views/Tablas", col_names=col_names, rows=result)

@route('/')
@get('/login') # o @route('/login')
def login():
    return template("Views/login")

@post('/login') # o @route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    #hash = pbkdf2_sha256.hash(password)
    #print(hash)
    if check_login(username, password):
        return principal()
    else:
        return login()

@route('/Principal')
def principal():
    return template("Views/Principal")

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

@route('/consulta1')
def consulta1():
    CONNECTION = cx_Oracle.connect(USER, PASS)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute("""select extract(year from ib.fechaPago) Año, SUM (ib.alicuota + a.alicuota + t.alicuota + s.alicuota + inm.alicuota) Monto
    from CuentaCorrientexImpIngresosBrutos ib, CuentaCorrientexImpAuto a
        CuentaCorrientexTasas t, CuentaCorrientexImpSellos s, 
        CuentaCorrientexImpInmueble inm
    where (extract(year from ib.FechaPago) = extract(year from a.FechaPago))
	    and (extract(year from ib.FechaPago) = extract(year from t.FechaPago))
        and (extract(year from ib.FechaPago) = extract(year from s.FechaPago))
        and (extract(year from ib.FechaPago) = extract(year from inm.FechaPago))
    group by extract(year from ib.fechaPago);""")
    result = CURSOR.fetchall()
    col_names = [row[0] for row in CURSOR.description]
    CURSOR.close()
    return template("Views/Tablas", col_names=col_names, rows=result)


@error(404)
def error404(error):
    return 'Nothing here, sorry'


run(host=HOST, port=PORT, debug=DEBUG)
