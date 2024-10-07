import os

import scapy.all as scapy


def save_results_to_file(base_name, results):
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)

    count = 0
    while True:
        filename = f"{base_name}{count}.txt" if count > 0 else f"{base_name}.txt"
        filepath = os.path.join(results_dir, filename)
        if not os.path.exists(filepath):
            break
        count += 1

    try:
        with open(filepath, 'a') as f:
            for result in results:
                f.write(result + '\n')
        print(f"Results saved in {filepath}")
    except Exception as e:
        print(f"Error writing file: {e}")


def arp_scanner():
    print("ARP Scanner Tool")
    network_range = input("Enter the network range (e.g., 192.168.1.0/24): ")

    try:
        arp_request = scapy.ARP(pdst=network_range)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

        results = []
        for element in answered_list:
            result_str = f"IP: {element[1].psrc} - MAC: {element[1].hwsrc}"
            print(result_str)
            results.append(result_str)

        # Salva i risultati in un file
        save_results_to_file("arp_scanner_results", results)
    except Exception as e:
        result_str = f"Error: {e}"
        print(result_str)
        save_results_to_file("arp_scanner_error", [result_str])


arp_scanner()
