# 2. Docker

Benefits of using Docker for a FastAPI, PostgreSQL, and Alembic project:

- Consistency: Ensures the application runs the same in development, testing, and production.
- Isolation: Separates dependencies for FastAPI and PostgreSQL to avoid conflicts.
- Simplified Deployment: Easily deploy and manage multi-container applications with Docker Compose.
- Portability: Runs on any machine with Docker, facilitating easy migration and scaling.
- Versioning: Supports versioning of containers, allowing for easy rollbacks and testing.
- Data Management: Simplifies database setup, persistence, and backups using Docker volumes.
- CI/CD Integration: Works well with CI/CD pipelines for streamlined development and deployment.

> Having Docker installed locally will be a prerequisite for deployment

## Quick Setup

<code-block lang="text" collapsible="true" collapsed-title="Current Project Structure">
<![CDATA[
student-management-system (root)
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── README.bs.md
├── README.md
├── requirements.txt
├── app/
└── scripts/            # + scripts for managing the containers
    ├── clean-up.ps1
    ├── clean-up.sh
    ├── start-psql-client.ps1
    ├── start-psql-client.sh
    ├── start.ps1
    └── start.sh
]]>
</code-block>

This project uses Docker to run FastAPI and PostgreSQL in separate containers.

<procedure title="FastAPI and PostgreSQL">

To run the FastAPI and PostgreSQL containers run the following command in the project root:

```Bash
./scripts/start
```

This script will create a shared network, build the FastAPI image, start the FastAPI and PostgreSQL containers, and output the container logs.

After successful builds, running `docker ps` should show the active containers.

Then visiting `http://localhost:8000/` or `http://127.0.0.1:8000/` in a browser will result with the html body of:

```Bash
{"Hello": "World"}
```

</procedure>

<procedure title="PostgreSQL Client">

To run a PSQL client as a container run:

```Bash
./scripts/start-psql-client
```

This script starts a new container based on the postgres docker image.
This container isn't specified in the docker compose file rather this
should be run if you don't want to download and install the postgres
driver locally.

It starts the client and connects to the network on which the database is
already on. If the database container isn't active the client will throw
errors.
</procedure>

<procedure title="Stopping and Clean Up">

To stop the containers run:

```Bash
docker-compose down
```

or run:

```Bash
./scripts/clean-up
```

For some more options when it comes to handling the client container and network.
</procedure>

<procedure title="Additional Options">

> You can also run:
> ```Bash
> ./scripts/{script name} --help
> ```
> To see how they work.

</procedure>

[_More details on setting up Docker, Dockerfile and Docker Compose can be found here_](https://safetimamovic.github.io/Student-Management-System/docker.html)

> Volumes aren't integrated yet, so live updates don't work


## Dockerfile for FastAPI

[Chosen python docker image](https://hub.docker.com/layers/library/python/3.12.5-alpine3.19/images/sha256-e82522145a995c3e85f873be18743f47de9d28ad8e017dad648bf6a4f47d908d?context=explore)

To create a docker image for the API to run on we need to create
a `Dockerfile`:

```Bash
touch Dockerfile
```

The only files we need in the container are the
FastAPI python files in the `app/` dir and the
dependency list `requirements.txt` for now.

`Dockerfile`:
```Docker
FROM python:3.12.5-alpine3.19

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

CMD ["fastapi", "run", "app/main.py", "--port", "8000", "--host", "0.0.0.0"]
```

- `FROM python:3.12.5-alpine3.19` - Lightweight version of the Python 3.12.5 image that is based on the Alpine Linux distribution.

- `WORKDIR /usr/src/app` - Specifies the working directory.

- `COPY requirements.txt ./` - Copies the requirements.txt file from the local machine to the Docker container.

- `RUN pip install --no-cache-dir -r requirements.txt` - Installs the necessary dependencies without the cache dir

- `COPY app ./app` - Copies all the contents from the local app dir into the new container app dir

- `EXPOSE 8000` - Tells the Docker Engine that this port is exposed.

- `CMD ["fastapi", "run", "app/main.py", "--port", "8000", "--host", "0.0.0.0"]`
    - Using `run` instead of `dev` specifies that the server will run in production mode.
    - The `--port` is set to 8000 by default, but explicitly setting it won't hurt.
    - The `--host` is set to 0.0.0.0

Then the image is built running:

```Bash
docker build . -t student-management-system-image
```

- `build .` - Looks for the `Dockerfile` within the present dir and builds it.
- `-t` - Specifies a tag for the container.

After it is built it can be run:

```Bash
docker run --name student-management-system-api -p 8000:8000 student-management-system-image
```

- `--name student-management-system-api` - Names the container.
- `-p 8000:8000` - Port forwarding, maps the host machine port to the containers port.

<code-block lang="Bash" collapsible="true" collapsed-title="Console Output">
<![CDATA[

(venv) PS C:\Users\Safet\Desktop\Student-Management-System> >>> docker run --name student-management-system-api -p 8000:8000 student-management-system-image <<<
INFO     Using path app\main.py                                                 
INFO     Resolved absolute path \usr\src\app\app\main.py
INFO     Searching for package file structure from directories with __init__.py
         files
INFO     Importing from \usr\src\app\app

 ╭─ Python module file ─╮
 │                      │
 │  🐍 main.py          │
 │                      │
 ╰──────────────────────╯

INFO     Importing module main
INFO     Found importable FastAPI app
                                                                                
 ╭─ Importable FastAPI app ─╮
 │                          │
 │  from main import app    │
 │                          │
 ╰──────────────────────────╯

INFO     Using import string main:app

 ╭─────────── FastAPI CLI - Production mode ───────────╮
 │                                                     │
 │  Serving at: http:\\0.0.0.0:8000                    │
 │                                                     │
 │  API docs: http:\\0.0.0.0:8000\docs                 │
 │                                                     │
 │  Running in production mode, for development use:   │
 │                                                     │
 │  fastapi dev                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http:\\0.0.0.0:8000 (Press CTRL+C to quit)
]]>
</code-block>

Checking the FastAPI container in another terminal window using:

```Bash
docker exec -it student-management-system-api sh
```

- `exec` - Command allows you to run a command inside a running container.
- `-it` - These are two flags combined:
    - `-i` - (interactive) Keeps STDIN (the input stream) open, which is useful for interactive sessions.
    - `-t` - (pseudo-TTY) Allocates a pseudo-TTY, which allows you to have a terminal session inside the container.
- `sh` - This is the command being run inside the container. Here, it starts a shell.

```Bash
PS C:\Users\Safet\Desktop\Student-Management-System> docker exec -it student-management-system-api sh
/usr/src/app # ls
app               requirements.txt
/usr/src/app # cd app
/usr/src/app/app # ls
__pycache__  main.py
```

The FastAPI container is running successfully.

> To stop the container, use `docker stop student-management-system-api`

## PostgreSQL Dockerization

[PostgreSQL Docker Image](https://hub.docker.com/_/postgres)

### Set Up Docker Network

A custom network to connect containers:

```Bash
docker network create student-management-system-network
```

Using the `docker network ls` lists the available networks:

Example:
```Bash
PS C:\Users\Safet\Desktop\Student-Management-System> docker network ls
NETWORK ID     NAME                                DRIVER    SCOPE
442b8854ab56   bridge                              bridge    local
870cf83d1a98   host                                host      local
4f868bd4397d   none                                null      local
af76b6b3547c   student-management-system-network   bridge    local
```

### Start the PostgreSQL Container

Run the PostgreSQL container specifying the network in a new terminal window dedicated to the server (or add `-d` to run in detached mode so console input isn't blocked):

<tabs>
<tab title="PowerShell">
<code-block lang="Bash">
<![CDATA[
docker run `
--name student-management-system-db-server `
--network student-management-system-network `
-p 5432:5432 `
-e POSTGRES_PASSWORD=admin `
postgres
]]>
</code-block>
</tab>
<tab title="Shell">
<code-block lang="Bash">
<![CDATA[
docker run \
--name student-management-system-db-server \
--network student-management-system-network \
-p 5432:5432 \
-e POSTGRES_PASSWORD=admin \
postgres
]]>
</code-block>
</tab>
</tabs>

- `--name student-management-system-db-server` - Names the container for easy reference.
- `--network student-management-system-network` - Connects the container to student-management-system-network.
- `-p 5432:5432` - Port forwarding, maps the host machine port to the containers port, in case of interfacing with the db server using a local db driver.
- `-e POSTGRES_PASSWORD=admin` - Sets the password for the postgres user.
- [`postgres`](https://hub.docker.com/_/postgres) - The docker image from which the container is built

Additional parameters:
- `-d` - Runs the container in the background (detached mode).

> If it's unable to find image 'postgres:latest' locally, it will just install it.

After it has been run, the console output should have something like this:
```Bash
...database system is ready to accept connections
```

Running `docker ps` in another terminal window shows currently running containers:

```Bash
PS C:\Users\Safet\Desktop\Student-Management-System> docker ps
CONTAINER ID   IMAGE                             COMMAND                  CREATED          STATUS          PORTS                    NAMES
>>> 1546238049ba   postgres                          "docker-entrypoint.s…"   49 seconds ago   Up 48 seconds   0.0.0.0:5432->5432/tcp   student-management-system-db-server <<<
>>> b2da2d832c31   student-management-system-image   "fastapi run app/mai…"   18 minutes ago   Up 18 minutes   0.0.0.0:8000->8000/tcp   student-management-system-api <<<
```

> `docker ps -a` shows all containers, even the ones which are not active

Running `docker images` lists all the locally installed images:

```Bash
PS C:\Users\Safet\Desktop\Student-Management-System\docs> docker images
REPOSITORY                        TAG       IMAGE ID       CREATED          SIZE
>>> student-management-system-image   latest    2ae6c5a3cbe0   20 minutes ago   114MB <<<
>>> postgres                          latest    7d4df2898d4d   2 days ago       432MB <<<
```

To enter this environment the following command is run in another terminal window:

```Bash
docker exec -it student-management-system-db-server sh
```

- `exec` - Command allows you to run a command inside a running container.
- `-it` - These are two flags combined:
    - `-i` - (interactive) Keeps STDIN (the input stream) open, which is useful for interactive sessions.
    - `-t` - (pseudo-TTY) Allocates a pseudo-TTY, which allows you to have a terminal session inside the container.
- `sh` - This is the command being run inside the container. Here, it starts a shell.

```Bash
PS C:\Users\Safet\Desktop\Student-Management-System> docker exec -it student-management-system-db-server sh
# psql -U postgres
psql (16.4 (Debian 16.4-1.pgdg120+1))
Type "help" for help.

postgres=# select now();
              now
-------------------------------
 2024-08-11 12:02:33.532333+00
(1 row)
```

### Run the psql Client to Interact with PostgreSQL

In another new terminal window the following command is run:

<tabs>
<tab title="PowerShell">
<code-block lang="Bash">
<![CDATA[
docker run `
  --name student-management-system-db-client `
  -it `
  --rm `
  --network student-management-system-network `
  postgres `
  psql `
  -h student-management-system-db-server `
  -U postgres
]]>
</code-block>
</tab>
<tab title="Shell">
<code-block lang="Bash">
<![CDATA[
docker run \
  --name student-management-system-db-client \
  -it \
  --rm \
  --network student-management-system-network \
  postgres \
  psql \
  -h student-management-system-db-server \
  -U postgres
]]>
</code-block>
</tab>
</tabs>

- `--name student-management-system-db-client` - Names the container as `student-management-system-db-client`.
- `-it` - Allows interactive access to psql.
- `--rm` - Removes the container after the psql session ends.
- `--network student-management-system-network` - Ensures the container can communicate with `student-management-system-db-server`.
- `psql -h student-management-system-db-server -U postgres` - Connects to the PostgreSQL server running in `student-management-system-db-server`.


```Bash
PS C:\Users\Safet\Desktop\Student-Management-System> >>> [docker command above] <<<
Password for user postgres: >>> [admin] <<<
psql (16.4 (Debian 16.4-1.pgdg120+1))
Type "help" for help.

postgres=# select now();
              now              
-------------------------------
 2024-08-10 23:40:11.483165+00
(1 row)
```

Running `docker ps` in another terminal window:

```Bash
PS C:\Users\Safet\Desktop\Student-Management-System> docker ps
CONTAINER ID   IMAGE                             COMMAND                  CREATED          STATUS          PORTS                    NAMES
>>> ee3b550d50de   postgres                          "docker-entrypoint.s…"   2 minutes ago    Up 2 minutes    5432/tcp                 student-management-system-db-client <<<
>>> 1546238049ba   postgres                          "docker-entrypoint.s…"   9 minutes ago    Up 9 minutes    0.0.0.0:5432->5432/tcp   student-management-system-db-server <<<
>>> b2da2d832c31   student-management-system-image   "fastapi run app/mai…"   26 minutes ago   Up 26 minutes   0.0.0.0:8000->8000/tcp   student-management-system-api <<<
```

Running `\q` in the PSQL Client terminal window exits the client and removes the container.

Running `\! {command}` will pass a command from the client cli to the shell.

Example: `\! clear` passes `clear` to the shell.

## Clean up



- Stop the container instances running:
    <tabs>
    <tab title="PowerShell">
    <code-block lang="Bash">
    <![CDATA[
    docker stop `
        student-management-system-api `
        student-management-system-db-server `
        student-management-system-db-client
    ]]>
    </code-block>
    </tab>
    <tab title="Shell">
    <code-block lang="Bash">
    <![CDATA[
    docker stop \
        student-management-system-api \
        student-management-system-db-server \
        student-management-system-db-client
    ]]>
    </code-block>
    </tab>
    </tabs>
    Output:
    ```Bash
    PS C:\Users\Safet\Desktop\Student-Management-System> docker stop `
    >>     student-management-system-api `
    >>     student-management-system-db-server `
    >>     student-management-system-db-client
    student-management-system-api
    student-management-system-db-server
    student-management-system-db-client

    ```
  Running `docker ps` should show no instances.


- Remove the PostgreSQL and FastAPI server containers (if needed) running:
    <tabs>
    <tab title="PowerShell">
    <code-block lang="Bash">
    <![CDATA[
    docker rm `
        student-management-system-api `
        student-management-system-db-server
    ]]>
    </code-block>
    </tab>
    <tab title="Shell">
    <code-block lang="Bash">
    <![CDATA[
    docker rm \
        student-management-system-api \
        student-management-system-db-server
    ]]>
    </code-block>
    </tab>
    </tabs>

    Example:

    ```Bash
    PS C:\Users\Safet\Desktop\Student-Management-System\docs> docker rm `
    >>     student-management-system-api `
    >>     student-management-system-db-server
    student-management-system-api
    student-management-system-db-server

    ```
  Running `docker ps -a` should show no instances, because the client PSQL instance is set to be removed already.

- Remove the PostgreSQL docker image (if needed) running `docker rmi postgres`

- Remove the student-management-system-image docker image (if needed) running `docker rmi student-management-system-image`

Running `docker images` should show no postgres images.

- To remove all networks not currently in use by any containers run:
    ```Bash
    docker network prune
    ```
  Running `docker network ls` should show only the default networks.

## Docker Compose

Docker Compose is a tool for defining and running multi-container Docker applications. It uses a YAML file to configure the application's services, networks, and volumes.

### Set Up Docker Compose

Created a `docker-compose.yml` file in the project root:

```yaml
services:
  postgres:
    image: postgres
    container_name: student-management-system-db-server
    environment:
      POSTGRES_PASSWORD: admin
    networks:
      - student-management-system-network
    ports:
      - "5432:5432"

  student-management-system-api:
    build: .
    container_name: student-management-system-api
    networks:
      - student-management-system-network
    ports:
      - "8000:8000"

networks:
  student-management-system-network:
    driver: bridge
```

Running `docker-compose up` in the project root builds and starts the services defined in the `docker-compose.yml` file.

Running `docker ps`:

```Bash
PS C:\Users\Safet\Desktop\Student-Management-System> docker ps
CONTAINER ID   IMAGE                                                     COMMAND                  CREATED              STATUS              PORTS                    NAMES
14288fb2b4d9   postgres                                                  "docker-entrypoint.s…"   About a minute ago   Up About a minute   0.0.0.0:5432->5432/tcp   student-management-system-db-server
fd5da13396f2   student-management-system-student-management-system-api   "fastapi run app/mai…"   About a minute ago   Up About a minute   0.0.0.0:8000->8000/tcp   student-management-system-api
```

Check the PostgreSQL container in another terminal window using:

```Bash
docker exec -it student-management-system-db-server sh
```

```Bash
PS C:\Users\Safet\Desktop\Student-Management-System> docker exec -it student-management-system-db-server sh
# psql -U postgres
psql (16.4 (Debian 16.4-1.pgdg120+1))
Type "help" for help.

postgres=# select now();
              now
-------------------------------
 2024-08-11 12:30:55.657612+00
(1 row)
```

Check the FastAPI container in another terminal window using:

```Bash
docker exec -it student-management-system-api sh
```

```Bash
PS C:\Users\Safet\Desktop\Student-Management-System\docs> docker exec -it student-management-system-api sh      
/usr/src/app # ls
app               requirements.txt
/usr/src/app # cd app
/usr/src/app/app # ls
__pycache__  main.py
```

Running `docker-compose down` stops and removes the containers defined in the `docker-compose.yml` file.

