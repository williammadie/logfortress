# LogFortress CLI

## Basic Commands

### Consult Help Manual

* `python main.py -h`

``` bash
usage: main.py [-h] {list,register_custom,access,access_custom,web} ...

Manage Docker container logs.

positional arguments:
  {list,register_custom,access,access_custom,web}
                        Commands
    list                List all running containers (use -a to include custom sources)
    register_custom     Register a custom log source
    access              Access logs of a container or custom source
    access_custom       Access custom logs of a container
    web                 Start the web server to view logs

options:
  -h, --help            show this help message and exit
```

### List running containers

* `python main.py list`

``` bash
Listing all log sources (running containers):
     ID               Name                      Image                Status 
============================================================================
7b20a1e85db0   logfortress          logfortress-logfortress:latest   running
290464c513ad   pgadmin4_container   dpage/pgadmin4:latest            running
```

### Consult container logs

* `python main.py access`

``` bash
Streaming logs for container: 7b20a1e85db0 Name: logfortress
* Serving Flask app 'logfortress.web_server'
* Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:2001
* Running on http://172.30.0.2:2001
Press CTRL+C to quit
* Restarting with stat
* Debugger is active!
* Debugger PIN: 497-260-602
172.30.0.1 - - [08/Jun/2025 09:33:23] "GET / HTTP/1.1" 200 -
172.30.0.1 - - [08/Jun/2025 09:33:23] "GET /static/styles.css HTTP/1.1" 200 -
172.30.0.1 - - [08/Jun/2025 09:33:24] "GET /static/favicon2.ico HTTP/1.1" 200 -
172.30.0.1 - - [08/Jun/2025 09:33:29] "GET /logs/290464c513ad1c4846bb91f37e0800b1d137498c7e7c97a6a9f14319ece6103f HTTP/1.1" 200 -
172.30.0.1 - - [08/Jun/2025 09:33:29] "GET /static/styles.css HTTP/1.1" 304 -
172.30.0.1 - - [08/Jun/2025 09:33:29] "GET /static/favicon2.ico HTTP/1.1" 304 -
172.30.0.1 - - [08/Jun/2025 09:33:29] "GET /logs/290464c513ad1c4846bb91f37e0800b1d137498c7e7c97a6a9f14319ece6103f/stream HTTP/1.1" 200 -
172.30.0.1 - - [08/Jun/2025 09:33:37] "GET / HTTP/1.1" 200 -
172.30.0.1 - - [08/Jun/2025 09:33:37] "GET /static/styles.css HTTP/1.1" 304 -
172.30.0.1 - - [08/Jun/2025 09:33:38] "GET /static/favicon2.ico HTTP/1.1" 304 -
172.30.0.1 - - [08/Jun/2025 09:33:41] "GET /logs/7b20a1e85db07bcfc2ad518b32d7d160ebcac8f572e0f501c69e094ed2b8c306 HTTP/1.1" 200 -
172.30.0.1 - - [08/Jun/2025 09:33:41] "GET /static/styles.css HTTP/1.1" 304 -
172.30.0.1 - - [08/Jun/2025 09:33:41] "GET /static/favicon2.ico HTTP/1.1" 304 -
```

## Web UI

* `python main.py web` - Start the Web UI.

## Custom Sources

* `python main.py register_custom` - Register a custom source.
* `python main.py access_custom` - Consult logs of a custom source.

