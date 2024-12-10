import pandas as pd
from typing import List


def transformation(tables: List[pd.DataFrame]) -> pd.DataFrame:
    # Desempaquetar tablas
    time_dimension = tables[0]
    courier_dimension = tables[1]
    office_dimension = tables[2]
    services = tables[3]
    service_statuses = tables[4]
    clientes_usuarioaquitoy_table = tables[5]
    customer_dimension = tables[6]

    # Convertimos fechas
    services["fecha_solicitud"] = (
        services["fecha_solicitud"].dt.floor("d").dt.tz_localize(None)
    )
    time_dimension["date"] = time_dimension["date"].dt.floor("d").dt.tz_localize(None)

    service_statuses["fecha"] = pd.to_datetime(service_statuses["fecha"])

    # Último estado del servicio
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

    # Renombrar columnas en services para coherencia
    services = services.rename(
        columns={
            "id": "service_id",
            "cliente_id": "original_customer_id",
            "mensajero_id": "original_courier_id",
        }
    )

    # Eliminar servicios sin mensajero asignado
    services = services.dropna(subset=["original_courier_id"])

    # Unir el último estado al servicio
    services = services.merge(
        latest_status[["service_id", "status_id"]], on="service_id", how="left"
    )

    # Crear mapeo date->time_id
    # Aquí usamos las fechas diarias (fecha normalizada)
    request_date = pd.to_datetime(time_dimension["date"]).dt.normalize()
    date_mapping = dict(zip(request_date, time_dimension["time_id"]))

    services["fecha_solicitud"] = pd.to_datetime(
        services["fecha_solicitud"]
    ).dt.normalize()
    services["time_id"] = services["fecha_solicitud"].map(date_mapping)

    # Unimos con clientes_usuarioaquitoy para obtener la sede
    services = services.merge(
        clientes_usuarioaquitoy_table[["id", "sede_id"]],
        left_on="usuario_id",
        right_on="id",
        how="inner",
    )
    services.drop(columns=["usuario_id", "id"], inplace=True)

    # Unimos con office_dimension para obtener office_id
    services = services.merge(
        office_dimension[["office_id", "original_office_id"]],
        left_on="sede_id",
        right_on="original_office_id",
        how="inner",
    )
    services.drop(columns=["sede_id", "original_office_id"], inplace=True)

    # Agrupamos por día, cliente, mensajero, time_id, office_id y contamos servicios
    daily_agg = (
        services.groupby(
            ["original_customer_id", "original_courier_id", "time_id", "office_id"]
        )
        .size()
        .reset_index(name="total_services")
    )

    # Unir con customer_dimension para obtener customer_id
    daily_agg = daily_agg.merge(
        customer_dimension[["customer_id", "original_customer_id"]],
        on="original_customer_id",
        how="inner",
    )
    daily_agg.drop(columns=["original_customer_id"], inplace=True)

    # Unir con courier_dimension para obtener courier_id
    daily_agg = daily_agg.merge(
        courier_dimension[["courier_id", "original_courier_id"]],
        left_on="original_courier_id",
        right_on="original_courier_id",
        how="inner",
    )
    daily_agg.drop(columns=["original_courier_id"], inplace=True)

    # Ajustar índices
    daily_agg.reset_index(inplace=True)
    daily_agg = daily_agg.rename(columns={"index": "service_daily_id"})
    daily_agg.set_index("service_daily_id", inplace=True)

    return daily_agg
