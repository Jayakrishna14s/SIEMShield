import psycopg2 # type: ignore
 
DB_HOST = "postgres"
DB_NAME = "SIEMSHIELD"
DB_USER = "Jayakrishna"
DB_PASSWORD = "root"
DB_PORT = "5432"

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    return conn

