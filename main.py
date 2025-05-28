# -*- coding: utf-8 -*-

import argparse
from controllers.create_drop_db import checkCreateDropDB
from controllers.database import SessionLocal, Engine
from sqlalchemy import text

from models.models import Base

def main():

    checkCreateDropDB()
    
    # Crear una sesión
    session = SessionLocal()

    try:
        result = session.execute(text("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
        """))
        for row in result:
            print(f" - {row[0]}")
    except Exception as e:
        print(f"Ups! Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()