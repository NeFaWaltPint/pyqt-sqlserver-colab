# -*- coding: utf-8 -*-

import configparser
import urllib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Leer el archivo de configuración
config = configparser.ConfigParser()
config.read('db_conf.ini')

db_config = config['SQLSERVER']
dialect = db_config['dialect']
#username = db_config['username']
#password = db_config['password']
host = db_config['host']
port = db_config['port']
database = db_config['database']
driver = db_config['driver']
trusted_connection = db_config.get('trusted_connection', 'no')

connection_str = (
    f"DRIVER={driver};"
    f"SERVER={host};"
    f"DATABASE={database};"
    f"Trusted_Connection={trusted_connection};"
)

params = urllib.parse.quote_plus(connection_str)
Engine = create_engine(f"{dialect}:///?odbc_connect={params}")

## Codificar el driver para la URL ODBC
#params = urllib.parse.quote_plus(
#    f"DRIVER={{{driver}}};"
#    f"SERVER={host},{port};"
#    f"DATABASE={database};"
#    f"UID={username};"
#    f"PWD={password}"
#)
#
## Crear el engine de SQLAlchemy
#connection_url = f"{dialect}:///?odbc_connect={params}"
#Engine = create_engine(connection_url)

# Crear una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)