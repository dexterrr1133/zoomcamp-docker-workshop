# zoomcamp-docker-workshop
Workshop codebases

## Zoomcamp Notes
docker run -it ubuntu
=stateless container, the changes are gone when used again

docker ps -a
=to see what containers are saved

docker rm $(docker ps -aq)
=rm is for remove
=a arguement is for all
=q arguement is for quiet

docker build -t test:pandas . 
-t = for creating a tag for your docker image
test:pandas = the name of the docker image
. = tells that every file and folder in the current directory to send it to the docker engine when building

docker run -it --rm entrypoint:bash test:pandas 12
-it = iteractive terminal
--rm = automatically removes docker image after exiting
entrypoint:bash = forces the container to start in bash

uv init 
= creates an environment

uv add pandas pyarrow
= adds the dependencies to the environment

docker run -it --rm \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v ny_taxi_postgres_data:/var/lib/postgresql \
    -p 5432:5432 \
    postgres:18
-e arguement is for setting the environment variables
-v arguement is for volume mapping
-p arguement is for port mapping
postgres:18 is for setting the version

uv add --dev pgcli
=add pgcli to only dev dependency, better not to add this to the docker container

uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
Inside pgcli, use `\dt` to list tables.
