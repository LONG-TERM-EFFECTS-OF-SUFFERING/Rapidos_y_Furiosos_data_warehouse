import copy
import pandas as pd
import yaml

from sqlalchemy import create_engine

from dimensions import courier, customer, office, service_status, time, update
from data_marts import acummulating_snapshot, services_daily, services_hour, updates

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
	"ciudad",
	"cliente",
	"clientes_mensajeroaquitoy",
	"mensajeria_estado",
	"mensajeria_estadosservicio",
	"mensajeria_novedadesservicio",
	"mensajeria_servicio",
	"mensajeria_tiponovedad",
	"sede",
]

content_required_tables = { }

for name in name_required_tables:
	content_required_tables[name] = pd.read_sql_table(name, OLTP_connection)

# ---------------------------------------------------------------------------- #
#                                TRANSFORMATION                                #
# ---------------------------------------------------------------------------- #

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

def create_dimensions():
	for i, dimension_name in enumerate(dimension_names):
		dimension_transformation_functions[i](dimension_related_tables[i]).to_sql(
			dimension_name, OLAP_connection, if_exists="replace", index=True
		)

def load_dimensions():
	for name in dimension_names:
		dimension_contents[name] = pd.read_sql_table(name, OLAP_connection)

# -------------------------------- DATA MARTS -------------------------------- #

fact_table_names = [
	"ACUMMULATING_SNAPSHOTFACT_TABLE",
	"SERVICES_HOUR_FACT_TABLE",
	"SERVICES_DAILY_FACT_TABLE",
	"UPDATES_FACT_TABLE",
]

data_marts_transformation_functions = [
	acummulating_snapshot.transformation,
	services_hour.transformation,
	services_daily.transformation,
	updates.transformation
]

fact_table_contents = { }

def create_data_marts():
	data_marts_related_tables = [
		[dimension_contents["TIME_DIMENSION"], content_required_tables["mensajeria_estado"], content_required_tables["mensajeria_estadosservicio"]],
		[dimension_contents["TIME_DIMENSION"], content_required_tables["mensajeria_servicio"], content_required_tables["mensajeria_estadosservicio"]],
		[dimension_contents["TIME_DIMENSION"], content_required_tables["mensajeria_servicio"], content_required_tables["mensajeria_estadosservicio"]],
		[dimension_contents["TIME_DIMENSION"], content_required_tables["mensajeria_novedadesservicio"]],
	]

	for i, fact_table_name in enumerate(fact_table_names):
		related_tables_copy = copy.deepcopy(data_marts_related_tables[i])
		fact_table_contents[fact_table_name] = data_marts_transformation_functions[i](related_tables_copy)
		fact_table_contents[fact_table_name].to_sql(
			fact_table_name, OLAP_connection, if_exists="replace", index=True
		)

# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
	while True:
		menu = ("Welcome to the ETL tool, we have the following options:\n"
				"1. Create and load the dimensions.\n"
				"2. Load the dimensions and create the datamarts.\n"
				"3. Exit.\n"
				"-> ")

		option = int(input(menu))

		match option:
			case 1:
				create_dimensions()
				load_dimensions()
				print("Dimensions created and loaded.")
			case 2:
				load_dimensions()
				create_data_marts()
				print("Dimensions loaded.")
			case 3:
				print("Exiting...")
				break
			case _:
				print("Invalid option selected.")
