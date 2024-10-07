import os

from scapy.all import sniff


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


def packet_sniffer():
    interface = input("Enter the network interface (e.g., eth0, wlan0): ")
    results = []

    def process_packet(packet):
        packet_summary = packet.summary()
        print(packet_summary)
        results.append(packet_summary)

    sniff(iface=interface, prn=process_packet)

    # Salva i risultati in un file
    save_results_to_file("packet_sniffer_results", results)


packet_sniffer()
