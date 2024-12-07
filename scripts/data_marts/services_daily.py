import pandas as pd
from typing import List


def transformation(tables: List[pd.DataFrame]) -> pd.DataFrame:
	time_dimension = tables[0]
	courier_dimension = tables[1]
	office_dimension = tables[2]
	services = tables[3]
	service_statuses = tables[4]
	clientes_usuarioaquitoy_table = tables[5]

	services["fecha_solicitud"] = services["fecha_solicitud"].dt.floor("d").dt.tz_localize(None)
	time_dimension["date"] = time_dimension["date"].dt.floor("d").dt.tz_localize(None)

	service_statuses["fecha"] = pd.to_datetime(service_statuses["fecha"])
	latest_status = service_statuses.sort_values("fecha").drop_duplicates(
		"servicio_id", keep="last"
	)

	latest_status = latest_status.rename(
		columns={
			"id": "status_record_id",
			"estado_id": "status_id",
			"servicio_id": "service_id",
		}
	)

	services = services.rename(
			columns={
					"id": "service_id",
					"cliente_id": "customer_id",
					"mensajero_id": "courier_id"
			}
	)

	services = services.dropna(subset=["courier_id"])

	services = services.merge(
			latest_status[["service_id", "status_id"]], on="service_id", how="left"
		)

	request_date = pd.to_datetime(time_dimension["date"]).dt.normalize()

	# Mapping
	date_mapping = dict(zip(request_date, time_dimension["time_id"]))
	services["fecha_solicitud"] = pd.to_datetime(services["fecha_solicitud"]).dt.normalize()
	services["time_id"] = services["fecha_solicitud"].map(date_mapping)

	services = services.dropna(subset=["time_id"])
	services = services.drop_duplicates(subset=["service_id"], keep="last")
	services["total_services_per_day"] = services.groupby(["courier_id", "customer_id", "time_id"])[
		"time_id"].transform("count")

	services = services.drop_duplicates(subset=["courier_id", "customer_id", "time_id"], keep="first")

	service_fact = services[
		[
			"time_id",
			"customer_id",
			"courier_id",
			"total_services_per_day",
			"usuario_id"
		]
	]

	service_fact = service_fact.merge(courier_dimension, left_on="courier_id", right_on="original_courier_id", how="inner")
	service_fact.drop(columns=["courier_id_x", "courier_id_y", "courier_city"], inplace=True)
	service_fact.rename(columns={ "original_courier_id": "courier_id" }, inplace=True)

	service_fact = service_fact.merge(clientes_usuarioaquitoy_table[["id", "sede_id"]], left_on="usuario_id", right_on="id", how="inner")
	service_fact.drop(columns=["usuario_id", "id"], inplace=True)

	service_fact = service_fact.merge(office_dimension[["office_id", "original_office_id"]], left_on="sede_id", right_on="original_office_id", how="inner")
	service_fact.drop(columns=["sede_id", "original_office_id"], inplace=True)

	service_fact.reset_index(inplace=True)
	service_fact = service_fact.rename(columns={ "index": "service_daily_id" })
	service_fact.set_index("service_daily_id", inplace=True)

	return service_fact
