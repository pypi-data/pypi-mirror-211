import os
import sys
import sqlite3


class MyDB:
    """Class to create and access with a minimum of efforts to databases sqlite3

    :param str db_path: Path to the database
    :param Lock lock: A lock to avoid concurrential access
    :param sqlite3.connector conn: The connector to the database


    :func:`MydDB.__init__` : The constructor
    :func:`MydDB.commit` : Commit the modifications
    :func:`MydDB.end_conn`) (alias :func:`MydDB.close`) : Disconnect

    :func:`MyDB.execute` : call connector.execute(), with/out lock and datas
    :func:`MyDB.add_db` : Add datas to the DB
    :func:`MyDB.insert_data` : insert datas to the database
    :func:`MyDB.request_db` : Request datas to the db from a query and column names (opt)
"""

    def __init__(self, db_path:str=None, lock_in=None, createIfNotExists:dict=None):
        """
Constructor

:param str db_path: Path of the database
:param Lock lock_in: Lock the database
:param str|list|dict createIfNotExists: Create table (or several tables) if path not exists ; dict : {table1:{col1 : type_sql, col2: type_sql, ...}, ...}

TODO :
------
Authorize usage of type Python or type SQL for createIfNotExists cols

"""
        self.lock=lock_in

        if db_path:
            self.db_path = db_path
        #endIf

        if self.db_path is not None and os.path.exists(self.db_path):
            pass

        elif createIfNotExists is not None:

            try:

                conn = sqlite3.connect(self.db_path)

            except sqlite3.OperationalError:

                os.makedirs(os.path.dirname(self.db_path), exist_ok=True) # exist_ok : ne pas lever d'erreur si existe
                sys.stderr.write(f"! WARNING : path for DATABASE not exist, create a directory:\n{os.path.dirname(self.db_path)}\n")

            finally:

                conn = sqlite3.connect(self.db_path)

            #endTry

            sys.stderr.write(f"! WARNING : path for DATABASE not exist, create a database:\n{self.db_path}\n")
            cursor = conn.cursor()

            if isinstance(createIfNotExists, bool) and createIfNotExists:

                conn.commit()
                conn.close()
                return

            elif isinstance(createIfNotExists, str):
                createIfNotExists = [createIfNotExists,]
            #endIf

            if isinstance(createIfNotExists, list) or isinstance(createIfNotExists, tuple):
                createIfNotExists = {e:{"useless_col":"INTEGER"} for e in createIfNotExists}
            #endIf

            for elt, cols in createIfNotExists.items():

                slist_cols = ",".join(
                    [f"{k}  {v}" for k, v in cols.items()]
                )
                query = f'CREATE TABLE {elt} ({slist_cols});'

                cursor.execute(query)

                sys.stderr.write(f"! Added table: {elt} with columns: {', '.join(cols.keys())}\n")
            #endFor

            conn.commit()
            conn.close()

            sys.stderr.write(f"! END WARNING : database is created\n")

        else:

            raise ValueError(f"path for DATABASE not exist: {self.db_path}")

        #endIf

        self.conn = sqlite3.connect(f"{self.db_path}")

    #endDef

    from ._request_db import request_db
    from ._add_db import add_db
    from ._insert_data import insert_data
    from ._execute import execute

    def commit(self):
        with self.lock:
            self.conn.commit()
        #endWith

    def end_conn(self):
        if self.lock:
            with self.lock:
                self.conn.close()
            #endWith
        else:
            with self.lock:
                self.conn.close()
            #endWith
        #enddIf
    #endDef

    def close(self):
        return self.end_conn()
    #endDef
#endClass

