# -*- coding: utf-8 -*-

import argparse
from models.models import Base
from controllers.database import SessionLocal, Engine

def checkCreateDropDB():
    parser = argparse.ArgumentParser(description='Argumentos para crear o eliminar la base de datos')
    parser.add_argument('-c', '--create', action='store_true', help='Crear la base de datos')
    parser.add_argument('-d', '--drop', action='store_true', help='Eliminar la base de datos')
    args = parser.parse_args()

    if args.create:
        print("Creando la base de datos...")
        Base.metadata.create_all(Engine)
        print("Base de datos creada exitosamente.")
    elif args.drop:
        print("Eliminando la base de datos...")
        Base.metadata.drop_all(Engine)
        print("Base de datos eliminada exitosamente.")
