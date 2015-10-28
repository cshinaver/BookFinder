from contextlib import closing
import psycopg2

from bookfinder import app


def connect_db():
    return psycopg2.connect(
        database=app.config['DATABASE_NAME'],
        user=app.config['DATABASE_USERNAME'],
        password=app.config['DATABASE_PASSWORD'],
        host=app.config['DATABASE_URL'],
    )


def init_db():
    app.logger.debug('Creating initial schema...')
    create_schema_sql = (
        '''
            create table book(name varchar(30), level int)
        '''
    )

    execute_sql_query(create_schema_sql)
    app.logger.debug('Table "book" created')


def flush_db():
    '''
    WARNING
    THIS WILL DROP ALL TABLES IN THE TEST DATABASE
    '''
    postgres_tables = execute_sql_query(
        '''
        select tablename from pg_tables where tableowner='postgres'
        '''
    )
    drop_table_sql = 'drop table '
    app.logger.debug('Dropping all tables owned by postgres user...')
    # append table names owned by postgres
    if postgres_tables:
        drop_table_sql += ','.join([t[0] for t in postgres_tables])
        execute_sql_query(drop_table_sql)
        app.logger.debug(
            'Tables {tables} dropped'.format(tables=str(postgres_tables))
        )
    else:
        app.logger.debug('No tables owned by postgres user exist in database')


def execute_sql_query(query):
    results = []
    with closing(connect_db()) as db:
        cursor = db.cursor()
        cursor.execute(query)
        try:
            results = cursor.fetchall()
        except psycopg2.ProgrammingError:
            pass
        db.commit()
    return results
