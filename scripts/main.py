import pandas as pd
import yaml
from sqlalchemy import create_engine

from dimensions import courier, customer, office, service_status, time, update
from data_marts import updates

# ---------------------------------------------------------------------------- #
#                              DATABASE CONNECTION                             #
# ---------------------------------------------------------------------------- #

with open("./config.yml", "r") as file:
	config = yaml.safe_load(file)
	config_OLTP = config["OLTP"]
	config_OLAP = config["OLAP"]


url_OLTP = (f"{config_OLTP['drivername']}://{config_OLTP['user']}:{config_OLTP['password']}"
			f"@{config_OLTP['host']}:{config_OLTP['port']}/{config_OLTP['database_name']}")

url_OLAP = (f"{config_OLAP['drivername']}://{config_OLAP['user']}:{config_OLAP['password']}"
			f"@{config_OLAP['host']}:{config_OLAP['port']}/{config_OLAP['database_name']}")

OLTP_connection = create_engine(url_OLTP)
OLAP_connection = create_engine(url_OLAP)

# ---------------------------------------------------------------------------- #
#                                  EXTRACTION                                  #
# ---------------------------------------------------------------------------- #

name_required_tables = [
	"clientes_mensajeroaquitoy",
	"ciudad",
	"cliente",
	"sede",
	"mensajeria_estado",
	"mensajeria_tiponovedad",
	"mensajeria_novedadesservicio"
]

content_required_tables = { }

for name in name_required_tables:
	content_required_tables[name] = pd.read_sql_table(name, OLTP_connection)

# ---------------------------------------------------------------------------- #
#                                TRANSFORMATION                                #
# ---------------------------------------------------------------------------- #

# -------------------------------- DIMENSIONS -------------------------------- #

dimension_names = [
	"COURIER_DIMENSION",
	"CUSTOMER_DIMENSION",
	"OFFICE_DIMENSION",
	"SERVICE_STATUS_DIMENSION",
	"TIME_DIMENSION",
	"UPDATE_DIMENSION"
]

dimension_transformation_functions = [
	courier.transformation,
	customer.transformation,
	office.transformation,
	service_status.transformation,
	time.transformation,
	update.transformation
]

dimension_related_tables = [
	[content_required_tables["clientes_mensajeroaquitoy"], content_required_tables["ciudad"]],
	[content_required_tables["cliente"], content_required_tables["ciudad"]],
	[content_required_tables["sede"], content_required_tables["ciudad"]],
	[content_required_tables["mensajeria_estado"]],
	[],
	[content_required_tables["mensajeria_tiponovedad"]],
]

dimension_contents = { }

for i, dimension_name in enumerate(dimension_names):
	dimension_contents[dimension_name] = dimension_transformation_functions[i](dimension_related_tables[i])
	dimension_contents[dimension_name].to_sql(
		dimension_name, OLAP_connection, if_exists="replace", index=True
	)

# -------------------------------- DATA MARTS -------------------------------- #

fact_table_names = [
	# "ACUMMULATING_SNAPSHOTFACT_TABLE",
	# "SERVICES_HOUR_FACT_TABLE",
	# "SERVICES_DAILY_FACT_TABLE",
	# "UPDATESFACT_TABLE",
]

data_marts_transformation_functions = [
	# updates.transformation
]

data_marts_related_tables = [
	# [dimension_contents["TIME_DIMENSION"], content_required_tables["mensajeria_novedadesservicio"]],
]

fact_table_contents = { }

for i, fact_table_name in enumerate(fact_table_names):
	fact_table_contents[fact_table_name] = data_marts_transformation_functions[i](data_marts_related_tables[i])
	fact_table_contents[fact_table_name].to_sql(
		fact_table_name, OLAP_connection, if_exists="replace", index=True
	)