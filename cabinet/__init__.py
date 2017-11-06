from cabinet.database import *

database_content = []
'''
database content holds the data extracted from the database.
to access it use.

>>> global database content.

'''

def db_content():
    global database_content
    #database_content = database_content*3
    return database_content


def refresh_content():
    get_database_tables()
    db_content()


def get_database_tables():
    '''
    Extracts data from the database.
    '''
    import psycopg2
    myConnection = psycopg2.connect(host=hostname, user=username,
                                    password=password, dbname=database,
                                    port=port )
    global database_content
    database_content = get_table_list(myConnection)
    myConnection.close()

#get_database_tables()
