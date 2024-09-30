# Dimensions, fact table and data mart

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
        int hour
        int minute
        int second
    }
```

## Fact table

```MERMAID
erDiagram
    SERVICE_FACT {
        int service_id PK
        int original_service_id
        int customer_id FK
        int courier_id FK
        int status_id FK
        int origin_location_id FK
        int destination_location_id FK
        int request_time FK
        int assignment_time FK
        int pickup_time FK
        int delivery_time FK
        int closure_time FK
        int update FK
        interval service_duration
        interval waiting_time
    }
```

## Data mart

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

    UPDATE_DIMENSION {
        int update_id PK
        string update_name
        string update_description
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
        int second
    }

    SERVICE_FACT {
        int service_id PK
        int original_service_id
        int customer_id FK
        int courier_id FK
        int status_id FK
        int origin_location_id FK
        int destination_location_id FK
        int request_time FK
        int assignment_time FK
        int pickup_time FK
        int delivery_time FK
        int closure_time FK
        int update FK
        interval service_duration
        interval waiting_time
    }

    COURIER_DIMENSION ||--o{ SERVICE_FACT : "has"
    CUSTOMER_DIMENSION ||--o{ SERVICE_FACT : "has"
    LOCATION_DIMENSION ||--o{ SERVICE_FACT : "has"
    UPDATE_DIMENSION ||--o{ SERVICE_FACT : "has"
    SERVICE_STATUS_DIMENSION ||--o{ SERVICE_FACT : "has"
    TIME_DIMENSION ||--o{ SERVICE_FACT : "has"
```

## Remarks

1. The information as "name" was not put in `COURIER_DIMENSION` or `CUSTOMER_DIMENSION` because in the OLTP database provided they all have the same name.
