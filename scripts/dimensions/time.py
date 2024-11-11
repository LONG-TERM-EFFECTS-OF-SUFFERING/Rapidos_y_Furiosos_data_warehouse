import pandas as pd


def transformation(tables):
	time_dimension = pd.DataFrame(
		{ "date": pd.date_range(start="18/9/2023", end="9/1/2024", freq="min") }
	)

	time_dimension["year"] = time_dimension["date"].dt.year
	time_dimension["month"] = time_dimension["date"].dt.month
	time_dimension["day"] = time_dimension["date"].dt.day
	time_dimension["day_of_year"] = time_dimension["date"].dt.day_of_year
	time_dimension["day_of_month"] = time_dimension["date"].dt.days_in_month
	time_dimension["month_str"] = time_dimension["date"].dt.month_name()
	time_dimension["day_str"] = time_dimension["date"].dt.day_name()
	time_dimension["hour"] = time_dimension["date"].dt.hour
	time_dimension["minute"] = time_dimension["date"].dt.minute

	time_dimension.reset_index(inplace=True)
	time_dimension.rename(columns={ "index": "time_id" }, inplace=True)
	time_dimension.set_index("time_id", inplace=True)

	return time_dimension
