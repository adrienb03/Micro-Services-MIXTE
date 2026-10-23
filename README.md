
# TP Microservices Mixte - API REST & GraphQL

This project consists of 4 Python microservices, orchestrated using Docker Compose.

The application uses GraphQL and REST API for querying and modifying data, and MongoDB for persistent storage.

## Running the Project

Make sure Docker and Docker Compose are installed.

From the project root directory, run:

```bash
docker compose up --build
```

To stop the services:

```bash
docker compose down
```

To stop the services and delete the MongoDB data:

```bash
docker compose down -v
```

## Microservices

| Service | Port | API Type | Description |
|---|---|---|---|
| Movie | 3001 | GraphQL | Manages movie information |
| Schedule | 3002 | REST | Manages movie schedules |
| Booking | 3003 | GraphQL | Manages user bookings |
| User | 3004 | REST | Manages user information |

Each service is accessible at `http://localhost:<port>`.

## Database

The project uses MongoDB, with a separate database for each microservice:

- `movies_db`
- `schedules_db`
- `bookings_db`
- `users_db`

MongoDB runs on port `27017`.

Data is persisted using a Docker volume (`mongo_data`).

### Mongo Express

Mongo Express provides a web interface for managing MongoDB databases.

Access it at:

http://localhost:8081

## Technologies

- Python
- Flask
- GraphQL
- MongoDB
- Docker
- Docker Compose

## Insomnia tests

You can import requests on Insomnia. The file to import is: Insomnia_EXPORT_tests.yaml from the project root directory.