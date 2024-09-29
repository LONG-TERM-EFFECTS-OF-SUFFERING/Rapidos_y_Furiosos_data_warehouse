# Dimensions and fact table

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
