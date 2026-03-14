# Docker Cheat Sheet

## Containers

### List running containers

    docker ps

### List all containers (including stopped)

    docker ps -a

### Inspect container details

    docker inspect <container>

------------------------------------------------------------------------

## Logs

### View container logs

    docker logs <container>

### Follow logs live

    docker logs -f <container>

### Show last 50 log lines

    docker logs --tail 50 <container>

### Show logs with timestamps

    docker logs -t <container>

Example:

    docker logs -f learn_airflow-airflow-webserver-1

------------------------------------------------------------------------

## Enter a Running Container

### Open bash shell

    docker exec -it <container> bash

If bash is unavailable:

    docker exec -it <container> sh

Example:

    docker exec -it learn_airflow-airflow-webserver-1 bash

------------------------------------------------------------------------

## Start / Stop Containers

Start container:

    docker start <container>

Stop container:

    docker stop <container>

Force kill container:

    docker kill <container>

Restart container:

    docker restart <container>

------------------------------------------------------------------------

## Remove Containers

Remove container:

    docker rm <container>

Remove all stopped containers:

    docker container prune

------------------------------------------------------------------------

## Images

List images:

    docker images

Pull image:

    docker pull apache/airflow:2.9.2

Remove image:

    docker rmi <image>

------------------------------------------------------------------------

## Run a Container

Example:

    docker run -d -p 8080:8080 --name myapp nginx

Meaning: - `-d` → run in background - `-p` → port mapping - `--name` →
container name

------------------------------------------------------------------------

## Docker Compose (Multi‑Container Apps)

Start services:

    docker compose up -d

Stop services:

    docker compose down

View logs:

    docker compose logs

Follow logs:

    docker compose logs -f

Restart a service:

    docker compose restart <service>

Example:

    docker compose restart airflow-webserver

------------------------------------------------------------------------

## System Cleanup

Check disk usage:

    docker system df

Remove unused objects:

    docker system prune

Remove everything unused (aggressive):

    docker system prune -a

------------------------------------------------------------------------

## Mental Model

Docker revolves around four core objects:

-   **Container** → Running process
-   **Image** → Template used to create containers
-   **Volume** → Persistent storage
-   **Network** → Communication layer between containers

------------------------------------------------------------------------

## Images (Build / Tag / Save)

Build from a Dockerfile (context = current folder):

    docker build -t myimage:latest .

Build and tag multiple names:

    docker build -t myimage:latest -t myimage:1.0 .

Tag an existing image:

    docker tag <image-id-or-name> myrepo/myimage:1.0

Save an image to a tarball (for transfer):

    docker save -o myimage.tar myrepo/myimage:1.0

Load an image from a tarball:

    docker load -i myimage.tar

------------------------------------------------------------------------

## Volumes & Bind Mounts

List volumes:

    docker volume ls

Inspect a volume:

    docker volume inspect <volume>

Create a named volume:

    docker volume create mydata

Run a container using a named volume:

    docker run -d -v mydata:/data --name myapp nginx

Bind mount a host directory (use for local development):

    docker run -d -v $(pwd)/config:/app/config --name myapp nginx

Remove dangling volumes (not in use):

    docker volume prune

------------------------------------------------------------------------

## Networks

List networks:

    docker network ls

Inspect a network:

    docker network inspect <network>

Create a bridge network (isolated):

    docker network create mynet

Run containers on the same network (so they can talk by name):

    docker run -d --network mynet --name db postgres
    docker run -d --network mynet --name app myapp

Connect an existing container to a network:

    docker network connect mynet <container>

------------------------------------------------------------------------

## Useful Commands & Tips

Show resource usage of running containers:

    docker stats

Show docker system information (daemon, storage driver, etc.):

    docker info

Show port mappings for a container:

    docker port <container>

Run a command and remove container when it exits:

    docker run --rm alpine echo "hello"

Run with environment variables:

    docker run -e ENV=prod -e DEBUG=1 myimage

Run with a custom entrypoint (override CMD/ENTRYPOINT):

    docker run --entrypoint /bin/sh myimage -c "echo hi"

Inspect container logs without following:

    docker logs --tail 100 <container>

Inspect a stopped container's last exit code:

    docker inspect <container> --format='{{.State.ExitCode}}'

------------------------------------------------------------------------

## Docker Compose Tips

Force recreate containers (even if unchanged):

    docker compose up -d --force-recreate

Rebuild images before starting:

    docker compose up -d --build

Show effective configuration (after compose overrides):

    docker compose config

Run a one-off command in a service container:

    docker compose run --rm <service> <command>

Bring down and remove volumes (be careful!):

    docker compose down --volumes
