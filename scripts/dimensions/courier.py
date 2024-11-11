from typing import List
import pandas as pd


def transformation(tables: List[pd.DataFrame]) -> pd.DataFrame:
	clientes_mensajeroaquitoy_table = tables[0]
	ciudad_table = tables[1]

	courier_dimension = clientes_mensajeroaquitoy_table.merge(
			ciudad_table, left_on="ciudad_operacion_id", right_on="ciudad_id", how="left"
	)

	courier_dimension.rename(
		columns={
			"nombre": "courier_city"
		}, inplace=True
	)

	courier_dimension = courier_dimension[["courier_city"]]

	courier_dimension.reset_index(inplace=True)
	courier_dimension.rename(columns={ "index": "courier_id" }, inplace=True)
	courier_dimension.set_index("courier_id", inplace=True)

	return courier_dimension
