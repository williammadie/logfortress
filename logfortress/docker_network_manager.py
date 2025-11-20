import docker


class DockerNetworkManager:
    """
    Class to manage Docker network data, including listing networks,
    and accessing container information within those networks.
    """

    def __init__(self) -> None:
        """Initialize the Docker client."""
        try:
            self.client = docker.from_env()
        except docker.errors.DockerException as e:
            raise RuntimeError(
                "Docker daemon is not running or cannot be reached. 🚫") from e

    def get_docker_networks(self):
        """Retrieve the list of Docker networks and their container associations."""
        networks = self.client.networks.list()
        network_data = []

        for network in networks:
            network.reload()
            containers = network.attrs['Containers']
            container_info = []

            for container_id, container_details in containers.items():
                container_name = container_details['Name']
                container_info.append(
                    {'id': container_id, 'name': container_name})

            network_data.append({
                'id': network.id,
                'name': network.name,
                'containers': container_info
            })
        return network_data
