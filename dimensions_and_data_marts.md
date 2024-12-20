# Dimensions and data marts

## Dimensions

### Courier

```MERMAID
erDiagram
    COURIER_DIMENSION {
        int courier_id PK
        int original_courier_id
        string courier_city
    }
```

### Customer

```MERMAID
erDiagram
    CUSTOMER_DIMENSION {
        int customer_id PK
        int original_customer_id
        string customer_city
    }
```

### Office

```MERMAID
erDiagram
    OFFICE_DIMENSION {
        int office_id PK
        int original_office_id
        string office_name
        string office_city
        string office_region
    }
```

> `office_name` would be the "sede" name.

### Update

```MERMAID
erDiagram
    UPDATE_DIMENSION {
        int update_id PK
        string update_description
    }
```

The possible description are:

1. "Novedades del servicio".

2. "No puedo continuar".

### Service status

```MERMAID
erDiagram
    SERVICE_STATUS_DIMENSION {
        int status_id PK
        string status_name
        string status_description
    }
```

### Time

```MERMAID
erDiagram
    TIME_DIMENSION {
        int time_id PK
        date date
        int year
        int month
        int day
        int day_of_week
        int day_of_month
        string month_str
        string day_str
        int hour
        int minute
    }
```

## Data marts

### Acummulating snapshot (transactional)

```MERMAID
erDiagram
    TIME_DIMENSION {
        int time_id PK
        date date
        int year
        int month
        int day
        int day_of_week
        int hour
        int minute
        int second
    }

    ACUMMULATING_SNAPSHOT_FACT_TABLE {
        int acummulating_snapshot_fact_table_id PK
        int service_id
        int request_time_id FK
        int assignment_time_id FK
        int pickup_time_id FK
        int delivery_time_id FK
        int closure_time_id FK
        interval request_assignment_time
        interval assignment_pickup_time
        interval pickup_delivery_time
        interval delivery_closure_time
    }

    TIME_DIMENSION ||--o{ ACUMMULATING_SNAPSHOT_FACT_TABLE : "has"
```

### Services (hour and daily)

```MERMAID
erDiagram
    COURIER_DIMENSION {
        int courier_id PK
        int original_courier_id
        string courier_city
    }

    CUSTOMER_DIMENSION {
        int customer_id PK
        int original_customer_id
        string customer_city
    }

    OFFICE_DIMENSION {
        int office_id PK
        int original_office_id
        string office_name
        string office_city
        string office_region
    }

    SERVICE_STATUS_DIMENSION {
        int status_id PK
        string status_name
        string status_description
    }

    TIME_DIMENSION {
        int time_id PK
        date date
        int year
        int month
        int day
        int day_of_week
        int hour
        int minute
    }

    SERVICE_FACT_TABLE {
        int service_fact_table_id PK
        int time_id FK
        int customer_id FK
        int courier_id FK
        int office_id FK
        int total_services
    }

    TIME_DIMENSION ||--o{ SERVICE_FACT_TABLE : "has"
    COURIER_DIMENSION ||--o{ SERVICE_FACT_TABLE : "has"
    CUSTOMER_DIMENSION ||--o{ SERVICE_FACT_TABLE : "has"
    OFFICE_DIMENSION ||--o{ SERVICE_FACT_TABLE : "has"
    SERVICE_STATUS_DIMENSION ||--o{ SERVICE_FACT_TABLE : "has"
```

### Updates (transactional)

```MERMAID
erDiagram
    TIME_DIMENSION {
        int time_id PK
        date date
        int year
        int month
        int day
        int day_of_week
        int hour
        int minute
        int second
    }

    UPDATE_DIMENSION {
        int update_id PK
        string update_name
    }

    UPDATES_FACT_TABLE {
        int updates_fact_table_id PK
        int update_id FK
        int time_id FK
        int service_id
        string update_description
    }

    TIME_DIMENSION ||--o{ UPDATES_FACT_TABLE : "has"
    UPDATE_DIMENSION ||--o{ UPDATES_FACT_TABLE : "has"
```

## Remarks

1. The information as "name" was not put in `COURIER_DIMENSION` or `CUSTOMER_DIMENSION` because in the OLTP database provided they all have the same name.
