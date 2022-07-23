# mysqlconnection.py
# This is the complete configuration of database items. Don't modify it!

"""
SELECT queries will return a list of dictionaries.
INSERT queries will return the auto-generated id of the inserted row.
UPDATE and DELETE queries will return nothing.
If the query goes wrong, it will return 'False'.
"""

import pymysql.cursors

class MySQLConnection:

    def __init__(self, db):
        connection = pymysql.connect(host = 'localhost',
                                    user = 'root',
                                    password = 'root',
                                    db = db,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = True)
        self.connection = connection

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)

                cursor.execute(query, data)

                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
            except Exception as e:
                print("Something went wrong...", e)
                return False
            finally:
                self.connection.close()

def connectToMySQL(db):
    return MySQLConnection(db)