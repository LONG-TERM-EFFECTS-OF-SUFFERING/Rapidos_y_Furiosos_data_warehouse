# Deconstructing the OLTP database

## Which months of the year have the highest number of courier service requests?

- Granularity: monthly.

- Related tables:

    - `mensajeria_servicio`.

        - `fecha_solicitud`.

## Which days of the week see the most service requests?

- Granularity: daily.

- Related tables:

    - `mensajeria_servicio`.

        - `fecha_solicitud`.

## At what time of day are couriers busiest?

- Granularity: transactional.

- Related tables:

    - `mensajeria_estado`.

        - `id`.

    - `mensajeria_estadosservicio`.

        - `hora`.

        - `estado_id`.

> Busyness will be measured as a function of how many services (at a specific time) have `state_id` equal to "Con mensajero asignado" ($2$).

## How many services are requested by each client per month?

- Granularity: monthly.

- Related tables:

    - `mensajeria_estadosservicio`.

        - `cliente_id`.

    - `clientes`.

## Which couriers are the most efficient (based on the number of services completed)?

- Granularity: transactional.

- Related tables:

    - `mensajeria_estadosservicio`.

        - `mensajero_id`.

    - `mensajeria_estado`.

        - `id`.

    - `mensajeria_estadosservicio`.

        - `estado_id`.

        - `servicio_id`.

## Which client locations request the most services?

- Granularity: transactional.

- Related tables:

    - `mensajeria_estadosservicio`.

        - `origen_id`.

    - `mensajeria_origenservicio`.

        - `ciudad_id`.

    - `ciudad`.

        - `nombre`.

## What is the average delivery time from service request to case closure?

- Granularity: transactional.

- Related tables.

    - `mensajeria_estado`.

        - `id`.

        - `nombre`.

    - `mensajeria_estadosservicio`.

        - `fecha`.

        - `hora`.

        - `estado_id`.

        - `servicio_id`.

> In `mensajeria_estadoservicio`, a `estado_id` equal to $6$ corresponds to "Terminado completo" and a `estado_id` equal to $1$ corresponds to "Iniciado".

## What are the waiting times at each service stage (e.g., initiated, courier assigned, picked up, delivered, closed)? In which stage do delays occur most frequently?

- Granularity: transactional.

- Related tables.

    - `mensajeria_estado`.

        - `id`.

        - `nombre`.

    - `mensajeria_estadosservicio`.

        - `fecha`.

        - `hora`.

        - `estado_id`.

        - `servicio_id`.

## What are the most common issues reported during service provision?

- Granularity: transactional.

- Related tables:

    - `mensajeria_tiponovedad`.

        - `id`.

        - `nombre`.

    - `mensajeria_novedadservicio`.

        - `servicio_id`.

        - `tipo_novedad_id`.
