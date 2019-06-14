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
    #CURSOR.execute("""INSERT INTO USUARIO VALUES (:algo,:algo)""", algo='chanchito')
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
    CURSOR.execute("""select extract(year from ib.fechapago) Anio, SUM(ib.alicuota + a.alicuota + t.alicuota + s.alicuota + inm.alicuota) Monto
from cuentacorrienteimpbruto ib, cuentacorrienteImpAuto a,
CuentaCorrienteTasa t, CuentaCorrienteImpSello s, 
CuentaCorrienteImpInmueble inm
where (extract(year from ib.fechapago) = extract(year from a.fechapago))
and (extract(year from a.fechapago) = extract(year from t.fechapago))
and (extract(year from t.fechapago) = extract(year from s.fechapago))
and (extract(year from s.fechapago) = extract(year from inm.fechapago))
group by extract(year from ib.fechapago)""")
    result = CURSOR.fetchall()
    col_names = [row[0] for row in CURSOR.description]
    CURSOR.close()
    return template("Views/Tablas", col_names=col_names, rows=result)

@route('/consulta2')
def consulta2():
    CONNECTION = cx_Oracle.connect(USER, PASS)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute("""select extract(year from ib.fechaPago) Anio, SUM (ib.alicuota) IIBB, SUM(a.alicuota) AUTOS, SUM(t.alicuota) TASAS, SUM(s.alicuota) SELLOS, SUM(inm.alicuota) INMUEBLES 
        from CuentaCorrienteImpBruto ib, CuentaCorrienteImpAuto a,
        CuentaCorrienteTasa t, CuentaCorrienteImpSello s, 
        CuentaCorrienteImpInmueble inm
        where  (extract(year from ib.FechaPago) = extract(year from a.FechaPago))
	        and (extract(year from ib.FechaPago) = extract(year from t.FechaPago))
            and (extract(year from ib.FechaPago) = extract(year from s.FechaPago))
            and (extract(year from ib.FechaPago) = extract(year from inm.FechaPago))
            and (extract(month from ib.FechaPago) = extract(month from a.FechaPago))
            and (extract(month from ib.FechaPago) = extract(month from t.FechaPago))
            and (extract(month from ib.FechaPago) = extract(month from s.FechaPago))
            and (extract(month from ib.FechaPago) = extract(month from inm.FechaPago))
        group by extract(year from ib.fechaPago)""")
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
    CURSOR.execute("""select autos.modelo modelo, transferencia.antiguotitular TitularAntiguo, transferencia.fecha Fecha,
    (CASE WHEN fisico.dni IS NOT NULL THEN fisico.nombre ELSE 
    (CASE WHEN juridica.razonsocial IS NOT NULL THEN juridica.razonsocial END) END) Titular
    from transferencia, autos, fisico, juridica
    where transferencia.patente= :dominio
    and transferencia.patente=autos.patente
    and (autos.dni=fisico.dni or juridica.razonsocial= autos.razonsocial)
    and ROWNUM=1""", dominio=dominio)
    result = CURSOR.fetchall()
    col_names = [row[0] for row in CURSOR.description]
    CURSOR.close()
    return template("Views/Tablas", col_names=col_names, rows=result)

@route('/consulta4')
def consulta4():
    CONNECTION = cx_Oracle.connect(USER, PASS)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute("""select i.direccion direccion,i.numero numero,i.piso piso,i.depto depto, v.valor Valor
        from ValoresInmueble v, inmueble i
        where i.codigo=v.codigo
        and extract(year from v.fecha) between ((extract(year from((CURRENT_DATE) - 365)))) and (extract(year from (CURRENT_DATE)))
        and v.valor >= 1000000""")
    result = CURSOR.fetchall()
    col_names = [row[0] for row in CURSOR.description]
    CURSOR.close()
    return template("Views/Tablas", col_names=col_names, rows=result)

@route('/consulta5')
def consulta5():
    CONNECTION = cx_Oracle.connect(USER, PASS)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute("""select d.codigo Delegacion, extract(year from inm.FechaPago) Year, extract(month from ib.FechaPago) Month, SUM (ib.alicuota + a.alicuota + t.alicuota + s.alicuota +inm.alicuota) Recaudacion
from CuentaCorrienteImpBruto ib, CuentaCorrienteImpAuto a,
        CuentaCorrienteTasa t, CuentaCorrienteImpSello s, 
        CuentaCorrienteImpInmueble inm ,Delegaciones d
inner join fisico f on d.codigo = f.codigo
inner join juridica j on d.codigo = j.codigo
where 
    ib.FechaPago between date '2018-08-09' and date '2019-09-08'
    and a.FechaPago between date '2018-08-09' and date '2019-09-08'
    and t.FechaPago between date '2018-08-09' and date '2019-09-08'
    and s.FechaPago between date '2018-08-09' and date '2019-09-08'
    and inm.FechaPago between date '2018-08-09' and date '2019-09-08'
    and d.codigo = f.codigo
    and d.codigo = j.codigo
    group by  extract(year from ib.FechaPago), ib.FechaPago, extract(year from inm.FechaPago), extract(month from ib.FechaPago), ib.FechaPago, 
    d.codigo
    order by Recaudacion desc""")
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
            group by extract (year from ib.fechaPago), extract(month from ib.fechaPago)""", fecha1=fecha1, fecha2=fecha2)
    result = CURSOR.fetchall()
    col_names = [row[0] for row in CURSOR.description]
    CURSOR.close()
    return template("Views/Tablas", col_names=col_names, rows=result)

@get('/consulta7') # o @route('/consulta7')
def consulta7():
    return template("Views/consulta7Form")

@post('/consulta7') # o @route('/consulta7', method='POST')
def do_consulta7():
    dniRazon= request.forms.get('dniRazon')
    CONNECTION = cx_Oracle.connect(USER, PASS)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute("""select  ib.saldo SaldoIIBB, ib.fechaPago FechaPagoIIBB, 
        a.saldo SaldoAutos, a.fechaPago FechaPagoAutos, t.saldo SaldoTasas, t.fechaPago FechaPagoTasas, 
        s.saldo SaldoSellos, s.fechaPago FechaPagoSellos, 
        inm.saldo SaldoInmuebles, inm.fechaPago FechaPagoInmuebles
        from cuentaCorrienteImpBruto ib, cuentaCorrienteImpAuto a, cuentaCorrienteTasa t,cuentaCorrienteImpSello s, cuentaCorrienteImpInmueble inm
        where ((ib.nroCuenta = (select cc.nrocuenta from cuentacorriente cc where cc.dni = :dniRazon)
        and a.nroCuenta = (select cc.nrocuenta from cuentacorriente cc where cc.dni = :dniRazon)
        and t.nroCuenta = (select cc.nrocuenta from cuentacorriente cc where cc.dni = :dniRazon)
        and s.nroCuenta = (select cc.nrocuenta from cuentacorriente cc where cc.dni = :dniRazon)
        and inm.nroCuenta = (select cc.nrocuenta from cuentacorriente cc where cc.dni = :dniRazon)
        and ib.fechaPago = (select max(fechaPago) from cuentaCorrienteImpBruto ib where ib.nrocuenta = (select cc.nrocuenta from cuentacorriente cc where cc.dni = :dniRazon))
        and a.fechaPago = (select max(fechaPago) from cuentacorrienteimpauto a where a.nrocuenta = (select cc.nrocuenta from cuentacorriente cc where cc.dni = :dniRazon))
        and t.fechaPago = (select max(fechaPago) from cuentacorrientetasa t where t.nrocuenta = (select cc.nrocuenta from cuentacorriente cc where cc.dni = :dniRazon))
        and s.fechaPago = (select max(fechaPago) from cuentacorrienteimpsello s where s.nrocuenta = (select cc.nrocuenta from cuentacorriente cc where cc.dni = :dniRazon))
        and inm.fechaPago = (select max(fechaPago) from cuentacorrienteimpinmueble inm where inm.nrocuenta = (select cc.nrocuenta from cuentacorriente cc where cc.dni = :dniRazon)))  
        or
        (ib.nroCuenta = (select cc.nrocuenta from cuentacorriente cc where cc.razonsocial = :dniRazon)
        and a.nroCuenta = (select cc.nrocuenta from cuentacorriente cc where cc.razonsocial = :dniRazon)
        and t.nroCuenta = (select cc.nrocuenta from cuentacorriente cc where cc.razonsocial = :dniRazon)
        and s.nroCuenta = (select cc.nrocuenta from cuentacorriente cc where cc.razonsocial = :dniRazon)
        and inm.nroCuenta = (select cc.nrocuenta from cuentacorriente cc where cc.razonsocial = :dniRazon))
        and ib.fechaPago = (select max(fechaPago) from cuentaCorrienteImpBruto ib where ib.nrocuenta = (select cc.nrocuenta from cuentacorriente cc where cc.razonsocial = :dniRazon))
        and a.fechaPago = (select max(fechaPago) from cuentacorrienteimpauto a where a.nrocuenta = (select cc.nrocuenta from cuentacorriente cc where cc.razonsocial = :dniRazon))
        and t.fechaPago = (select max(fechaPago) from cuentacorrientetasa t where t.nrocuenta = (select cc.nrocuenta from cuentacorriente cc where cc.razonsocial = :dniRazon))
        and s.fechaPago = (select max(fechaPago) from cuentacorrienteimpsello s where s.nrocuenta = (select cc.nrocuenta from cuentacorriente cc where cc.razonsocial = :dniRazon))
        and inm.fechaPago = (select max(fechaPago) from cuentacorrienteimpinmueble inm where inm.nrocuenta = (select cc.nrocuenta from cuentacorriente cc where cc.razonsocial = :dniRazon)))"""
                   , dniRazon=dniRazon)
    result = CURSOR.fetchall()
    col_names = [row[0] for row in CURSOR.description]
    CURSOR.close()
    return template("Views/Tablas", col_names=col_names, rows=result)

@get('/consulta8') # o @route('/consulta8')
def consulta8():
    return template("Views/consulta8Form")

@post('/consulta8') # o @route('/consulta8', method='POST')
def do_consulta8():
    delegacion= request.forms.get('delegacion')
    mes = request.forms.get('mes')
    anio = request.forms.get('anio')
    CONNECTION = cx_Oracle.connect(USER, PASS)
    CURSOR = CONNECTION.cursor()
    CURSOR.execute("""select d.codigo, d.ciudad, ib.codigo, a.codigo, t.codigo, s.codigo, inm.codigo, 
        count(ib.fechaPago), count(a.fechaPago), count(t.fechaPago), count(s.fechaPago), 
        count(inm.fechaPago)
        from cuentaCorriente cc
        inner join cuentaCorrienteImpBruto ib on ib.nroCuenta = cc.nroCuenta
        inner join cuentaCorrienteImpAuto a on a.nroCuenta = cc.nroCuenta
        inner join cuentaCorrienteTasas t on t.nroCuenta = cc.nroCuenta
        inner join cuentaCorrienteImpSellos s on s.nroCuenta = cc.nroCuenta
        inner join cuentaCorrienteImpInmuebles inm on inm.nroCuenta = cc.nroCuenta
        inner join fisicas f on f.DNI/Razon_Social = cc.DNI/Razon_Social
        inner join juridicas j on j.DNI/Razon_Social = cc.DNI/Razon_Social
        inner join Delegaciones d on d.codigo = f.codigo
        inner join Delegaciones d on d.codigo = j.codigo
        where ( (extract(year from ib.fechaPago) = :anio)
	    and (extract(year from ib.fechaPago) = extract(year from a.fechaPago))
	    and (extract(year from ib.fechaPago) = extract(year from t.fechaPago))
	    and (extract(year from ib.fechaPago) = extract(year from s.fechaPago))
	    and (extract(year from ib.fechaPago) = extract(year from inm.fechaPago))
    	and (extract(month from ib.fechaPago) = :mes)
	    and (extract(month from ib.fechaPago) = extract(month from a.fechaPago))
	    and (extract(month from ib.fechaPago) = extract(month from t.fechaPago))
	    and (extract(month from ib.fechaPago) = extract(month from s.fechaPago))
	    and (extract(month from ib.fechaPago) = extract(month from inm.fechaPago))
	    and (d.codigo = :delegacion) )
        group by :delegacion, :anio, :mes""", delegacion=delegacion, anio=anio, mes=mes)
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
