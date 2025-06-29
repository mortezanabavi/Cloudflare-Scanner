import ipaddress, requests
from multiprocessing import Process
import time, random, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open('ip.txt', 'r') as f:
    ip_ranges = [line.strip() for line in f if line.strip()]

def range_test(network):
    for ip in network:
        try:
            start_time = time.time()
            result = requests.get(f"https://{ip}", timeout=(5, 5), verify=False)
            end_time = time.time()
            ping_time = round((end_time - start_time) * 1000, 2)
            print(f"[+] Good IP: {ip} (Ping: {ping_time} ms)")
        except Exception as e:
            # print(f"[-] {ip} failed: {e}")
            pass

if __name__ == '__main__':
    number_of_ranges = int(input('Enter number of IP ranges to scan randomly : '))
    ip_ranges = random.sample(ip_ranges, min(number_of_ranges, len(ip_ranges)))

    processes = []
    for ip_range in ip_ranges:
        print(f"[+] Starting scan: {ip_range}")
        network = ipaddress.ip_network(ip_range, strict=False)
        p = Process(target=range_test, args=(network,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
