import os

import dns.query
import dns.resolver
import dns.zone


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


def dns_zone_transfer_test():
    print("DNS Zone Transfer Tester Tool")
    domain = input("Enter the domain (e.g., example.com): ")

    # Ottenere i nameserver per il dominio
    try:
        nameservers = dns.resolver.resolve(domain, 'NS')
        nameserver_list = [str(ns) for ns in nameservers]
        print(f"Found nameservers: {', '.join(nameserver_list)}")
    except Exception as e:
        print(f"Error resolving nameservers: {e}")
        return

    results = []

    # Testa il trasferimento di zona per ogni nameserver
    for ns in nameserver_list:
        ns = ns.strip('.')  # Rimuovere eventuali punti finali nei nomi dei nameserver
        print(f"Testing zone transfer for {ns}...")
        try:
            zone = dns.zone.from_xfr(dns.query.xfr(ns, domain))
            for name, node in zone.nodes.items():
                record = zone[name].to_text(name)
                result_str = f"Record from {ns}: {record}"
                print(result_str)
                results.append(result_str)
        except dns.exception.FormError:
            result_str = f"Zone transfer not allowed on {ns}"
            print(result_str)
            results.append(result_str)
        except Exception as e:
            result_str = f"Error testing {ns}: {e}"
            print(result_str)
            results.append(result_str)

    # Salva i risultati in un file
    save_results_to_file("dns_zone_transfer_results", results)


dns_zone_transfer_test()
