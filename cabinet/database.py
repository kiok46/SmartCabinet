#!/usr/bin/python
# coding=utf-8

'''
This file is used to read from database.
'''

hostname = '149.202.206.59'
port = '5432'
username = 'smartuser'
password = 'smartpass'
database = 'smartcabinet'

# Simple routine to run a query on a database and print the results:

'''
List of Available Tables in the Database.

TABEL_LIST = ['config', 'episode', 'event_log', 'event_type', 'gfh',
              'incidence', 'line', 'linedetail', 'maintainance',
              'maintainance_type', 'orderassign', 'patient', 'permission',
              'product', 'role', 'role_r_permission', 'room', 'tag', 'user',
              'user_r_role']


# If you want to access the table content.

def get_tabel_content(connection, table_name) :
    cursor = connection.cursor()
    cursor.execute( "SELECT * FROM {}".format(table_name))

    a = cursor.fetchall()
    for i in a:
        print i
'''


def get_table_list(connection):
    cursor = connection.cursor()
    querry = "SELECT t.rfid, t.created_date, t.enabled, t.line_detail_id, "+ \
             "ld.lot, ld.serialnumber, ld.expiredate, l.quantity, "+\
             "t.providername, o.warehousecode, p.code, p.code_alt, "+\
             "t.providerRef, p.description FROM Tag AS t LEFT JOIN LineDetail "+\
             "AS ld ON ld.line_detail_id = t.line_detail_id LEFT JOIN Line AS "+\
             "l ON l.line_id = ld.line_id LEFT JOIN Product AS p ON "+\
             "p.product_id = l.product_id LEFT JOIN Orderassign AS o ON o.order_id = l.order_id;"

    cursor.execute(querry)
    a = cursor.fetchall()
    list_ = []
    for i in a:
        list_.append(i)
    return list_


if __name__ == '__main__':
    '''
    Boilerplate to test this manually. (Stand alone.)
    '''
    import psycopg2
    myConnection = psycopg2.connect(host=hostname, user=username,
                                    password=password, dbname=database,
                                    port=port )
    print (get_table_list(myConnection))
    myConnection.close()
