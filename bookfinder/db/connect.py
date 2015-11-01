from contextlib import closing
import psycopg2

from bookfinder import app


def connect_db():
    return psycopg2.connect(
        database=app.config['DATABASE_NAME'],
        user=app.config['DATABASE_USERNAME'],
        password=app.config['DATABASE_PASSWORD'],
        host=app.config['DATABASE_URL'],
        port=app.config['DATABASE_PORT'],
    )


def init_db():
    app.logger.debug('Creating initial schema...')
    create_schema_sql = (
        '''
            create table Book(
                id int primary key,
                title varchar(50),
                ISBN varchar(13),
                author varchar(100)
            );
            create table PurchaseChoice(
                id int primary key,
                price varchar(10),
                type varchar(20),
                isRental boolean,
                link varchar(100),
                seller varchar(30),
                book_id int,
                foreign key (book_id) references Book(id)
            );
            create table BookfinderUser(
                id int primary key,
                username varchar(20),
                email varchar(50),
                password varchar(50)
            );
        '''
    )

    execute_sql_query(create_schema_sql)
    app.logger.debug('Table "Book" created')
    app.logger.debug('Table "PurchaseChoice" created')
    app.logger.debug('Table "BookfinderUser" created')


def flush_db():
    '''
    WARNING
    THIS WILL DROP ALL TABLES IN THE TEST DATABASE
    '''
    postgres_tables = execute_sql_query(
        '''
        select tablename from pg_tables where tableowner='{db_user}'
        '''.format(db_user=app.config['DATABASE_USERNAME'])
    )
    drop_table_sql = 'drop table '
    app.logger.debug('Dropping all tables owned by {db_user} user...'.format(
        db_user=app.config['DATABASE_USERNAME'],
    ))
    # append table names owned by postgres
    if postgres_tables:
        drop_table_sql += ','.join([t[0] for t in postgres_tables])
        execute_sql_query(drop_table_sql)
        app.logger.debug(
            'Tables {tables} dropped'.format(tables=str(postgres_tables))
        )
    else:
        app.logger.debug(
            'No tables owned by {db_user} user exist in database'.format(
                db_user=app.config['DATABASE_USERNAME'],
            )
        )


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
