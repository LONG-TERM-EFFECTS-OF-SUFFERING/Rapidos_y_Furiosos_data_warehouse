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

### Status

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
    }
```

## Fact table

```MERMAID
erDiagram
    SERVICE_FACT {
        int service_id PK
        int time_id FK
        int customer_id FK
        int courier_id FK
        int status_id FK
        int origin_location_id FK
        int destination_location_id FK
        timestamp request_time
        timestamp assignment_time
        timestamp pickup_time
        timestamp delivery_time
        timestamp closure_time
        interval service_duration
        interval waiting_time
        text issues_reported
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
    }

    SERVICE_FACT {
        int service_id PK
        int time_id FK
        int customer_id FK
        int courier_id FK
        int status_id FK
        int service_type_id FK
        int origin_location_id FK
        int destination_location_id FK
        timestamp request_time
        timestamp assignment_time
        timestamp pickup_time
        timestamp delivery_time
        timestamp closure_time
        interval service_duration
        interval waiting_time
        text issues_reported
    }

    TIME_DIMENSION ||--o{ SERVICE_FACT : "has"
    CUSTOMER_DIMENSION ||--o{ SERVICE_FACT : "has"
    COURIER_DIMENSION ||--o{ SERVICE_FACT : "has"
    SERVICE_STATUS_DIMENSION ||--o{ SERVICE_FACT : "has"
    LOCATION_DIMENSION ||--o{ SERVICE_FACT : "has"
```

## Remarks

1. The information as "name" was not put in `COURIER_DIMENSION` or `CUSTOMER_DIMENSION` because in the OLTP database provided they all have the same name.

2. The `TIME_DIMENSION` did not include information such as "hour", "minute" and "second" because none of the questions required this level of detail.
