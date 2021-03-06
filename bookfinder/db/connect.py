from contextlib import closing
import psycopg2
import psycopg2.extras

from bookfinder import app


def connect_db():
    return psycopg2.connect(
        database=app.config['DATABASE_NAME'],
        user=app.config['DATABASE_USERNAME'],
        password=app.config['DATABASE_PASSWORD'],
        host=app.config['DATABASE_HOST'],
        port=app.config['DATABASE_PORT'],
    )


def init_db():
    app.logger.debug('Creating initial schema...')
    create_schema_sql = (
        '''
            create table Book(
                id serial primary key,
                title varchar(200),
                ISBN varchar(13) unique,
                author varchar(100),
                thumbnail_link varchar(200)
            );
            create table BookfinderUser(
                id serial primary key,
                username varchar(20) unique,
                email varchar(50),
                pw_hash varchar(160)
            );
            create table PurchaseChoice(
                id serial primary key,
                price varchar(10),
                type varchar(20),
                isRental boolean,
                link varchar(100),
                local_seller_id int,
                isLocalSeller boolean,
                remoteSellerName varchar(30),
                book_id int,
                foreign key (book_id) references Book(id),
                foreign key (local_seller_id)
                references BookfinderUser(id)
                on delete cascade
            );
            create table BooksViewed(
                id serial primary key,
                book_id int,
                foreign key (book_id) references Book(id) on delete cascade,
                user_id int,
                foreign key (user_id) references BookfinderUser(id)
                on delete cascade,
                time_added timestamp
            );
        '''
    )

    execute_sql_query(create_schema_sql)
    app.logger.debug('Table "Book" created')
    app.logger.debug('Table "PurchaseChoice" created')
    app.logger.debug('Table "BookfinderUser" created')
    app.logger.debug('Table "BooksViewed" created')


def flush_db():
    '''
    WARNING
    THIS WILL DROP ALL TABLES IN THE TEST DATABASE
    '''
    postgres_tables = execute_sql_query(
        '''
        select tablename
        from pg_tables
        where
            tableowner='{db_user}'
            and tablename NOT LIKE 'pg_%'
            and tablename NOT LIKE 'sql_%'
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


def execute_sql_query(query, params=None):
    results = []
    with closing(connect_db()) as db:
        cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(query, params)
        try:
            results = cursor.fetchall()
        except psycopg2.ProgrammingError:
            pass
        db.commit()
    return results
