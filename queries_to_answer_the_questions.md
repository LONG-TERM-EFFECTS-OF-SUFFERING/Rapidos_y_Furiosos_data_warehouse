# Queries to answer the questions

## Which months of the year have the highest number of courier service requests?

### Using the service hour dataframe

```SQL
SELECT
    td.month,
    SUM(sfh.total_services) AS total_services
FROM
    public."SERVICE_FACT_HOUR_TABLE" sfh
JOIN
    public."TIME_DIMENSION" td ON sfh.time_id = td.time_id
GROUP BY
    td.month
ORDER BY
    total_services DESC;
```

## Which days of the week see the most service requests?

### Using the service hour dataframe

```SQL
SELECT
    td.day_str AS day_of_week,
    SUM(sfh.total_services) AS total_services
FROM
    public."SERVICE_FACT_HOUR_TABLE" sfh
JOIN
    public."TIME_DIMENSION" td ON sfh.time_id = td.time_id
GROUP BY
    td.day_str
ORDER BY
    total_services DESC;
```

## At what time of day are couriers busiest?

### Using the service hour dataframe

```SQL
SELECT
    td.hour,
    SUM(sfh.total_services) AS total_services
FROM
    public."SERVICE_FACT_HOUR_TABLE" sfh
JOIN
    public."TIME_DIMENSION" td ON sfh.time_id = td.time_id
GROUP BY
    td.hour
ORDER BY
    total_services DESC;
```

## How many services are requested by each client per month?

### Using the service hour dataframe

```SQL
SELECT
    sfh.customer_id,
    td.month,
    COUNT(sfh.service_fact_hour_table_id) AS total_services
FROM
    public."SERVICE_FACT_HOUR_TABLE" sfh
JOIN
    public."TIME_DIMENSION" td ON sfh.time_id = td.time_id
GROUP BY
    sfh.customer_id,
    td.month
ORDER BY
    sfh.customer_id,
    td.month;
```

## Which couriers are the most efficient (based on the number of services completed)?

### Using the service hour dataframe

```SQL
SELECT
    sfh.courier_id,
    COUNT(sfh.service_fact_hour_table_id) AS total_services
FROM
    public."SERVICE_FACT_HOUR_TABLE" sfh
GROUP BY
    sfh.courier_id
ORDER BY
    total_services DESC
LIMIT 10;
```

## Which are the locations that request the most services per client?

### Using the service hour dataframe

```SQL
SELECT
    sfh.customer_id,
    sfh.office_id,
    COUNT(sfh.service_fact_hour_table_id) AS total_services
FROM
    public."SERVICE_FACT_HOUR_TABLE" sfh
GROUP BY
    sfh.customer_id,
    sfh.office_id
ORDER BY
    sfh.customer_id,
    total_services DESC;
```

## What is the average delivery time from service request to case closure?

```SQL
SELECT
    AVG((delivery_closure_time - request_assignment_time) / 3600) AS average_delivery_time_hours
FROM
    public."ACUMMULATING_SNAPSHOT_FACT_TABLE"
WHERE
    delivery_closure_time != 0
    AND request_assignment_time != 0;
```

## What are the waiting times at each service stage (e.g., initiated, courier assigned, picked up, delivered, closed)? In which stage do delays occur most frequently?

## Complete services

``` SQL
SELECT
    AVG(request_assignment_time) AS avg_request_assignment_time,
    AVG(assignment_pickup_time) AS avg_assignment_pickup_time,
    AVG(pickup_delivery_time) AS avg_pickup_delivery_time,
    AVG(delivery_closure_time) AS avg_delivery_closure_time
FROM
    public."ACUMMULATING_SNAPSHOT_FACT_TABLE"
WHERE
    request_assignment_time != 0
    AND assignment_pickup_time != 0
    AND pickup_delivery_time != 0
    AND delivery_closure_time != 0;
```

- avg_request_assignment_time: $10092.603901611536$.

- avg_assignment_pickup_time: $4387.201017811705$.

- avg_pickup_delivery_time: $4123.867684478371$.

- avg_delivery_closure_time: $18151.80661577608$.

## All services

```SQL
SELECT
    AVG(request_assignment_time) AS avg_request_assignment_time
FROM
    public."ACUMMULATING_SNAPSHOT_FACT_TABLE"
WHERE
    request_assignment_time != 0
```

$10581.046125318706$

```SQL
SELECT
    AVG(assignment_pickup_time) AS avg_assignment_pickup_time
FROM
    public."ACUMMULATING_SNAPSHOT_FACT_TABLE"
WHERE
    assignment_pickup_time != 0
```

$5281.767459562321$

```SQL
SELECT
    AVG(pickup_delivery_time) AS avg_pickup_delivery_time
FROM
    public."ACUMMULATING_SNAPSHOT_FACT_TABLE"
WHERE
    pickup_delivery_time != 0
```

$6188.743354824115$

```SQL
SELECT
    AVG(delivery_closure_time) AS avg_delivery_closure_time
FROM
    public."ACUMMULATING_SNAPSHOT_FACT_TABLE"
WHERE
    delivery_closure_time != 0
```

$18402.80608365019$

## What are the most common issues reported during service provision?

```SQL
SELECT
    update_description,
    COUNT(*) AS issue_count
FROM
    public."UPDATES_FACT_TABLE"
GROUP BY
    update_description
ORDER BY
    issue_count DESC
LIMIT 10;
```
