import argparse
import ipaddress
import json
import math
from pathlib import Path
import socket
import threading
from queue import Empty, Queue

def probe(address, ports=(80,1883), timeout=0.5):
    opened = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.settimeout(timeout)
            try:
                if connection.connect_ex((str(address), port)) == 0:
                    opened.append(port)
            except OSError:
                continue
    return opened

def scan(subnet='192.168.1.0/24', ports=(80,1883), timeout=0.5, workers=254):
    network = ipaddress.ip_network(subnet, strict=False)
    private_blocks = [ipaddress.ip_network(n) for n in ('10.0.0.0/8','172.16.0.0/12','192.168.0.0/16','127.0.0.0/8')]
    if network.version != 4 or not any(network.subnet_of(block) for block in private_blocks):
        raise ValueError('Choose an RFC1918 private or loopback IPv4 subnet')
    if network.num_addresses > 256:
        raise ValueError('Choose a /24 or smaller subnet')
    if not ports or any(not 1 <= p <= 65535 for p in ports):
        raise ValueError('Ports must be between 1 and 65535')
    if not math.isfinite(timeout) or timeout <= 0 or not 1 <= workers <= 254:
        raise ValueError('Timeout must be positive and workers between 1 and 254')
    tasks = Queue()
    for address in network.hosts():
        tasks.put(str(address))
    found = []
    lock = threading.Lock()
    def worker():
        while True:
            try:
                address = tasks.get_nowait()
            except Empty:
                return
            try:
                opened = probe(address, ports, timeout)
                if opened:
                    with lock:
                        found.append({'ip':address,'ports':opened})
            finally:
                tasks.task_done()
    threads = [threading.Thread(target=worker) for _ in range(min(workers,tasks.qsize()))]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return sorted(found,key=lambda item:ipaddress.ip_address(item['ip']))

def main():
    parser = argparse.ArgumentParser(description='Find local HTTP and MQTT endpoints')
    parser.add_argument('subnet', nargs='?', default='192.168.1.0/24')
    parser.add_argument('--ports', type=int, nargs='+', default=[80,1883])
    parser.add_argument('--timeout', type=float, default=0.5)
    parser.add_argument('--workers', type=int, default=254)
    parser.add_argument('--output', default='devices.json')
    args = parser.parse_args()
    try:
        results = scan(args.subnet,args.ports,args.timeout,args.workers)
    except ValueError as error:
        parser.error(str(error))
    text = json.dumps(results,indent=2)
    Path(args.output).write_text(text+'\n',encoding='utf-8')
    print(text)

if __name__ == '__main__':
    main()
