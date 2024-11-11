import pandas as pd
from typing import List


def transformation(tables: List[pd.DataFrame]) -> pd.DataFrame:
	time_dimension = tables[0]
	updates = tables[1]

	updates["fecha_novedad"] = updates["fecha_novedad"].dt.floor("min").dt.tz_localize(None)

	updates_fact_table = pd.merge(updates, time_dimension[["date", "time_id"]],
								left_on="fecha_novedad", right_on="date", how="left")

	updates_fact_table.drop(columns=["id", "fecha_novedad", "date", "es_prueba", "mensajero_id"], inplace=True)

	updates_fact_table.rename(
		columns={
			"tipo_novedad_id": "update_id",
			"servicio_id": "service_id",
			"descripcion": "update_description",
		}, inplace=True
	)

	updates_fact_table.reset_index(inplace=True)
	updates_fact_table.rename(columns={ "index": "updates_fact_table_id" }, inplace=True)
	updates_fact_table.set_index("updates_fact_table_id", inplace=True)

	return updates_fact_table
