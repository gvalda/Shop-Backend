import os


def get_postgres_uri():
    host = os.environ.get('DB_HOST', 'localhost')
    port = os.environ.get('DB_PORT', 54321)
    password = os.environ.get('DB_PASSWORD', 'abc123')
    user = os.environ.get('DB_USER', 'admin')
    db_name = os.environ.get('DB_NAME', 'db_backend')
    print(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
    return f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
