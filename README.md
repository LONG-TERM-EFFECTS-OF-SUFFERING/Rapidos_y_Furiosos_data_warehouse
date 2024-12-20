# Project

The project involves building a data analytics system for "Rápidos y Furiosos", a courier company operating in various cities across Colombia. The company's goal is to support its decision-making processes by analyzing the data generated by its customers and couriers. "Rápidos y Furiosos" already has an operational information system that manages clients and services, but due to growth and increased demand, new challenges have emerged, such as customer complaints about delivery delays and couriers reporting issues with certain clients.

## Members

- Agudelo Hernández Carlos Andrés (2125653).

- Calderón Prieto Brandon (2125974).

- Ortiz Gonzalez Juan Camilo (2023921).

## Questions to be answered

1. Which months of the year have the highest number of courier service requests?

2. Which days of the week see the most service requests?

3. At what time of day are couriers busiest?

4. How many services are requested by each client per month?

5. Which couriers are the most efficient (based on the number of services completed)?

6. Which client locations request the most services?

7. What is the average delivery time from service request to case closure?

8. What are the waiting times at each service stage (e.g., initiated, courier assigned, picked up, delivered, closed)? In which stage do delays occur most frequently?

9. What are the most common issues reported during service provision?

## Business processes

### Courier services management

- Service request: customers request courier services through a web application, specifying the city of origin and destination, addresses and delivery times (express, within 2-3 hours, or during the day).

- Service assignment: when a new service is registered, a notification is sent to available couriers. A courier picks up the service through a mobile application, which changes the service status to "With assigned courier".

- Service delivery: the courier picks up the order at the origin address and delivers it to the destination address. The service goes through several statuses (Initiated, With assigned courier, Picked up at origin, Delivered at destination, Closed).

- Shipment status monitoring: customers can check the status of the service through the operational application at any time.

### Updates management

- Updates management: if unforeseen events occur, such as mechanical failures or customer delays, the courier can report news, which can alter the delivery time.

## Dimensions

1. Courier.

2. Customer.

3. Office.

4. Update.

5. Status.

6. Time.

## Bus matrix

|     Business processes      | Courier | Customer | Office | Update | Status | Time |
|:---------------------------:|:-------:|:--------:|:------:|:------:|:------:|:----:|
| courier services management |    X    |    X     |   X    |        |   X    |  X   |
|     updates management      |         |          |        |   X    |        |  X   |
