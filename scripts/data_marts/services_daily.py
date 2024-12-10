import pandas as pd
from typing import List


def transformation(tables: List[pd.DataFrame]) -> pd.DataFrame:
	time_dimension = tables[0]
	courier_dimension = tables[1]
	office_dimension = tables[2]
	services = tables[3]
	service_statuses = tables[4]
	clientes_usuarioaquitoy_table = tables[5]
	customer_dimension = tables[6]

	services = services.dropna(subset=["mensajero_id"])

	services = services[[
		"id",
		"fecha_solicitud",
		"cliente_id",
		"mensajero_id",
		"usuario_id"
	]]

	services = services.rename(
		columns={
				"id": "service_id",
				"fecha_solicitud": "date",
				"cliente_id": "original_customer_id",
				"mensajero_id": "original_courier_id"
		}
	)

	services = services.merge(clientes_usuarioaquitoy_table[["id", "sede_id"]], left_on="usuario_id",
								right_on="id", how="inner")
	services.drop(columns=["usuario_id", "id"], inplace=True)


	services = services.merge(office_dimension[["office_id", "original_office_id"]], left_on="sede_id",
								right_on="original_office_id", how="inner")
	services.drop(columns=["sede_id", "original_office_id"], inplace=True)


	services = pd.merge(services, time_dimension[["time_id", "date"]], on="date", how="inner")
	services.drop(columns=["date"], inplace=True)

	services = (services.groupby(["original_customer_id", "original_courier_id", "time_id", "office_id"])
				.size().reset_index(name="total_services"))

	service_fact = services.merge(customer_dimension[["customer_id", "original_customer_id"]], on="original_customer_id",
									how="inner")
	service_fact.drop(columns=["original_customer_id"], inplace=True)


	service_fact = service_fact.merge(courier_dimension[["courier_id", "original_courier_id"]], on="original_courier_id",
									how="inner")
	service_fact.drop(columns=["original_courier_id"], inplace=True)

	service_fact.reset_index(inplace=True)
	service_fact = service_fact.rename(columns={ "index": "service_daily_id" })
	service_fact.set_index("service_daily_id", inplace=True)

	return service_fact
