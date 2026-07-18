# zoomcamp-docker-workshop

Workshop notes and Docker cheat sheet.

## Core Docker Commands

### Run a temporary container

```bash
docker run -it ubuntu
```

A stateless container; changes disappear when the container is removed.

### List containers

```bash
docker ps -a
```

Shows all containers, including stopped ones.

### Remove containers

```bash
docker rm $(docker ps -aq)
```

Removes all containers.

### Build an image

```bash
docker build -t test:pandas .
```

`-t` sets the image name and tag. `.` sends the current directory as the build context.

### Run an image interactively

```bash
docker run -it --rm --entrypoint bash test:pandas
```

`--rm` removes the container after exit. `--entrypoint bash` starts a shell instead of the default command.

## Python Setup

```bash
uv init
uv add pandas pyarrow
uv add --dev pgcli
```

`uv init` creates the environment. `uv add --dev pgcli` keeps `pgcli` in the dev dependencies only.

## PostgreSQL and pgAdmin

### Start Postgres

```bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  --network=pg-network \
  --name pgdatabase \
  postgres:18
```

### Connect with pgcli

```bash
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

Inside pgcli, use `\dt` to list tables.

### Start pgAdmin

```bash
docker run -it \
  --network=pg-network \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -e PGADMIN_CONFIG_ENHANCED_COOKIE_PROTECTION=False \
  -e PGADMIN_CONFIG_SESSION_COOKIE_SAMESITE=None \
  -e PGADMIN_CONFIG_SESSION_COOKIE_SECURE=True \
  -e PGADMIN_CONFIG_PROXY_X_FOR_COUNT=1 \
  -e PGADMIN_CONFIG_PROXY_X_PROTO_COUNT=1 \
  -e PGADMIN_CONFIG_PROXY_X_HOST_COUNT=1 \
  -e PGADMIN_CONFIG_PROXY_X_PORT_COUNT=1 \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8086:80 \
  dpage/pgadmin4:8.13
```

## Ingest Script

```bash
docker build -t taxi_ingest:v002 .

docker run -it \
  --network=pg-network \
  taxi_ingest:v002 \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=pgdatabase \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --target-table=yellow_taxi_trips
```

## Docker Compose Workflow

```bash
docker compose -f pipeline/docker-compose.yaml config
docker compose down
docker compose up
```

Useful checks:

```bash
docker compose -f pipeline/docker-compose.yaml ps
docker compose -f pipeline/docker-compose.yaml logs -f ingest
```

## Commands Used Today

```bash
docker rm -f pgadmin
docker network rm pg-network
docker volume rm pipeline_ny_taxi_postgres_data
docker compose down
docker compose up
docker compose ps
docker compose logs --tail=80 ingest
```

What these helped diagnose:

- `docker rm -f pgadmin` cleared the old standalone pgAdmin container name conflict.
- `docker network rm pg-network` only works after containers are removed from it.
- `docker volume rm pipeline_ny_taxi_postgres_data` was needed because Postgres 18 expects the data mount at `/var/lib/postgresql`.
- `docker compose logs --tail=80 ingest` showed the loader was waiting on Postgres readiness.
