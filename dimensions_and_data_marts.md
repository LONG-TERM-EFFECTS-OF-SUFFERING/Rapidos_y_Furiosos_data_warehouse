# Dimensions and data marts

## Dimensions

### Courier

```MERMAID
erDiagram
    COURIER_DIMENSION {
        int courier_id PK
        string courier_city
    }
```

### Customer

```MERMAID
erDiagram
    CUSTOMER_DIMENSION {
        int customer_id PK
        string customer_city
    }
```

### Location

```MERMAID
erDiagram
    LOCATION_DIMENSION {
        int location_id PK
        string location_name
        string location_type
        string location_city
        string location_region
    }
```

> `location_name` would be the "sede" name.

### Update

```MERMAID
erDiagram
    UPDATE_DIMENSION {
        int update_id PK
        string update_name
        string update_description
    }
```

The possible names are:

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
        int request_time FK
        int assignment_time FK
        int pickup_time FK
        int delivery_time FK
        int closure_time FK
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
        string courier_city
    }

    CUSTOMER_DIMENSION {
        int customer_id PK
        string customer_city
    }

    LOCATION_DIMENSION {
        int location_id PK
        string location_name
        string location_type
        string location_city
        string location_region
    }

    SERVICE_STATUS_DIMENSION {
        int status_id PK
        string status_name
        string status_description
    }

    SERVICE_FACT_TABLE {
        int service_fact_table_id PK
        int service_id
        int customer_id FK
        int courier_id FK
        int status_id FK
        int origin_location_id FK
        int destination_location_id FK
    }

    COURIER_DIMENSION ||--o{ SERVICE_FACT_TABLE : "has"
    CUSTOMER_DIMENSION ||--o{ SERVICE_FACT_TABLE : "has"
    LOCATION_DIMENSION ||--o{ SERVICE_FACT_TABLE : "has"
    SERVICE_STATUS_DIMENSION ||--o{ SERVICE_FACT_TABLE : "has"
```

### News (transactional)

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
        string update_description
    }

    NEWS_FACT_TABLE {
        int news_fact_table_id PK
        int service_id
        int update FK
        int time FK
    }

    TIME_DIMENSION ||--o{ NEWS_FACT_TABLE : "has"
    UPDATE_DIMENSION ||--o{ NEWS_FACT_TABLE : "has"
```

## Remarks

1. The information as "name" was not put in `COURIER_DIMENSION` or `CUSTOMER_DIMENSION` because in the OLTP database provided they all have the same name.
