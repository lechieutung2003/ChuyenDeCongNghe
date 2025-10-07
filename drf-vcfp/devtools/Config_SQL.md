# Project Setup Guide

This guide will help you set up the development environment for the project using Docker Compose.

## Prerequisites

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) on your computer.
- Make sure Docker Desktop is running before executing any Docker commands.

## Environment Configuration

1. **Copy environment files:**
   - Copy `env.example` to `.env` in the `devtools` folder.
   - Edit `.env` and set values, especially for `BUILD_USERNAME = admin` and `MYSQL_ROOT_PASSWORD & BUILD_PASSWORD = 123456`.
   - Copy `builder/env.example` to `builder/.env` and edit `BUILD_BACKEND_URL=localhost:8008`, `BUILD_USERNAME=admin`, `BUILD_PASSWORD=123456`.

## Starting the SQL Service

Run the following command in the `devtools` directory:

```sh
docker compose --env-file .env up -d --build
```

For Apple Silicon Macbook, use this command instead:
```sh
docker compose --env-file .env -f docker-compose-apple-silicon.yml up -d --build
```

To stop the services, run the command below:

```sh
docker compose down
```

For Apple Silicon Macbook, use this command instead:

```sh
docker compose -f docker-compose-apple-silicon.yml down
```

## Common Issues

- **Docker not running:**  
  If you see an error like `The system cannot find the file specified`, make sure Docker Desktop is started.

## Notes

- The `.env` file contains all environment variables for your services.
- The `docker/mysql` folder stores MySQL data persistently.
- Other services (MongoDB, Redis, Elastic Stack, etc.) can be enabled by uncommenting their sections in the compose file as needed.

---