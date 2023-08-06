def insert_data(self, table_name:str, data_dict:dict, allow_duplicates:bool=True, commit:bool=True):
    """
    Insère des données dans une table.

    :param table_name: Nom de la table cible.
    :type table_name: str
    :param data_dict: Dictionnaire contenant les colonnes et leurs valeurs.
    :type data_dict: dict
    :param allow_duplicates: Indique si les doublons sont autorisés (par défaut: True).
    :type allow_duplicates: bool
    :param commit: Indique si la transaction doit être validée immédiatement (par défaut: False).
    :type commit: bool

    :return: None
    :rtype: None
    """

    columns = ", ".join(data_dict.keys())
    #placeholders = ":" + ", :".join(data_dict.keys()) #[e if e is not None else "NULL" for e in data_dict.values()])
    placeholders = ", ".join(["?" for e in data_dict.keys()]) #[e if e is not None else "NULL" for e in data_dict.values()])

    if allow_duplicates:
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    else:
        query = f"INSERT OR IGNORE INTO {table_name} ({columns}) VALUES ({placeholders})"
        # query = f"INSERT OR REPLACE INTO {table_name} ({columns}) VALUES ({placeholders})"
    #endIf


    self.add_db(query=query, datas=list(data_dict.values()), commit=commit)
#endIl
