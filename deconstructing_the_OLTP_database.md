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

> Busyness will be measured as a function of how many services (at a specify time) have `state_id` equal to "Con mensajero asignado" ($2$).

## How many services are requested by each client per month?

## Which couriers are the most efficient (based on the number of services completed)?

## Which client locations request the most services?

## What is the average delivery time from service request to case closure?

- Granularity: transactional.

- Related tables:.

    - `mensajería_estadoservicio`

        - `servicio_id`

        - `estado_id`

        - `fecha`

        - `hora`

    - `mensajería_estado`

        - `id`

        - `nombre`

> It should be noted that in `mensajería_estadoservicio` to detect the states. the state with the attribute `estado_id` equal to "6" must be searched, which corresponds to "Terminado completo". It could even take into account the "Iniciado" with `estado_id` equal to "1".

## What are the waiting times at each service stage (e.g., initiated, courier assigned, picked up, delivered, closed)? In which stage do delays occur most frequently?

- Granularity: transactional.

- Related tables:

    - `mensajería_estadoservicio`

        - `servicio_id`

        - `estado_id`

        - `fecha`

        - `hora`

    - `mensajería_estado`

        - `id`

        - `nombre`

## What are the most common issues reported during service provision?
## Español: ¿Cuáles son los problemas más comunes reportados durante la prestación del servicio?

- Granularity: transactional.

- Related tables:

    - `mensajería_novedadservicio`

        - `servicio_id`

        - `tipo_novedad_id`

    - `mensajería_tiponovedad`
        
        - `id`
        
        - `nombre`