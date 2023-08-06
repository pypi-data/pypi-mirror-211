def _execute(conn, query, datas):
    """
    :param sqlite3.connector conn: Connector
    :param str query: Query
    :param list|tuple datas: List of arguments (same number as '?' in the query)

    :returns: cursor of the db
    """

    c = conn.cursor()

    if datas is not None:
        c.execute( query, datas )
    else:
        c.execute( query )
    #endIf

    return c

def execute(self, query:str, datas:list=[], lock:bool=False):
    """
    :param str query: Query
    :param list|tuple datas: List of arguments (same number as '?' in the query)

    :param book lock: enable/disable lock

    :raise ValueError: query not a string
    :raise ValueError: datas is not a list

    :returns: cursor of the db
    """

    if not isinstance(query, str):
        sys.stderr.write(f"query: {query}\n")
        raise ValueError(f"query is expected to be a string, not {type(query)}")
    #endIf
    if not isinstance(datas, list) and not isinstance(datas, tuple):
        sys.stderr.write(f"datas: {datas}\n")
        raise ValueError(f"datas is expected to be a list, not {type(datas)}")
    #endIf

    if lock and self.lock:
        with self.lock:
            return _execute(self.conn, query, datas)
        #EndWith
    else:
        return _execute(self.conn, query, datas)
    #endIf

    return None
#endDef
