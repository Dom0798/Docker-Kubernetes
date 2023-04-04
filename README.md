# Docker-Kubernetes
Docker files and examples and hits on how to use Docker.

## Basics
### Build, run and start
#### Build image
You can use `docker build .` when we have a Dockerfile in the directory.

There are many flags available (use --help to get a list) to add some features:

- `-t`: indicate a NAME:TAG.

#### Run image to create a container
You can use `docker run IMAGE` to create a container of that image.

Note: `docker run` is attached by default. You can use --detach to change this.

There are many flags available (use --help to get a list) to add some features:

- `-it`: launch a container as interactive and creates a terminal
- `--rm`: remove container when it exits
- `--name`: launch a container with specific name.

#### Start an existing container
If you only want to run again the same container and don't create a new one, you can run `docker start CONTAINER`.

Note: `docker start` is detached by default. You can use --attach to change this.

There are many flags available (use --help to get a list) to add some features:

- `-i`: runs container as interactive


### Managing images and containers
#### Containers
Use `docker ps` to get a list of active containers, add -a to get all containers.

Use `docker rm CONTAINER` to remove a container.

To automatically remove a container when it exits, use the --rm flag when using `docker run`.

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