# Docker-Kubernetes
Docker files and examples and hits on how to use Docker.

## Docker
### Build, run and start
#### Build image
You can use `docker build .` when we have a Dockerfile in the directory.

There are many flags available (use *--help* to get a list) to add some features:

- `-t`: indicate a NAME:TAG.

#### Run image to create a container
You can use `docker run IMAGE` to create a container of that image.

Note: `docker run` is attached by default. You can use *--detach* to change this.

There are many flags available (use *--help* to get a list) to add some features:

- `-it`: launch a container as interactive and creates a terminal
- `--rm`: remove container when it exits
- `--name`: launch a container with specific name.

#### Start an existing container
If you only want to run again the same container and don't create a new one, you can run `docker start CONTAINER`.

Note: `docker start` is detached by default. You can use *--attach* to change this.

There are many flags available (use *--help* to get a list) to add some features:

- `-i`: runs container as interactive


### Managing images and containers
#### Containers
Use `docker ps` to get a list of active containers, add -a to get all containers.

Use `docker rm CONTAINER` to remove a container.

To automatically remove a container when it exits, use the *--rm* flag when using `docker run`.

To copy files in and out of a container, you can use `docker cp SOURCE DEST` where the container path should be `CONTAINER_NAME:/path`.

#### Images
Use `docker images` to get a list of your images.

Use `docker rmi IMAGE` to remove an image. You need to remove all associated containers first. For remove all images, use `docker image prune -a`, or without the flag to remove the ones without a tag.

To rename an image, use `docker tag OLD_IMAGE_NAME:OLD_TAG NEW_IMAGE_NAME:NEW_TAG`.

To get image info, use `docker image inspect IMAGE_ID`.

### Pushing and pulling images with DockerHub
Once a repo is created in the DockerHub page and the image is has the same name, you can use `docker push IMAGE_NAME`.

To pull an image, use `docker pull IMAGE_NAME:TAG`.

To login to your DockerHub account, run `docker login` and enter credentials.

### Volumes
To create a named volume, in the `docker run` command you should add `-v NAMED_VOL:/path/of/data`.

List the volumes with `docker volume ls`.

To remove anonymous volumes, use `docker volume prune`.

### Bind Mounts
For dev purposes, we can use a second volume flag to provide a bind mount as follows: `-v "SOURCE/CODE/PATH:/DEST/CODE/PATH"`. With this, changes in source code can be seen in active container.

We can add a `:ro`at the end to specify the container to use this folder as a read-only source.

You may want to add anonymous volumes after to prioritize internal folder such as read-write folders or dependencies folders.

### Connecting to databases
#### Container to localhost
If you want a container that connects to your local database (for example, mysql), you need to use *host.docker.internal* instead of *localhost*.

#### Container to container
Use `docker container inspect IMAGE_NAME` command with the database container that you are using and search for the IP adress in the network settings.

An easier way to do this is to use Container Networks. With `docker network create NETWORK_NAME`, create a network; after this, run the database container adding the *--network NETWORK_NAME* flag. In the connection code, you should use the database container name as host.

## Troubleshooting
### mySQL
If ever having a problem about caching_sha2_password, execute the following commands:
```
$ docker exec -it mysql bash    # if executing db in a container
$ mysql -u root -p
$ ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'your password here';
```