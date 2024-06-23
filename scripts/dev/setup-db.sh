source scripts/dev/.settings
docker pull postgres:16.0
docker run --name postgres-dev -e POSTGRES_HOST_AUTH_METHOD=trust -d postgres:16.0