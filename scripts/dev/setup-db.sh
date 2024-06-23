source scripts/dev/.settings
docker pull postgres:16.0
docker run --name postgres-dev --env PGUSER=$POSTGRES_USER --env POSTGRES_USER=$POSTGRES_USER --env POSTGRES_PASSWORD=$POSTGRES_DEV_PASSWORD -d postgres:16.0
