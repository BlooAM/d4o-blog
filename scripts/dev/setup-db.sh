source scripts/dev/.env
echo $POSTGRES_DEV_PASSWORD
docker build -t postgres-dev -f scripts/dev/Dockerfile_dev --build-arg POSTGRES_DEV_USER=root --build-arg  POSTGRES_DEV_PASSWORD=$POSTGRES_DEV_PASSWORD --build-arg POSTGRES_DEV_PORT=$POSTGRES_DEV_PORT ./
docker run -d -it --name postgres-dev-img -p 5432:5432 postgres-dev