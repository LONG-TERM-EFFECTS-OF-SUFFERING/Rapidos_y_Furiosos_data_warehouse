import yaml
from sqlalchemy import create_engine, text


dimension_tables = [
	"COURIER_DIMENSION",
	"CUSTOMER_DIMENSION",
	"OFFICE_DIMENSION",
	"SERVICE_STATUS_DIMENSION",
	"TIME_DIMENSION",
	"UPDATE_DIMENSION"
]

fact_tables = [
	"ACUMMULATING_SNAPSHOT_FACT_TABLE",
	"SERVICE_DAILY_FACT_TABLE",
	"SERVICE_HOUR_FACT_TABLE",
	"UPDATES_FACT_TABLE"
]

def create_relations(engine):
	def add_primary_key_dimension_table(dimension_table):
		with engine.connect() as connection:
			with connection.begin():
				name_without_dimension = dimension_table.replace("_DIMENSION", "").lower()
				query = text(f"""
				ALTER TABLE "{dimension_table}"
				ADD CONSTRAINT pk_{name_without_dimension}_dimension PRIMARY KEY ({name_without_dimension}_id);
				""")
				connection.execute(query)

	def add_primary_key_fact_table(fact_table):
		with engine.connect() as connection:
			with connection.begin():
				name_without_fact_table = fact_table.replace("_FACT_TABLE", "").lower()
				query = text(f"""
				ALTER TABLE "{fact_table}"
				ADD CONSTRAINT pk_{name_without_fact_table}_fact_table PRIMARY KEY ({name_without_fact_table}_id);
				""")
				connection.execute(query)

	def alter_table(table, query):
		with engine.connect() as connection:
			with connection.begin():
				query = text(f"""
				ALTER TABLE "{table}"
				{query}
				""")
				connection.execute(query)

	for dimension_table in dimension_tables:
		add_primary_key_dimension_table(dimension_table)

	for fact_table in fact_tables:
		add_primary_key_fact_table(fact_table)

	query = """
	ADD FOREIGN KEY (request_time_id) REFERENCES "TIME_DIMENSION"(time_id),
	ADD FOREIGN KEY (assignment_time_id) REFERENCES "TIME_DIMENSION"(time_id),
	ADD FOREIGN KEY (pickup_time_id) REFERENCES "TIME_DIMENSION"(time_id),
	ADD FOREIGN KEY (delivery_time_id) REFERENCES "TIME_DIMENSION"(time_id),
	ADD FOREIGN KEY (closure_time_id) REFERENCES "TIME_DIMENSION"(time_id);
	"""

	alter_table("ACUMMULATING_SNAPSHOT_FACT_TABLE", query)

	query = """
	ADD FOREIGN KEY (time_id) REFERENCES "TIME_DIMENSION"(time_id),
	ADD FOREIGN KEY (customer_id) REFERENCES "CUSTOMER_DIMENSION"(customer_id),
	ADD FOREIGN KEY (courier_id) REFERENCES "COURIER_DIMENSION"(courier_id),
	ADD FOREIGN KEY (office_id) REFERENCES "OFFICE_DIMENSION"(office_id);
	"""

	alter_table("SERVICE_DAILY_FACT_TABLE", query)

	query = """
	ADD FOREIGN KEY (time_id) REFERENCES "TIME_DIMENSION"(time_id),
	ADD FOREIGN KEY (customer_id) REFERENCES "CUSTOMER_DIMENSION"(customer_id),
	ADD FOREIGN KEY (courier_id) REFERENCES "COURIER_DIMENSION"(courier_id),
	ADD FOREIGN KEY (office_id) REFERENCES "OFFICE_DIMENSION"(office_id);
	"""

	alter_table("SERVICE_HOUR_FACT_TABLE", query)

	query = """
	ADD FOREIGN KEY (update_id) REFERENCES "COURIER_DIMENSION"(courier_id),
	ADD FOREIGN KEY (time_id) REFERENCES "TIME_DIMENSION"(time_id);
	"""

	alter_table("UPDATES_FACT_TABLE", query)

if __name__ == "__main__":
	with open("./config.yml", "r") as file:
		config = yaml.safe_load(file)
		config_OLAP = config["OLAP"]

	url_OLAP = (f"{config_OLAP['drivername']}://{config_OLAP['user']}:{config_OLAP['password']}"
			f"@{config_OLAP['host']}:{config_OLAP['port']}/{config_OLAP['database_name']}")

	OLAP_connection = create_engine(url_OLAP)

	create_relations(OLAP_connection)