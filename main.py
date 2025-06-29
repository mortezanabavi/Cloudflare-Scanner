import ipaddress, requests
from multiprocessing import Process, Pool, cpu_count
import time, random, urllib3
from concurrent.futures import ThreadPoolExecutor
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open('ip.txt', 'r') as f:
    ip_ranges = [line.strip() for line in f if line.strip()]

def check_ip(ip):
    try:
        start_time = time.time()
        headers = {
            "Host": "www.speedtest.net"
        }
        result = requests.get(f"https://{ip}", timeout=(5, 5), headers=headers, verify=False)
        end_time = time.time()
        ping_time = round((end_time - start_time) * 1000, 2)
        print(f"[+] Good IP: {ip} (Ping: {ping_time} ms)")
    except Exception as e:
        # print(f"[-] {ip} failed: {e}")
        pass

def scan_range(ip_range):
    try:
        print(f"[~] Scanning range: {ip_range}")
        network = ipaddress.ip_network(ip_range, strict=False)
        with ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(check_ip, [str(ip) for ip in network])
    except Exception as e:
        print(f"[!] Failed to scan {ip_range}: {e}")

if __name__ == '__main__':
    print(f"[!] Starting scan of {len(ip_ranges)} ranges...")
    with Pool(processes=min(20, cpu_count())) as pool:
        random.shuffle(ip_ranges)
        pool.map(scan_range, ip_ranges)
