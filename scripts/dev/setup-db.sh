source scripts/dev/.settings
docker pull postgres
docker run --name postgres-dev -e POSTGRES_DEV_PASSWORD="$POSTGRES_DEV_PASSWORD" -d postgres