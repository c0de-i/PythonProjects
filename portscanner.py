import socket
import pyfiglet
import argparse
import ipaddress
from concurrent.futures import ThreadPoolExecutor

# banner
banner = pyfiglet.figlet_format("PORT SCANNER BY CODE_I", font="digital")
print(banner)

# inputs
parser = argparse.ArgumentParser()
parser.add_argument("host", help="IP range or hostname")
parser.add_argument("--ports", help="ports to scan (e.g. 80,443)")
parser.add_argument("--mode", type=int, choices=[1, 2, 3, 4], default=1, help="1: 1-1024, 2: selected common ports, 3: custom range, 4: specific ports")
args = parser.parse_args()

# get ip list
try:
    if '/' in args.host:
        network = ipaddress.ip_network(args.host, strict=False)
        host_list = [str(ip) for ip in network.hosts()]
    else:
        ip = socket.gethostbyname(args.host)
        host_list = [ip]
except (ValueError, socket.gaierror):
    print("Invalid host input.")
    quit()

# get port list
if args.ports:
    port_list = [int(port) for port in args.ports.split(",")]
else:
    if args.mode == 1:
        port_list = range(1, 1025)
    elif args.mode == 2:
        port_list = [20, 21, 22, 23, 25, 53, 80, 110, 123, 137, 143, 161, 162, 443, 3306]
    elif args.mode == 3:
        port_range1 = int(input("Enter port range from: "))
        port_range2 = int(input("Enter port range to: "))
        port_list = range(port_range1, port_range2+1)
    else:
        print("Invalid mode input.")
        quit()

# port scanning
def portscan(ip_port):
    ip, port = ip_port
    try:
        with socket.create_connection((ip, port), timeout=1) as s:
            with results_lock:
                if ip not in results:
                    results[ip] = []
                results[ip].append(port)
    except (socket.timeout, ConnectionRefusedError):
        pass

# get port names
def get_port_names(port_list):
    port_names = {}
    for port in port_list:
        try:
            service = socket.getservbyport(port)
            port_names[port] = service
        except OSError:
            port_names[port] = ""
    return port_names

# scan hosts
results = {}
results_lock = ThreadPoolExecutor(max_workers=50)
with results_lock:
    for ip in host_list:
        try:
            socket.inet_aton(ip)
        except socket.error:
            print(f"Invalid IP address: {ip}")
            continue
        results_lock.map(portscan, [(ip, port) for port in port_list])

# print results
if not results:
    print("\nThere are no open ports.")
else:
    port_names = get_port_names(port_list)
    for ip, ports in results.items():
        if not ports:
            print(f"\n{ip}: No open ports.")
        else:
            open_ports = [f"{port} ({port_names.get(port)})" for port in ports]
            print(f"\nHost IP: {ip}: There are {len(ports)} open ports: {', '.join(open_ports)}")
