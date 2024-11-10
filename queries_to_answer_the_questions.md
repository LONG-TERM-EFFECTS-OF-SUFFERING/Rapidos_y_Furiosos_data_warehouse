# Queries to answer the questions

## Which months of the year have the highest number of courier service requests?

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
