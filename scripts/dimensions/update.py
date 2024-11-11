from typing import List
import pandas as pd


def transformation(tables: List[pd.DataFrame]) -> pd.DataFrame:
	mensajeria_tiponovedad_content = tables[0]

	update_dimension = mensajeria_tiponovedad_content.drop(columns=["id"])
	update_dimension.reset_index(inplace=True)
	update_dimension.rename(
		columns={
			"index": "update_id",
			"nombre": "update_name",
		}, inplace=True
	)
	update_dimension.set_index("update_id", inplace=True)

	return update_dimension
