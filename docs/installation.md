# Installation

It is possible to install *LogFortress* from PyPi or from DockerHub:

- If you want to use the CLI, use the Python package approach.
- If you want a **turnkey solution**, use the Docker container approach. It will immediately start the Web UI and let you debug your containers.

## Install from PyPi

``` bash
pip install logfortress
```

## Installation from DockerHub

**Step n°1:** Write a docker compose file.

``` yaml
services:
  logfortress:
    build: .
    container_name: logfortress
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock # (1)
    ports:
      - "2001:2001"
```

1.  The container mounts the Docker socket `/var/run/docker.sock` to allow the application to communicate with the host Docker daemon. This is required because the library uses the Docker API Client to access containers information.

**Step n°2:** Acess the Web UI at <a href="http://127.0.0.1:2001/" target="_blank">http://127.0.0.1:2001/</a>.


