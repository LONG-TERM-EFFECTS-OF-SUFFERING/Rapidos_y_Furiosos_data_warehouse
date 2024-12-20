from typing import List
import pandas as pd


def transformation(tables: List[pd.DataFrame]) -> pd.DataFrame:
	sede_table = tables[0]
	ciudad_table = tables[1]
	departamento_table = tables[2]

	office_dimension = sede_table.merge(ciudad_table, on="ciudad_id", how="left")

	office_dimension = office_dimension.rename(
			columns={
				"sede_id": "original_office_id",
				"nombre_x": "office_name",
				"nombre_y": "office_city"
			}
		)

	office_dimension = office_dimension[[
			"original_office_id",
			"office_name",
			"office_city",
			"departamento_id"
		]]

	office_dimension = office_dimension.merge(departamento_table, on="departamento_id", how="left")
	office_dimension.drop(columns=["departamento_id"], inplace=True)
	office_dimension.rename(columns={ "nombre": "office_region" }, inplace=True)

	office_dimension.reset_index(inplace=True)
	office_dimension.rename(columns={ "index": "office_id" }, inplace=True)
	office_dimension.set_index("office_id", inplace=True)

	return office_dimension