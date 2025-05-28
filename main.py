# -*- coding: utf-8 -*-

from controllers.database import SessionLocal
from sqlalchemy import text
def main():
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
    finally:
        session.close()

if __name__ == "__main__":
    main()