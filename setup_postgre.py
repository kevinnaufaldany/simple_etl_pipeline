import psycopg2
from psycopg2 import sql

def create_database():
    """Script untuk membuat database PostgreSQL dan grant privileges."""
    DB_USER_ADMIN = 'postgres'
    DB_PASSWORD_ADMIN = 'kevins.kom'
    DB_USER_DEV = 'developer'
    DB_PASSWORD_DEV = 'developer' # sesuaikan dengan password yang anda
    DB_HOST = 'localhost'
    DB_PORT = 5432
    DB_NAME = 'db_fashion'
    
    try:
        conn = psycopg2.connect(
            user=DB_USER_ADMIN,
            password=DB_PASSWORD_ADMIN,
            host=DB_HOST,
            port=DB_PORT,
            database='postgres'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        print(f"Connected ke PostgreSQL sebagai {DB_USER_ADMIN}")
        
        cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [DB_NAME])
        exists = cursor.fetchone()
        
        if exists:
            print(f"Database '{DB_NAME}' sudah ada.")
        else:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
            print(f"Database '{DB_NAME}' berhasil dibuat!")
        
        try:
            cursor.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s").format(sql.Identifier(DB_USER_DEV)), [DB_PASSWORD_DEV])
            print(f"User '{DB_USER_DEV}' berhasil dibuat!")
        except psycopg2.errors.DuplicateObject:
            print(f"User '{DB_USER_DEV}' sudah ada, skip create.")
        
        cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(
            sql.Identifier(DB_NAME),
            sql.Identifier(DB_USER_DEV)
        ))
        print(f"Grant privileges ke user '{DB_USER_DEV}' untuk database '{DB_NAME}'")
        
        cursor.close()
        conn.close()
        
        conn2 = psycopg2.connect(
            user=DB_USER_ADMIN,
            password=DB_PASSWORD_ADMIN,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        conn2.autocommit = True
        cursor2 = conn2.cursor()
        
        cursor2.execute(sql.SQL("GRANT ALL ON SCHEMA public TO {}").format(sql.Identifier(DB_USER_DEV)))
        cursor2.execute(sql.SQL("GRANT CREATE ON SCHEMA public TO {}").format(sql.Identifier(DB_USER_DEV)))
        print(f"Grant schema privileges ke user '{DB_USER_DEV}'")
        
        cursor2.close()
        conn2.close()
        
        print("\nSetup database berhasil!")
        print(f"Database: {DB_NAME}")
        print(f"User: {DB_USER_DEV}")
        print(f"Host: {DB_HOST}:{DB_PORT}")
        
    except psycopg2.OperationalError as e:
        print(f"Error: Tidak bisa connect ke PostgreSQL")
        print(f"Pastikan PostgreSQL sudah running di {DB_HOST}:{DB_PORT}")
        print(f"Error detail: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Setup database PostgreSQL untuk Fashion Scraper...")
    print("==============================================\n")
    create_database()
