"""Database client."""
from typing import List

from pandas import DataFrame
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.exc import SQLAlchemyError

from clients.log import LOGGER


class Database:
    """Database client."""

    def __init__(self, uri: str, args: dict):
        self.engines = {
            "analytics": create_engine(
                f"{uri}/analytics", connect_args=args, echo=False
            ),
            "hackers_prod": create_engine(
                f"{uri}/hackers_prod", connect_args=args, echo=False
            ),
        }

    def _table(self, table_name: str, database_name) -> Table:
        """
        :param table_name: Name of database table to fetch
        :type table_name: str
        :param database_name: Name of database to connect to.
        :type database_name: str

        :returns: Table
        """
        return Table(
            table_name, MetaData(bind=self.engines[database_name]), autoload=True
        )

    @LOGGER.catch
    def execute_queries(self, queries: dict, database_name="hackers_prod") -> dict:
        """Execute collection of SQL queries.

        :param queries: Map of query names -> SQL queries.
        :type queries: dict
        :param database_name: Name of database to connect to.
        :type database_name: str

        :returns: dict
        """
        results = {}
        for k, v in queries.items():
            query_result = self.engines[database_name].execute(v)
            results[k] = f"{query_result.rowcount} rows affected."
        return results

    @LOGGER.catch
    def execute_query(self, query: str, database_name="hackers_prod"):
        """
        Execute single SQL query.

        :param query: SQL query to run against database.
        :type query: str
        :param database_name: Name of database to connect to.
        :type database_name: str
        """
        try:
            result = self.engines[database_name].execute(query)
            return result
        except SQLAlchemyError as e:
            LOGGER.error(e)
            return f"Failed to execute SQL query {query}: {e}"

    @LOGGER.catch
    def execute_query_from_file(self, sql_file: str, database_name="hackers_prod"):
        """Execute single SQL query.

        :param sql_file: Filepath of SQL query to run.
        :type sql_file: str
        :param database_name: Name of database to connect to.
        :type database_name: str
        """
        try:
            query = open(sql_file, "r").read()
            result = self.engines[database_name].execute(query)
            return result
        except SQLAlchemyError as e:
            LOGGER.error(e)
            return f"Failed to execute SQL {sql_file}: {e}"

    @LOGGER.catch
    def fetch_records(self, query, database_name=None) -> List[str]:
        """
        Fetch all rows via query.

        :param query: SQL query to run against database.
        :type query: str
        :param database_name: Name of database to connect to.
        :type database_name: Optional[str]
        """
        rows = self.engines[database_name].execute(query).fetchall()
        return [row.items() for row in rows]

    @LOGGER.catch
    def fetch_record(self, query: str, database_name=None):
        """
        Fetch a single row; typically used to verify whether a
        record already exists (ie: users).

        :param query: SQL query to run against database.
        :type query: str
        :param database_name: Name of database to connect to.
        :type database_name: Optional[str]
        """
        return self.engines[database_name].execute(query).first()

    def insert_records(
        self, rows: List[dict], table_name=None, database_name=None, replace=False
    ) -> str:
        """
        Insert rows into table.

        :param rows: List of dictionaries to insert where keys are columns.
        :type rows: List[dict]
        :param table_name: Name of database table to fetch.
        :type table_name: str
        :param database_name: Name of database to connect to.
        :type database_name: Optional[str]
        :param replace: Whether or not to truncate table prior to insert.
        :type replace: bool
        """
        try:
            if replace:
                self.engines[database_name].execute(f"TRUNCATE TABLE {table_name}")
            table = self._table(table_name, database_name)
            self.engines[database_name].execute(table.insert(), rows)
            return f"Inserted {len(rows)} into {table.name}."
        except SQLAlchemyError as e:
            LOGGER.error(e)
            raise e

    def insert_dataframe(
        self, df: DataFrame, table_name=None, database_name="analytics", action="append"
    ):
        """
        Insert Pandas DataFrame into SQL table.

        :param df: Tabular data to insert into SQL table.
        :type df: DataFrame
        :param table_name: Name of database table to insert into.
        :type table_name: str
        :param database_name: Name of database to connect to.
        :type database_name: Optional[str]
        :param action: Method of dealing with duplicate rows.
        :type action: str
        """
        df.to_sql(table_name, self.engines[database_name], if_exists=action)
        return df.to_json(orient="records")
