import pandas as pd
from typing import List


def transformation(tables: List[pd.DataFrame]) -> pd.DataFrame:
	time_dimension = tables[0]
	courier_dimension = tables[1]
	office_dimension = tables[2]
	services = tables[3]
	service_statuses = tables[4]
	clientes_usuarioaquitoy_table = tables[5]

	service_statuses["hora_str"] = service_statuses["hora"].astype(str)

	service_statuses["datetime"] = pd.to_datetime(
		service_statuses["fecha"]
	) + pd.to_timedelta(service_statuses["hora_str"])

	latest_status = service_statuses.sort_values("datetime").drop_duplicates(
		"servicio_id", keep="last"
	)

	latest_status = latest_status.rename(
		columns={
					"id": "status_record_id",
					"estado_id": "status_id",
					"servicio_id": "service_id"
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

	services["hora_solicitud_str"] = services["hora_solicitud"].astype(str)
	services["request_time"] = pd.to_datetime(
		services["fecha_solicitud"]
	) + pd.to_timedelta(services["hora_solicitud_str"])
	services["request_time"] = services["request_time"].dt.floor("h")

	time_dimension["date"] = pd.to_datetime(time_dimension["date"])
	time_mapping = dict(zip(time_dimension["date"], time_dimension["time_id"]))

	services["time_id"] = services["request_time"].map(time_mapping)

	service_fact = services[
			[
					"service_id",
					"customer_id",
					"courier_id",
					"status_id",
					"usuario_id",
					"time_id",
			]
	]

	service_fact = (
		service_fact.groupby(["time_id", "customer_id", "courier_id", "usuario_id"])
		.agg(total_services=pd.NamedAgg(column="service_id", aggfunc="count"))
		.reset_index()
	)

	service_fact = service_fact.merge(courier_dimension, left_on="courier_id", right_on="original_courier_id", how="inner")
	service_fact.drop(columns=["courier_id_x", "courier_id_y", "courier_city"], inplace=True)
	service_fact.rename(columns={ "original_courier_id": "courier_id" }, inplace=True)

	service_fact = service_fact.merge(clientes_usuarioaquitoy_table[["id", "sede_id"]], left_on="usuario_id", right_on="id", how="inner")
	service_fact.drop(columns=["usuario_id", "id"], inplace=True)

	service_fact = service_fact.merge(office_dimension[["office_id", "original_office_id"]], left_on="sede_id", right_on="original_office_id", how="inner")
	service_fact.drop(columns=["sede_id", "original_office_id"], inplace=True)
	service_fact.reset_index(inplace=True)

	service_fact = service_fact.rename(columns={ "index": "service_hour_id" })
	service_fact.set_index("service_hour_id", inplace=True)

	return service_fact
