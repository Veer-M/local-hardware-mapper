# Local hardware mapper

This program checks addresses on a local network to help find controllers and other devices. It looks for open HTTP and MQTT ports and saves the addresses it finds.

## How it works

A subnet is a group of network addresses. The default subnet is `192.168.1.0/24`, which has 254 normal host addresses. For each address, the program tries port 80 for HTTP and port 1883 for MQTT. These ports are often used by web interfaces and messaging services.

It uses threads to check several addresses at once. Each port gets a 0.5-second timeout by default. A timeout is the longest the program waits for one connection attempt. The full scan can take longer than one second because each address has several ports to check and the computer has to manage the threads.

The results are saved in `devices.json`. Each entry has an IP address and a list of ports that accepted a connection.

## What the results mean

An open port means something accepted the connection. It does not prove that the device is a microcontroller or that it is running the expected service. The program finds reachable addresses and ports. It does not show the physical cables or wireless links between devices.

Only scan networks you own or have permission to check. The program accepts private IPv4 networks and loopback addresses, which point back to your own computer. It limits each scan to a /24 subnet or a smaller group of addresses.

## Try it

Use Python 3.11 or newer. Open a terminal in this project's folder and create a virtual environment. This keeps its packages separate from your other Python projects.

```sh
python -m venv .venv
```

On Windows, activate it with this command.

```sh
.venv\Scripts\activate
```

On macOS or Linux, use this command instead.

```sh
source .venv/bin/activate
```

Then install the packages the project needs.

```sh
python -m pip install -r requirements.txt
```

```sh
python network_mapper.py 192.168.1.0/24
python network_mapper.py 192.168.0.0/24 --ports 80 1883 8080 --workers 32
```

Change the subnet to match your network. Use `--ports` to choose ports, `--timeout` to change the wait per port, and `--workers` to change how many addresses can be checked at once.

## Tests

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

The tests open a real port on the same computer and check that the mapper finds it. They also check the subnet limits. They do not scan other devices on the network.
