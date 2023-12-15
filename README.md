# VPR-Web Ver.1779

## Quick Start

Docker environment variable list:

+ `KAFKA_URL`: Apache Kafka host address.

**Frontend (Flask):**

Docker Hub link: [Here](https://hub.docker.com/repository/docker/trinitrotofu/vpr-frontend/general).

Example:

```shell
docker run -p 80:5000 -e KAFKA_URL="localhost:9092" --name vpr-frontend trinitrotofu/vpr-frontend:latest
```

**Backend:**

Docker Hub link: [Here](https://hub.docker.com/repository/docker/trinitrotofu/vpr-backend/general).

Example:

```shell
docker run -e KAFKA_URL="localhost:9092" --name vpr-backend trinitrotofu/vpr-backend:latest
```
