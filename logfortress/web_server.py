import docker
from flask import Flask, render_template, Response
from logfortress.docker_link import DockerLink
from logfortress.docker_logs_manager import DockerLogsManager
from logfortress.docker_network_manager import DockerNetworkManager
from logfortress.ui.utils import UserInterfaceUtils

app = Flask(__name__)
manager = DockerLogsManager()
network_manager = DockerNetworkManager()


@app.route('/')
def list_sources():
    manager.reload_custom_log_sources()
    containers = manager.client.containers.list()
    custom_sources = []

    for name, path in manager.custom_log_sources.items():
        try:
            container = manager.client.containers.get(name)
            image_tag = container.image.tags[0] if container.image.tags else "<no tag>"
            custom_sources.append({
                'id': container.id[:12],
                'name': name,
                'image': image_tag,
                'status': container.status,
                'log_file_path': path
            })
        except docker.errors.NotFound:
            custom_sources.append({
                'id': 'N/A',
                'name': name,
                'image': 'N/A',
                'status': 'N/A',
                'log_file_path': path
            })

    return render_template(
        'list_sources.html',
        containers=containers,
        custom_sources=custom_sources,
        get_status_emoji=UserInterfaceUtils.get_status_emoji
    )


def generate_log_stream(container_id, is_custom, log_file_path=None):
    """Generate a log stream for a container."""
    try:
        container = manager.client.containers.get(container_id)

        # Check if the container is running before starting the log stream
        if container.status != 'running':
            yield f"data: Container {container.name} is not running.\n\n"
            return

        if is_custom and log_file_path:
            # Stream logs from a custom log file path inside the container
            exec_log = container.exec_run(
                f"tail -f {log_file_path}", stream=True)
            for log in exec_log.output:
                log_data = log.decode('utf-8').rstrip()
                yield f"data: {log_data}\n\n"
        else:
            # Stream standard container logs
            for log in container.logs(stream=True):
                log_data = log.decode('utf-8').rstrip()
                yield f"data: {log_data}\n\n"

    except docker.errors.NotFound:
        yield f"data: Container {container_id} not found.\n\n"
    except Exception as e:
        yield f"data: Error streaming logs: {e}\n\n"


@app.route('/logs/<container_id>')
def view_logs(container_id):
    """Stream logs for a container."""
    try:
        # Attempt to fetch the container details
        container = manager.client.containers.get(container_id)
        container_name = container.name
        container_status = container.status
        image_tag = container.image.tags[0] if container.image.tags else "<no tag>"
    except docker.errors.NotFound:
        # If the container is not found, use placeholders
        container_name = "N/A"
        container_status = "N/A"
        image_tag = "N/A"

    # Determine if the container is a custom log source
    is_custom = container_id in manager.custom_log_sources
    log_file_path = manager.custom_log_sources.get(container_id)

    return render_template(
        'view_logs.html',
        container_id=container_id,
        container_name=container_name,
        container_status=container_status,
        is_custom=is_custom,
        log_file_path=log_file_path,
        get_status_emoji=UserInterfaceUtils.get_status_emoji,
        image_tag=image_tag,
        image_url=DockerLink(image_tag).build_link()
    )


@app.route('/logs/<container_id>/stream')
def stream_logs(container_id):
    """Stream logs for a container."""
    is_custom = container_id in manager.custom_log_sources
    log_file_path = manager.custom_log_sources.get(container_id)

    return Response(generate_log_stream(container_id, is_custom, log_file_path),
                    mimetype='text/event-stream')


@app.route('/network-map')
def map_docker_networks():
    """ Render a map of Docker networks and their containers. """
    docker_networks = network_manager.get_docker_networks()
    return render_template('network_map.html', networks=docker_networks)


def start_server():
    """ Start the Flask web server. """
    app.run(host='0.0.0.0', port=2001, debug=True)
