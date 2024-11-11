from typing import List
import pandas as pd


def transformation(tables: List[pd.DataFrame]) -> pd.DataFrame:
	cliente_table = tables[0]
	ciudad_table = tables[1]

	customer_dimension = cliente_table.merge(ciudad_table, on="ciudad_id", how="left")

	customer_dimension.rename(
		columns={
			"nombre_y": "customer_city",
		}, inplace=True
	)

	customer_dimension = customer_dimension[["customer_city"]]

	customer_dimension.reset_index(inplace=True)
	customer_dimension.rename(columns={ "index": "customer_id" }, inplace=True)
	customer_dimension.set_index("customer_id", inplace=True)

	return customer_dimension
