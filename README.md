# LogFortress 🏰

A powerful debugging tool for Docker containers that provides both command-line and web-based interfaces for managing and monitoring container logs in real-time.

## 🚀 Features

- **Container Log Management**: List and access logs from running Docker containers
- **Custom Log Sources**: Register and monitor custom log files within containers
- **Real-time Log Streaming**: View logs in real-time with live updates
- **Web Interface**: Modern web-based UI for log monitoring
- **Command-line Interface**: Full-featured CLI for automation and scripting
- **Docker Integration**: Seamless integration with Docker daemon
- **Persistent Configuration**: Save custom log source configurations

## 📋 Prerequisites

- Python 3.7 or higher
- Docker daemon running
- Access to Docker socket (for container management)

## 🛠️ Installation

### Using pip (from source)

```bash
# Clone the repository
git clone https://github.com/yourusername/logfortress.git
cd logfortress

# Install dependencies using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### Using Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t logfortress .
docker run -p 2001:2001 -v /var/run/docker.sock:/var/run/docker.sock logfortress
```

## 🎯 Usage

### Command Line Interface

#### List running containers
```bash
python main.py list
```

#### List all log sources (including custom sources)
```bash
python main.py list -a
```

#### Register a custom log source
```bash
python main.py register_custom <container_name> <log_file_path>
```

#### Access container logs
```bash
python main.py access <container_id_or_name>
```

#### Access custom log source
```bash
python main.py access_custom <container_name>
```

#### Start web server
```bash
python main.py web
```

### Web Interface

1. Start the web server:
   ```bash
   python main.py web
   ```

2. Open your browser and navigate to `http://localhost:2001`

3. View and monitor logs through the web interface

## 🔧 Configuration

### Custom Log Sources

You can register custom log files within containers for monitoring:

```bash
# Register a custom log file
python main.py register_custom my-app /var/log/application.log

# Access the custom log
python main.py access_custom my-app
```

### Docker Socket Access

For Docker integration, ensure the Docker socket is accessible:

```bash
# When running in Docker
-v /var/run/docker.sock:/var/run/docker.sock

# When running locally
sudo usermod -aG docker $USER
```

## 📁 Project Structure

```
logfortress/
├── logfortress/           # Main package
│   ├── docker_logs_manager.py  # Core log management logic
│   ├── web_server.py           # Flask web server
│   ├── docker_guards.py        # Docker runtime checks
│   ├── log_persistence.py      # Configuration persistence
│   ├── static/                 # Web assets
│   └── templates/              # HTML templates
├── docs/                  # Documentation
├── main.py               # CLI entry point
├── Dockerfile            # Container definition
├── docker-compose.yml    # Docker Compose configuration
├── pyproject.toml        # Project configuration
└── README.md            # This file
```

## 🐳 Docker Support

LogFortress is designed to work seamlessly with Docker:

- **Container Discovery**: Automatically discovers running containers
- **Log Streaming**: Real-time log streaming from containers
- **Custom Paths**: Monitor specific log files within containers
- **Docker Socket**: Direct integration with Docker daemon

## 🔍 Examples

### Basic Container Monitoring

```bash
# List all running containers
python main.py list

# Monitor logs from a specific container
python main.py access my-web-app

# Start web interface for visual monitoring
python main.py web
```

### Custom Log File Monitoring

```bash
# Register a custom log file
python main.py register_custom my-app /var/log/nginx/access.log

# Monitor the custom log file
python main.py access_custom my-app
```

### Web Interface Usage

1. Start the web server
2. Navigate to the web interface
3. Click on any container to view its logs
4. Custom log sources are highlighted and accessible

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/) for the web interface
- Uses [Docker SDK for Python](https://docker-py.readthedocs.io/) for container management
- Styled with modern web technologies for a great user experience

## 📞 Support

If you encounter any issues or have questions:

1. Check the [documentation](docs/)
2. Search existing [issues](https://github.com/yourusername/logfortress/issues)
3. Create a new issue with detailed information

---

**LogFortress** - Your fortress for Docker log management! 🏰