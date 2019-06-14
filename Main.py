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
    CURSOR.execute("""INSERT INTO USUARIO VALUES ('admin','admin')""")
    CURSOR.execute("""SELECT * FROM usuario""")
    result = CURSOR.fetchall()
    col_names = [row[0] for row in CURSOR.description]
    CURSOR.close()
    return template("Views/Tablas", col_names=col_names, rows=result)


@get('/NuevoFisico') # o @route('/NuevoFisico')
def NuevoFisico():
    return template("Views/NuevoFisico")

@post('/NuevoFisico') # o @route('/NuevoFisico', method='POST')
def do_NuevoFisico():
    dni= request.forms.get('dni')
    cuil= request.forms.get('cuil')
    nombre= request.forms.get('nombre')
    apellido= request.forms.get('apellido')
    usuario= request.forms.get('usuario')
    contrasenia= request.forms.get('contrasenia')
    hashContra = pbkdf2_sha256.hash(contrasenia)
    return agregar_fisico(dni,cuil,nombre,apellido,usuario,hashContra)


@get('/NuevoJuridico') # o @route('/NuevoJuridico')
def NuevoJuridico():
    return template("Views/NuevoJuridico")

@post('/NuevoJuridico') # o @route('/NuevoJuridico', method='POST')
def do_NuevoJuridico():
    razonSocial= request.forms.get('RazonSocial')
    cuil= request.forms.get('cuil')
    usuario= request.forms.get('usuario')
    contrasenia= request.forms.get('contrasenia')
    hashContra = pbkdf2_sha256.hash(contrasenia)
    return agregar_juridico(razonSocial,cuil,usuario,hashContra)


@get('/ModificarFisico') # o @route('/ModificarFisico')
def ModificarFisico():
    return template("Views/ModificarFisico")

@post('/ModificarFisico') # o @route('/ModificarFisico', method='POST')
def do_ModificarFisico():
    dni= request.forms.get('dni')
    cuil= request.forms.get('cuil')
    nombre= request.forms.get('nombre')
    apellido= request.forms.get('apellido')
    return modificar_fisico(dni,cuil,nombre,apellido)

@get('/ModificarJuridico') # o @route('/ModificarJuridico')
def ModificarJuridico():
    return template("Views/ModificarJuridico")

@post('/ModificarJuridico') # o @route('/ModificarJuridico', method='POST')
def do_ModificarJuridico():
    razonSocial= request.forms.get('RazonSocial')
    cuil= request.forms.get('cuil')
    return modificar_juridico(razonSocial, cuil)

@route('/')
@get('/login') # o @route('/login')
def login():
    return template("Views/login")

@post('/login') # o @route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
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
        #CAMBIAR PASSWORD A CONTRASENIA
        CURSOR.execute("""SELECT contrasenia FROM Usuario WHERE Usuario= :username""", username=user)
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

@route('/consulta2')
def consulta2():
    CONNECTION = cx_Oracle.connect(USER, PASS)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute("""select extract(year from ib.fechaPago) Año, SUM (ib.alicuota) IIBB SUM(a.alicuota) AUTOS 	SUM(t.alicuota) TASAS SUM(s.alicuota) SELLOS SUM(inm.alicuota) INMUEBLES 
        from CuentaCorrientexImpIngresosBrutos ib, CuentaCorrientexImpAuto a
        CuentaCorrientexTasas t, CuentaCorrientexImpSellos s, 
        CuentaCorrientexImpInmueble inm
        where  (extract(year from ib.FechaPago) = extract(year from a.FechaPago))
	        and (extract(year from ib.FechaPago) = extract(year from t.FechaPago))
            and (extract(year from ib.FechaPago) = extract(year from s.FechaPago))
            and (extract(year from ib.FechaPago) = extract(year from inm.FechaPago))
            and (extract(month from ib.FechaPago) = extract(month from a.FechaPago))
            and (extract(month from ib.FechaPago) = extract(month from t.FechaPago))
            and (extract(month from ib.FechaPago) = extract(month from s.FechaPago))
            and (extract(month from ib.FechaPago) = extract(month from inm.FechaPago))
        group by extract(year from ib.fechaPago);""")
    result = CURSOR.fetchall()
    col_names = [row[0] for row in CURSOR.description]
    CURSOR.close()
    return template("Views/Tablas", col_names=col_names, rows=result)


@get('/consulta3') # o @route('/consulta3')
def consulta3():
    return template("Views/consulta3Form")

@post('/consulta3') # o @route('/consulta3', method='POST')
def do_consulta3():
    dominio = request.forms.get('dominio')
    CONNECTION = cx_Oracle.connect(USER, PASS)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute("""select a.modelo modelo , t.antiguotitular TitularAntiguo,t.fecha Fecha,
        case when f.nombre=NULL then j.usuario or 
        case when j.usuario=NULL then f.nombre
        end Titular
        from transferencia t
        inner join autos a on a.patente=t.patente
        inner join fisica f on f.DNI=a.DNI
        inner join juridica j on j.DNI=a.DNI
        where t.patente=:dominio;""", dominio=dominio)
    result = CURSOR.fetchall()
    col_names = [row[0] for row in CURSOR.description]
    CURSOR.close()
    return template("Views/Tablas", col_names=col_names, rows=result)

@route('/consulta4')
def consulta4():
    CONNECTION = cx_Oracle.connect(USER, PASS)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute("""select i.direccion direccion,i.numero numero,i.piso piso,i.depto depto
        from ValoresInmuebles v
        inner join inmuebles i on i.id=v.id
        where v.Fecha = (current_date from dual - 365)
        and v.valor>=1000000;""")
    result = CURSOR.fetchall()
    col_names = [row[0] for row in CURSOR.description]
    CURSOR.close()
    return template("Views/Tablas", col_names=col_names, rows=result)

@get('/consulta6') # o @route('/consulta6')
def consulta6():
    return template("Views/consulta6Form")

@post('/consulta6') # o @route('/consulta6', method='POST')
def do_consulta6():
    fecha1= request.forms.get('fecha1')
    fecha2 = request.forms.get('fecha2')
    CONNECTION = cx_Oracle.connect(USER, PASS)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute("""select SUM (ib.alicuota) IIBB, SUM(a.alicuota) AUTOS, SUM(t.alicuota) TASAS, SUM(s.alicuota) SELLOS, SUM(inm.alicuota) INMUEBLES,
            (SUM (ib.alicuota) / (SUM (ib.alicuota + a.alicuota + t.alicuota + s.alicuota + inm.alicuota))) %IIBB,
            (SUM (a.alicuota) / (SUM (ib.alicuota + a.alicuota + t.alicuota + s.alicuota + inm.alicuota))) %AUTO,
            (SUM (t.alicuota) / (SUM (ib.alicuota + a.alicuota + t.alicuota + s.alicuota + inm.alicuota))) %TASAS,
            (SUM (s.alicuota) / (SUM (ib.alicuota + a.alicuota + t.alicuota + s.alicuota + inm.alicuota))) %SELLOS,
            (SUM (inm.alicuota) / (SUM (ib.alicuota + a.alicuota + t.alicuota + s.alicuota + inm.alicuota))) %INMUEBLES
            from CuentaCorrientexImpIngresosBrutos ib, CuentaCorrientexImpAuto a, CuentaCorrientexTasas t, CuentaCorrientexImpSellos s, 
            CuentaCorrientexImpInmueble inm
            where (ib.FechaPago between to_date (:fecha1, 'yyyy/mm/dd') and to_date (:fecha2, 'yyyy/mm/dd'))
            and (a.FechaPago between to_date (:fecha1, 'yyyy/mm/dd') and to_date (:fecha2, 'yyyy/mm/dd'))
            and (t.FechaPago between to_date (:fecha1, 'yyyy/mm/dd') and to_date (:fecha2, 'yyyy/mm/dd'))
            and (s.FechaPago between to_date (:fecha1, 'yyyy/mm/dd') and to_date (:fecha2, 'yyyy/mm/dd'))
            and (inm.FechaPago between to_date (:fecha1, 'yyyy/mm/dd') and to_date (:fecha2, 'yyyy/mm/dd'))
            group by extract (year from ib.fechaPago), extract(month from ib.fechaPago)""",
                   fecha1=fecha1, fecha2=fecha2)
    result = CURSOR.fetchall()
    col_names = [row[0] for row in CURSOR.description]
    CURSOR.close()
    return template("Views/Tablas", col_names=col_names, rows=result)

def agregar_fisico(dni,cuil,nombre,apellido,usuario,contrasenia):
    CONNECTION = cx_Oracle.connect(USER, PASS)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute("""INSERT INTO USUARIO VALUES (:usuar, :contra)""", usuar=usuario, contra=contrasenia)
    CURSOR.execute("""INSERT INTO FISICA (DNI, CUIL, Nombre, Apellido, Usuario)
            VALUES (:dni, :cuil, :nombre, :apellido, :usuario)""", dni=dni, cuil=cuil, nombre=nombre,
                    apellido=apellido, usuario=usuario)
    CURSOR.execute("""SELECT * FROM FISICA WHERE DNI = :dni""", dni=dni)
    result = CURSOR.fetchall()
    col_names = [row[0] for row in CURSOR.description]
    CURSOR.execute("""commit""")
    CURSOR.close()
    return template("Views/Tablas", col_names=col_names, rows=result)

def agregar_juridico(razonSocial,cuil,usuario,contrasenia):
    CONNECTION = cx_Oracle.connect(USER, PASS)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute("""INSERT INTO USUARIO VALUES (:usuar, :contra)""", usuar=usuario, contra=contrasenia)
    CURSOR.execute("""INSERT INTO Juridica (razonsocial, CUIL, Usuario)
            VALUES (:razonSocial, :cuil, :usuario)""", razonSocial=razonSocial, cuil=cuil, usuario=usuario)
    CURSOR.execute("""SELECT * FROM juridica WHERE razonsocial = :razonSocial""", razonSocial=razonSocial)
    result = CURSOR.fetchall()
    col_names = [row[0] for row in CURSOR.description]
    CURSOR.execute("""commit""")
    CURSOR.close()
    return template("Views/Tablas", col_names=col_names, rows=result)

def modificar_fisico(dni,cuil,nombre,apellido):
    CONNECTION = cx_Oracle.connect(USER, PASS)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute("""UPDATE FISICA
            SET CUIL=:cuil, nombre=:nombre, apellido=:apellido
            WHERE dni=:dni""",cuil=cuil, nombre=nombre, apellido=apellido, dni=dni)
    CURSOR.execute("""SELECT * FROM FISICA WHERE DNI = :dni""", dni=dni)
    result = CURSOR.fetchall()
    col_names = [row[0] for row in CURSOR.description]
    CURSOR.execute("""commit""")
    CURSOR.close()
    return template("Views/Tablas", col_names=col_names, rows=result)

def modificar_juridico(razonSocial,cuil):
    CONNECTION = cx_Oracle.connect(USER, PASS)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute("""UPDATE juridica
            SET CUIL=:cuil
            WHERE Razon_Social=:razonSocial""",cuil=cuil, razonSocial=razonSocial)
    CURSOR.execute("""SELECT * FROM juridica WHERE Razon_Social = :razonSocial""", razonSocial=razonSocial)
    result = CURSOR.fetchall()
    col_names = [row[0] for row in CURSOR.description]
    CURSOR.execute("""commit""")
    CURSOR.close()
    return template("Views/Tablas", col_names=col_names, rows=result)

@error(404)
def error404(error):
    return 'Nothing here, sorry'


run(host=HOST, port=PORT, debug=DEBUG)
