import mysql.connector as mysql
import logging

logging.getLogger(__name__)

class DB:
    """
    Base class that implements database connections
    """
    # def __new__(cls, *args, **kwargs):
    #     """ Implement as singleton"""
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super().__new__(cls)
    #     return cls.instance

    def __init__(self,
                 database: str = None,
                 host = None):
        self.conn = mysql.Connect(
            host = host or "0.0.0.0",
            user = "root",
            password = "123456",
            database = database,
            auth_plugin = 'mysql_native_password',
            autocommit = True
        )
        self.curs = self.conn.cursor(buffered = True, dictionary = True)

    def query(self, query: str, results: bool = True):
        """ Execute a query into the selected database."""
        self.curs.execute(query)
        logging.debug(f"SQL: ``{query}`")
        if results:
            return self.curs.fetchall()

    def change_db(self, database: str):
        """ Select the database. Equivalent of `use <DATABASE>`"""
        self.conn.database = database
        logging.debug(f"Changing DB to {database}")

    def select_where(self, table, *columns, **wheres) -> dict or list:
        """
        Select columns from a table by column values, equivalent to a
        SELECT (column1, ...) FROM TABLE WHERE (k1 = v1, k2 = v2)

        One may pass multi = True as a kwargs to get multiple results. Default
        behavior is to return one result
        """
        multi = wheres.pop("multi", None)
        if not columns:
            cols = " * "
        else:
            cols = ", ".join(columns)
        sql = "SELECT " + cols
        sql += " FROM " + table
        if wheres:
            sql += " WHERE "
            for k, v in wheres.items():
                sql += f" {k} = '{v}', "
            sql = sql[:-2] # trim final comma
        print(sql)
        ret = self.query(sql)
        logging.debug(f"SQL: {sql}")
        if multi:
            return ret
        else:
            return ret[0]

    def select_column(self, table, column, multi = True):
        """
        Select all values in a column in a table.
        If multi is False, returns only the first value found
        """
        sql = f"SELECT {column} from {table}"

        logging.debug(f"SQL: {sql}")
        if multi:
            return self.query(sql)
        else:
            return self.query(sql)[0][column]

    def select_all_by_key(self, table, key, value) -> list:
        """
        Select all matches by key, value. Returns a list if multi is True,
        else returns a dictionary.
        """
        sql = f"SELECT * FROM {table} WHERE {key} = '{value}'"
        logging.debug(f"SQL: {sql}")
        return self.query(sql)

    def insert_row(self, table, **kwargs):
        """
        Insert a row into table, using key-value pairings.
        """
        sql = f"INSERT INTO {table} ("
        for key in kwargs.keys():
            sql += f"{key}, "
        sql = sql[:-2] # trim ", "
        sql += ") VALUES ("
        for v in kwargs.values():
            sql += f"'{v}', "
        sql = sql[:-2] # trim ", "
        sql += ")"
        self.query(sql, results = False)
        logging.debug(f"SQL: {sql}")
        return True

    def update_value(self, table, key, new_value, **wheres):
        """
        Update a value, based on key, in the database, with
        wheres being the where clause in the SQL statement.
        """
        sql = f"UPDATE {table} SET {key} = '{new_value}'"
        if wheres:
            sql += "WHERE "
            for k, v in wheres.items():
                f"{k} = '{v}' and "
            sql = sql[:-6] # cleave final 'and '
        print(sql)
        self.query(sql, results = False)
        logging.debug(f"SQL: {sql}")
        return True

    def update_row(self, table, selector, value, **new_values):
        sql = f"UPDATE {table} SET "
        for k, v in new_values.items():
            sql += f" {k} = '{v}', "
        sql = sql[:-2] # remove the trailing comma
        sql += f" WHERE {selector} = '{value}'"

        self.query(sql, results = False)
        logging.debug(f"SQL: {sql}")
        return True

    def get_table_names(self) -> list:
        """
        Get the names of each table, as a list.
        """
        ret = self.query("SHOW TABLES")
        logging.debug("SQL: SHOW TABLES")
        names = []
        for item in ret:
            names.append(list(item.values())[0])
        return names

    def delete_row(self, table, **wheres):
        """
        Delete a row from table, based on wheres
        """

        if not wheres:
            raise Exception("Missing `wheres` kwargs in call to delete_row")
        sql = f"DELETE FROM {table} WHERE "
        for k, v in wheres.items():
            sql += f"{k} = {v}, "
        sql = sql[:2]
        logging.debug(f"SQL: {sql}")


    def select_all(self, table_name):
        sql = f"SELECT * FROM {table_name}"
        ret = self.query(sql)
        logging.debug(f"SQL: {sql}")
        return ret

    def get_columns_names(self, table) -> list:
        sql = f"describe {table}"
        ret = self.query(sql)
        logging.debug(f"SQL: {sql}")
        names = []
        for field in ret:
            names.append(field.get("Field"))
        return names
