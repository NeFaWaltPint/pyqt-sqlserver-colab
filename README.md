# pyqt-sqlserver-colab
Un repo para un ejercicio de python con interfaz qt y conexión a bd sql server

## Requisitos
- python 3.13.3
- Ms SQL Server 2022

### Preparación: user y BD para MSSQLSERVER

```cmd
# conectar con privilegiso de usuario windows
sqlcmd -S localhost -E

# dentro de sql server crear usuario
CREATE LOGIN admin2 WITH PASSWORD = '00123';
Go

# crear bd y usarla
CREATE DATABASE BaseDatosPrueba;
USE BaseDatosPrueba;
Go

# agregar el usuario a la bd
CREATE USER admin2 FOR LOGIN admin2;
Go

# dar permisos al usuario y salir
ALTER ROLE db_owner ADD MEMBER admin2;
Go
exit

# inyectar script de creación de tablas, NO ES NECESARIO si ya define los modelos desde `models/models.py`
sqlcmd -S localhost -U pruebausuario -P password -d BaseDatosPrueba -i creacion_tablas_migration_up.sql
```

### Instalar requerimientos en ambiente
Agregar ambiente .Venv (gestionar con vscode) y activarlo, luego instalar los requerimientos
```cmd
pip install -r requirements.txt
```

### Usar PyQT Designer desde Venv
En `.venv\Lib\site-packages\QtDesigner\designer.exe` se encuentra el ejecutable para construir la interfaz de manera _gráfica_.
Desde este se puede exportar el código python de la parte gráfica, guardarlo como `view.py`

#### Variables
Variables de conexión a db en archivo `db_conf.ini`, si no existe crearlo con lo siguiente:
```
[SQLSERVER]
dialect = mssql+pyodbc
username = pruebausuario
password = password
host = localhost
port = 1433
database = BaseDatosPrueba
driver = ODBC Driver 17 for SQL Server
```

## Ejecución desde `main.py`
Para crear o borrar las tablas ya no es necesario inyección de sql si tiene definido el modelo en `models.py`.

```cmd
# Para crear las tablas ejecutar:
python main.py -c

# Para borrar las tabllas ejecutar:
python main.py -d
```

_**Nota:** Si el drop de las tablas da error, puede deberse a una tabla huerfana que ya no coincide en nombre en el modelo actual, hay que entrar manualmente a la bd y borrarla, luego de eso mientras db y modelo se mantengan sincronizados no debe dar problema_ 