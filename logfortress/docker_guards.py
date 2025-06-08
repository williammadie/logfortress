from functools import wraps
import docker
from docker.errors import DockerException

def ensure_docker_running(func):
    """
    Decorator to ensure that the Docker daemon is running before executing a function.
    If the Docker daemon is not accessible, it prints an error message and exits.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Attempt to create a low-level API client to check Docker's availability
            client = docker.APIClient()
            client.ping()
        except (DockerException, Exception) as e:
            print("Error: Docker daemon is not running or cannot be reached.")
            print(f"Details: {e}")
            return
        return func(*args, **kwargs)
    return wrapper