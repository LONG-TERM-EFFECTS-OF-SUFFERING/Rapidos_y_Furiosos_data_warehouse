from typing import List
import pandas as pd


def transformation(tables: List[pd.DataFrame]) -> pd.DataFrame:
	mensajeria_estado_table = tables[0]

	service_status_dimension = mensajeria_estado_table.rename(
		columns={
			"nombre": "status_name",
			"descripcion": "status_description",
		}
	)

	service_status_dimension.drop(columns=["id"], inplace=True)

	service_status_dimension.reset_index(inplace=True)
	service_status_dimension.rename(columns={ "index": "service_status_id" }, inplace=True)
	service_status_dimension.set_index("service_status_id", inplace=True)

	return service_status_dimension
