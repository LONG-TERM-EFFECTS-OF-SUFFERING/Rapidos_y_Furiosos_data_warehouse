import pandas as pd
from typing import List


def transformation(tables: List[pd.DataFrame]) -> pd.DataFrame:
    # Unpack tables
    time_dimension = tables[0]
    courier_dimension = tables[1]
    office_dimension = tables[2]
    services = tables[3]
    service_statuses = tables[4]
    clientes_usuarioaquitoy_table = tables[5]
    customer_dimension = tables[6] 

    # Convert 'hora' to string and create a datetime column for statuses
    service_statuses["hora_str"] = service_statuses["hora"].astype(str)
    service_statuses["datetime"] = pd.to_datetime(
        service_statuses["fecha"]
    ) + pd.to_timedelta(service_statuses["hora_str"])

    # Get the latest status per service
    latest_status = service_statuses.sort_values("datetime").drop_duplicates(
        "servicio_id", keep="last"
    )
    latest_status = latest_status.rename(
        columns={"estado_id": "status_id", "servicio_id": "service_id"}
    )

    # Rename service columns for consistency
    # We use original_customer_id / original_courier_id to align with previous logic
    services = services.rename(
        columns={
            "id": "service_id",
            "cliente_id": "original_customer_id",
            "mensajero_id": "original_courier_id",
        }
    )

    # Drop services without assigned courier
    services = services.dropna(subset=["original_courier_id"])

    # Merge latest status into services
    services = services.merge(
        latest_status[["service_id", "status_id"]], on="service_id", how="left"
    )

    # Create a request_time column at hourly granularity
    services["hora_solicitud_str"] = services["hora_solicitud"].astype(str)
    services["request_time"] = pd.to_datetime(
        services["fecha_solicitud"]
    ) + pd.to_timedelta(services["hora_solicitud_str"])
    services["request_time"] = services["request_time"].dt.floor("h")

    # Map request_time to time_id using time_dimension
    time_dimension["date"] = pd.to_datetime(time_dimension["date"])
    time_mapping = dict(zip(time_dimension["date"], time_dimension["time_id"]))
    services["time_id"] = services["request_time"].map(time_mapping)

    # Merge with user information to get the office (sede_id)
    services = services.merge(
        clientes_usuarioaquitoy_table[["id", "sede_id"]],
        left_on="usuario_id",
        right_on="id",
        how="inner",
    )
    services.drop(columns=["usuario_id", "id"], inplace=True)

    # Merge with office_dimension to get office_id
    services = services.merge(
        office_dimension[["office_id", "original_office_id"]],
        left_on="sede_id",
        right_on="original_office_id",
        how="inner",
    )
    services.drop(columns=["sede_id", "original_office_id"], inplace=True)

    # Aggregate services by time_id, customer, courier, and office to count total_services
    hourly_agg = (
        services.groupby(
            ["original_customer_id", "original_courier_id", "time_id", "office_id"]
        )
        .size()
        .reset_index(name="total_services")
    )

    # Merge with customer_dimension to get customer_id
    hourly_agg = hourly_agg.merge(
        customer_dimension[["customer_id", "original_customer_id"]],
        on="original_customer_id",
        how="inner",
    )
    hourly_agg.drop(columns=["original_customer_id"], inplace=True)

    # Merge with courier_dimension to get courier_id
    hourly_agg = hourly_agg.merge(
        courier_dimension[["courier_id", "original_courier_id"]],
        left_on="original_courier_id",
        right_on="original_courier_id",
        how="inner",
    )
    hourly_agg.drop(columns=["original_courier_id"], inplace=True)

    # Rename index and set it as the primary index
    hourly_agg.reset_index(inplace=True)
    hourly_agg = hourly_agg.rename(columns={"index": "service_hour_id"})
    hourly_agg.set_index("service_hour_id", inplace=True)

    return hourly_agg
