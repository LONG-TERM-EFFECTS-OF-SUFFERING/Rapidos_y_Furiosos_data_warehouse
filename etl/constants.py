# Table names
COURIER_TABLE = "clientes_mensajeroaquitoy"
CITY_TABLE = "ciudad"
CUSTOMER_TABLE = "cliente"
OFFICE_TABLE = "sede"
SERVICE_STATUS_TABLE = "mensajeria_estado"
UPDATES_TABLE = "mensajeria_tiponovedad"

# Queries
QUERY_TIME_DIMENSION = """
    SELECT generate_series(
        '2023-09-18'::timestamp, 
        '2024-01-09'::timestamp, 
        '1 minute'::interval
    ) AS date;
"""