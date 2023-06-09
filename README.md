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

### Dockerfile and docker compose yml
See Dockerfile and docker-compose.yml files in this repo to understand them.
To run a docker compose file in detached mode, use `docker compose up -d`. For taking it down, use `docker compose down`.

### Useful docker commands
- `docker exec -it CONTAINER_NAME command`: let's you run a command and communicate with the running container content

### Deployment in AWS
#### EC2 instance
If on Windows, use PuTTY to connect to your EC2 instance:
1. Use PuTTygen to change the .pem to .ppk:
    1. Load the .pem
    2. Use RSA and click on Save private key
2. Use PuTTY to connect:
    1. On host name use the instance DNS
    2. Use port 22
    3. On Connection>SSH>Auth, load the .ppk
    4. Click Open.

#### Install Docker in EC2
1. Run the following:
```
$ sudo yum update -y
$ sudo yum -y install docker
$ sudo service docker start
$ sudo usermod -a -G docker ec2-user
```
2. Log out, then log in again and run:
```
$ sudo systemctl enable docker
$ sudo systemctl start docker
$ sudo systemctl status docker
```
Everything should have been succesful.

## Kubernetes
### Install
When using Docker Destop, just go to the settings to the Kubernetes tab, enable it and wait to the install to complete.
Use `kubectl get nodes` command to check if it is installed.

### Deployment object creation
To create an object in your cluster, use `kubectl create deployment NAME --image=IMAGE_NAME`. Note: the image should be at Docker Hub.
With this, we create a master node connected to a worker node with the container of the image in the args.

### Service object creation
In order to expose a pod, you should use `kubectl expose deployment NAME_DEPLOYMENT --type=LoadBalancer --port=PORT_NUMBER`.
We are using a LoadBalancer to take advantage of the scaling features and don't use only a NodePort.

### Scaling
To run several instances of a pod, use `kubectl scale deployment/DEPLOYMENT_NAME --replicas=NUMBER_TO_SCALE`

### Updating
To update a deployment, you should use `kubectl set image deployment/DEPLOYMENT_NAME CURRENT_CONTAINER_NAME=IMAGE_NAME`. Note: it will only update if the new image has a different tag.

### Rollback
To do a rollback, you can use `kubectl rollout undo deployment/DEPLOYMENT_NAME`. This will undo the latest deployment.

If you want to go to a specific revision you can use the following commands:
```
# get revisions
$ kubectl rollout history deployment/DEPLOYMENT_NAME
# rollback to one of those revisions
$ kubectl rollout undo deployment/DEPLOYMENT_NAME --to-revision=NUM_REVISION
```

### Declarative approach (or yaml file)
See deployment.yaml and service.yaml files in this repo to understand them.

To run them, use `kubectl apply -f NAME_OF_FILE.yaml`.

In order to update, just make the changes in the file and use the same command.

Deleting the resources created by this should be done with `kubectl delete -f NAME_OF_FILE.yaml`.

### Dashboard
In order to use the dashboard, you should deploy the UI with:
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
```
Run the port exposure with `kubectl proxy` and now you can access the UI in http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/

To create a token, use the following commands and paste the token generated in the web page:
```
$ kubectl apply -f dashboard-adminuser.yaml
$ kubectl -n kubernetes-dashboard create token admin-user
```


## Troubleshooting
### mySQL
If ever having a problem about caching_sha2_password, execute the following commands:
```
$ docker exec -it mysql bash    # if executing db in a container
$ mysql -u root -p
$ ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'your password here';
```

### Clean up Docker WSL disk space
To clean the virtual disk space, use the following command:
```
Optimize-VHD -Path "C:\Path\to\AppData\Local\Docker\wsl\data\ext4.vhdx" -Mode Full
```