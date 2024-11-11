import pandas as pd
from typing import List


def transformation(tables: List[pd.DataFrame]) -> pd.DataFrame:
	time_dimension = tables[0]
	services = tables[1]
	service_statuses = tables[2]

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
			"mensajero_id": "courier_id",
			"origen_id": "origin_office_id",
			"destino_id": "office_id",
		}
	)

	services["courier_id"].isna().sum()
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
			"office_id",
			"total_services_per_day"
		]
	]

	return service_fact
