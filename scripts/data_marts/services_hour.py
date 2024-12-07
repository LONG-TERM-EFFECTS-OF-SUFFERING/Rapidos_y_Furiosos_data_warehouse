import pandas as pd
from typing import List


def transformation(tables: List[pd.DataFrame]) -> pd.DataFrame:
	time_dimension = tables[0]
	services = tables[1]
	service_statuses = tables[2]

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
			"servicio_id": "service_id",
			"origen_id": "origin_office_id",
			"destino_id": "destination_office_id",
		}
	)

	services = services.rename(
		columns={
			"id": "service_id",
			"cliente_id": "customer_id",
			"mensajero_id": "courier_id",
			"origen_id": "origin_office_id",
			"destino_id": "destination_office_id",
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

	services["office_id"] = services["origin_office_id"]
	services = services.drop(columns=["origin_office_id", "destination_office_id"])

	service_fact = services[
		[
			"service_id",
			"customer_id",
			"courier_id",
			"status_id",
			"office_id",
			"time_id",
		]
	]

	service_fact = (
		service_fact.groupby(["time_id", "customer_id", "courier_id", "office_id"])
		.agg(total_services=pd.NamedAgg(column="service_id", aggfunc="count"))
		.reset_index()
	)

	service_fact.reset_index(inplace=True)
	service_fact = service_fact.rename(columns={ "index": "service_hour_id" })
	service_fact.set_index("service_hour_id", inplace=True)

	return service_fact
