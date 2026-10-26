# Local hardware mapper

This checks a local subnet for open HTTP and MQTT ports and saves the results as JSON. It can help locate a headless controller when its address is unknown.

## Run it

Use Python 3.11 or newer. Run these commands from this repository's folder.

```sh
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
# source .venv/bin/activate
python -m pip install -r requirements.txt
```

```sh
python network_mapper.py 192.168.1.0/24
python network_mapper.py 192.168.0.0/24 --ports 80 1883 8080 --workers 32
```

## How it works and current limits

Only scan networks you own or have permission to inspect. An open port is a reachable endpoint, not proof that it is an IoT device or that the expected service is running. This discovers endpoints rather than physical network links. A half-second timeout is per port; scheduling and network conditions mean a whole scan is not guaranteed to finish in one second. Tests use loopback only.

## Tests

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Tests open a real loopback listener, discover its port, and check subnet restrictions. They do not scan the surrounding network.
