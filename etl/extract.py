from typing import List, Iterator

import pandas as pd
from pandas import DataFrame
from sqlalchemy.engine import Engine

import constants

def extract(tables: list, connection: Engine) -> list[DataFrame | Iterator[DataFrame]]:
    """
    Extracts the specified tables from the database and converts them into DataFrames.

    :param tables: The tables to extract.
    :param connection: The connection to the database.
    :return: A list of tables in DF format.
    """
    dataframes = []
    for table in tables:
        df = pd.read_sql_table(table, connection)
        dataframes.append(df)
    return dataframes

def extract_courier(connection: Engine):
    """
    Extracts the tables required for the courier dimension.

    :param connection: The connection of the database.
    :return: pandas.DataFrame.
    """
    dim_courier = pd.read_sql_table(constants.COURIER_TABLE, connection)
    dim_city = pd.read_sql_table(constants.CITY_TABLE, connection)
    return [dim_courier, dim_city]

def extract_customer(connection: Engine):
    """
    Extracts the tables required for the customer dimension.

    :param connection: The connection of the database.
    :return: pandas.DataFrame.
    """
    dim_customer = pd.read_sql_table(constants.CUSTOMER_TABLE, connection)
    dim_city = pd.read_sql_table(constants.CITY_TABLE, connection)
    return [dim_customer, dim_city]

def extract_office(connection: Engine):
    """
    Extracts the tables required for the office dimension.

    :param connection: The connection of the database.
    :return: pandas.DataFrame.
    """
    dim_office = pd.read_sql_table(constants.OFFICE_TABLE, connection)
    dim_city = pd.read_sql_table(constants.CITY_TABLE, connection)
    return [dim_office, dim_city]

def extract_service_status(connection: Engine):
    """
    Extracts the tables required for the service status dimension.

    :param connection: The connection of the database.
    :return: pandas.DataFrame.
    """
    dim_service_status = pd.read_sql_table(constants.SERVICE_STATUS_TABLE, connection)
    return dim_service_status

def extract_time(connection: Engine):
    """
    Extracts the tables required for the time dimension.

    :param connection: The connection of the database.
    :return: pandas.DataFrame.
    """
    dim_time = pd.read_sql(constants.QUERY_TIME_DIMENSION, connection)
    return dim_time

def extract_update(connection: Engine):
    """
    Extracts the tables required for the update dimension.

    :param connection: The connection of the database.
    :return: pandas.DataFrame.
    """
    dim_update = pd.read_sql_table(constants.UPDATES_TABLE, connection)
    return dim_update