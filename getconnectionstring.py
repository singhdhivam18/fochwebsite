import os

def get_connection_string():
    driver = os.environ.get('DB_DRIVER', 'ODBC Driver 17 for SQL SERVER')
    server = os.environ.get('DB_SERVER')
    database = os.environ.get('DB_NAME')
    uid = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')

    return (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={uid};"
        f"PWD={password};"
    )