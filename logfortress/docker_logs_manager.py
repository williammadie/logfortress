import logging
import shutil
import docker
from logfortress.log_persistence import LogPersistence
from texttable import Texttable

from logfortress.docker_guards import ensure_docker_running

logger = logging.getLogger(__name__)


class DockerLogsManager:
    """
    Class to manage Docker container logs, including listing containers,
    registering new containers, and accessing logs of existing containers.
    """

    def __init__(self) -> None:
        """Initialize the Docker client."""
        try:
            self.client = docker.from_env()
        except docker.errors.DockerException as e:
            raise RuntimeError(
                "Docker daemon is not running or cannot be reached. 🚫") from e
        self.persistence = LogPersistence()
        self.custom_log_sources = self.persistence.load()

    def reload_custom_log_sources(self) -> None:
        """Reload custom log sources from the persistence file."""
        self.custom_log_sources = self.persistence.load()

    def _create_table(self, headers: list, rows: list) -> str:
        """Create a formatted table for display.

        :param headers: List of column headers.
        :param rows: List of rows, where each row is a list of column values.
        :return: Formatted table as a string.
        """
        terminal_width, _ = shutil.get_terminal_size((80, 24))
        table = Texttable(max_width=terminal_width)
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype(['t' for _ in headers])  # Text columns
        table.set_cols_align(['l' for _ in headers])  # Left align
        table.header(headers)
        for row in rows:
            table.add_row(row)
        return table.draw()

    def _print_centered_bold(self, text: str) -> None:
        """Print a centered and bolded text."""
        terminal_width, _ = shutil.get_terminal_size((80, 24))
        bold_text = f"\033[1m{text}\033[0m"  # ANSI escape code for bold
        padding = (terminal_width - len(text)) // 2
        # Center the text with padding
        # print(' ' * max(0, padding) + bold_text)
        print(bold_text)

    @ensure_docker_running
    def list_log_sources(self) -> None:
        """List all running Docker containers in a tabular format."""
        print("Listing all log sources (running containers):")
        containers = self.client.containers.list()

        rows = []
        for container in containers:
            image_tag = container.image.tags[0] if container.image.tags else "<no tag>"
            rows.append([container.id[:12], container.name,
                        image_tag, container.status])

        print(self._create_table(['ID', 'Name', 'Image', 'Status'], rows))

    @ensure_docker_running
    def list_all_log_sources(self) -> None:
        """List all log sources, including custom log sources."""
        self.reload_custom_log_sources()
        self._print_centered_bold("Log sources Table")
        containers = self.client.containers.list()

        rows = []
        for container in containers:
            image_tag = container.image.tags[0] if container.image.tags else "<no tag>"
            rows.append([container.id[:12], container.name,
                        image_tag, container.status])

        print(self._create_table(['ID', 'Name', 'Image', 'Status'], rows))

        if self.custom_log_sources:
            print("\n")
            self._print_centered_bold("Custom log sources Table")
            custom_rows = []
            for name, path in self.custom_log_sources.items():
                try:
                    container = self.client.containers.get(name)
                    image_tag = container.image.tags[0] if container.image.tags else "<no tag>"
                    custom_rows.append(
                        [container.id[:12], name, image_tag, path, container.status])
                except docker.errors.NotFound:
                    print(f"Warning: Container '{name}' not found. Skipping.")
                    custom_rows.append(["N/A", name, "N/A", path, "N/A"])

            print(self._create_table(
                ['ID', 'Container Name', 'Image', 'Log File Path', 'Status'], custom_rows))
        else:
            print("\nNo custom log sources registered.")

    @ensure_docker_running
    def register_custom(self, container_name: str, log_file_path: str) -> None:
        """
        Register a custom log source by specifying a container and a log file path.

        :param container_name: Name of the Docker container.
        :param log_file_path: Path to the log file inside the container.
        """
        try:
            container = self.client.containers.get(container_name)
            self.custom_log_sources[container_name] = log_file_path
            self.persistence.save(self.custom_log_sources)
            print(
                f"Registered custom log source for container '{container_name}' at path '{log_file_path}' ✅")
        except Exception as e:
            print(f"Error registering custom log source: {e}")

    def access_custom_log_source(self, container_name: str) -> None:
        """
        Access logs from a custom log source in a container.

        :param container_name: The container name to access custom logs from.
        """
        if container_name not in self.custom_log_sources:
            print(
                f"No custom log source registered for container '{container_name}'")
            return

        log_file_path = self.custom_log_sources[container_name]
        try:
            container = self.client.containers.get(container_name)
            print(
                f"Streaming custom logs for container: {container_name} from file: {log_file_path}")
            exec_log = container.exec_run(
                f"tail -f {log_file_path}", stream=True)
            for log in exec_log.output:
                print(log.decode('utf-8').strip())
        except Exception as e:
            print(f"Error accessing custom logs: {e}")

    @ensure_docker_running
    def access_log_source(self, container_id_or_name: str) -> None:
        """
        Stream logs from a specific container.

        :param container_id_or_name: The container ID or name to access logs from.
        """
        try:
            container = self.client.containers.get(container_id_or_name)
            print(
                f"Streaming logs for container: {container.id[:12]} Name: {container.name}")
            for log in container.logs(stream=True):
                print(log.decode('utf-8').strip())
        except Exception as e:
            print(f"Error accessing logs: {e}")
