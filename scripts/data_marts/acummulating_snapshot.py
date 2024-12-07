import pandas as pd
from typing import List


def transformation(tables: List[pd.DataFrame]) -> pd.DataFrame:
	time_dimension = tables[0]
	mensajeria_estado = tables[1]
	mensajeria_estadosservicio = tables[2]

	service_statuses = mensajeria_estadosservicio.drop(columns=["foto", "observaciones", "es_prueba", "foto_binary"])

	service_statuses["hora"] = service_statuses["hora"].astype(str)
	service_statuses["date"] = pd.to_datetime(
		service_statuses["fecha"].astype(str) + " " + service_statuses["hora"],
		infer_datetime_format=True,
		errors="coerce"
	)

	service_statuses["date"] = service_statuses["date"].dt.floor("min")

	service_statuses.drop(columns=["fecha", "hora"], inplace=True)

	service_statuses = pd.merge(service_statuses, mensajeria_estado[["id", "nombre"]],
								left_on="estado_id", right_on="id", how="left")

	service_statuses.drop(columns=["estado_id", "id_y"], inplace=True)
	service_statuses.rename(
		columns={
			"id_x": "id",
			"servicio_id": "service_id",
			"nombre": "status"
		}, inplace=True
	)

	acummulating_snapshot_fact_table = service_statuses[["service_id"]].drop_duplicates()

	date_columns = ["request_time_id", "assignment_time_id", "pickup_time_id", "delivery_time_id", "closure_time_id"]
	for col in date_columns:
		acummulating_snapshot_fact_table[col] = pd.NaT

	for _, row in service_statuses.iterrows():
		service_id = row["service_id"]
		status = row["status"]
		date = row["date"]

		if status == "Iniciado":
			acummulating_snapshot_fact_table.loc[acummulating_snapshot_fact_table["service_id"] == service_id,
													"request_time_id"] = date
		elif status == "Con mensajero Asignado":
			acummulating_snapshot_fact_table.loc[acummulating_snapshot_fact_table["service_id"] == service_id,
													"assignment_time_id"] = date
		elif status == "Recogido por mensajero":
			acummulating_snapshot_fact_table.loc[acummulating_snapshot_fact_table["service_id"] == service_id,
													"pickup_time_id"] = date
		elif status == "Entregado en destino":
			acummulating_snapshot_fact_table.loc[acummulating_snapshot_fact_table["service_id"] == service_id,
													"delivery_time_id"] = date
		elif status == "Terminado completo":
			acummulating_snapshot_fact_table.loc[acummulating_snapshot_fact_table["service_id"] == service_id,
													"closure_time_id"] = date

	def substract_series(series_1, series_2):
		result = series_1 - series_2
		result[pd.isna(series_1) | pd.isna(series_2)] = pd.Timedelta(0)
		return result

	acummulating_snapshot_fact_table["request_assignment_time"] = substract_series(acummulating_snapshot_fact_table["assignment_time_id"], acummulating_snapshot_fact_table["request_time_id"])
	acummulating_snapshot_fact_table["assignment_pickup_time"] = substract_series(acummulating_snapshot_fact_table["pickup_time_id"], acummulating_snapshot_fact_table["assignment_time_id"])
	acummulating_snapshot_fact_table["pickup_delivery_time"] = substract_series(acummulating_snapshot_fact_table["delivery_time_id"], acummulating_snapshot_fact_table["pickup_time_id"])
	acummulating_snapshot_fact_table["delivery_closure_time"] = substract_series(acummulating_snapshot_fact_table["closure_time_id"], acummulating_snapshot_fact_table["delivery_time_id"])

	acummulating_snapshot_fact_table["request_assignment_time"] = acummulating_snapshot_fact_table["request_assignment_time"].dt.total_seconds()
	acummulating_snapshot_fact_table["assignment_pickup_time"] = acummulating_snapshot_fact_table["assignment_pickup_time"].dt.total_seconds()
	acummulating_snapshot_fact_table["pickup_delivery_time"] = acummulating_snapshot_fact_table["pickup_delivery_time"].dt.total_seconds()
	acummulating_snapshot_fact_table["delivery_closure_time"] = acummulating_snapshot_fact_table["delivery_closure_time"].dt.total_seconds()

	time_mapping = dict(zip(time_dimension["date"], time_dimension["time_id"]))

	acummulating_snapshot_fact_table["request_time_id"] = acummulating_snapshot_fact_table["request_time_id"].map(time_mapping)
	acummulating_snapshot_fact_table["assignment_time_id"] = acummulating_snapshot_fact_table["assignment_time_id"].map(time_mapping)
	acummulating_snapshot_fact_table["pickup_time_id"] = acummulating_snapshot_fact_table["pickup_time_id"].map(time_mapping)
	acummulating_snapshot_fact_table["delivery_time_id"] = acummulating_snapshot_fact_table["delivery_time_id"].map(time_mapping)
	acummulating_snapshot_fact_table["closure_time_id"] = acummulating_snapshot_fact_table["closure_time_id"].map(time_mapping)

	acummulating_snapshot_fact_table.reset_index(inplace=True)
	acummulating_snapshot_fact_table.rename(columns={ "index": "acummulating_snapshot_id" }, inplace=True)
	acummulating_snapshot_fact_table.set_index("acummulating_snapshot_id", inplace=True)

	return acummulating_snapshot_fact_table
