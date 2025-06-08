import argparse
from logfortress.docker_logs_manager import DockerLogsManager
from logfortress.web_server import start_server


def handle_list(manager: DockerLogsManager, all_sources: bool) -> None:
    """Handle the 'list' command."""
    if all_sources:
        manager.list_all_log_sources()
    else:
        manager.list_log_sources()


def handle_register_custom(manager: DockerLogsManager, container_name: str, log_file_path: str) -> None:
    """Handle the 'register_custom' command."""
    manager.register_custom(container_name, log_file_path)


def handle_access(manager: DockerLogsManager, container_id_or_name: str) -> None:
    """Handle the 'access' command."""
    manager.access_log_source(container_id_or_name)


def handle_access_custom(manager: DockerLogsManager, container_name: str) -> None:
    """Handle the 'access_custom' command."""
    manager.access_custom_log_source(container_name)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Manage Docker container logs.")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # List command
    list_parser = subparsers.add_parser(
        'list', help='List all running containers (use -a to include custom sources)')
    list_parser.add_argument(
        '-a', '--all', action='store_true', help='Include custom log sources')

    # Register custom command
    register_parser = subparsers.add_parser(
        'register_custom', help='Register a custom log source')
    register_parser.add_argument(
        'container_name', help='Name of the Docker container')
    register_parser.add_argument(
        'log_file_path', help='Path to the log file inside the container')

    # Access command
    access_parser = subparsers.add_parser(
        'access', help='Access logs of a container or custom source')
    access_parser.add_argument(
        'container_id_or_name', help='The container ID or name to access logs from')

    # Access custom command
    access_custom_parser = subparsers.add_parser(
        'access_custom', help='Access custom logs of a container')
    access_custom_parser.add_argument(
        'container_name', help='The container name to access custom logs from')

    # Start web server command
    subparsers.add_parser(
        'web', help='Start the web server to view logs')

    args = parser.parse_args()

    try:
        manager = DockerLogsManager()
    except RuntimeError as e:
        print(e)
        return

    if args.command == 'list':
        handle_list(manager, args.all)
    elif args.command == 'register_custom':
        handle_register_custom(
            manager, args.container_name, args.log_file_path)
    elif args.command == 'access':
        handle_access(manager, args.container_id_or_name)
    elif args.command == 'access_custom':
        handle_access_custom(manager, args.container_name)
    elif args.command == 'web':
        start_server()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
