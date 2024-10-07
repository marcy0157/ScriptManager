import os

import dns.resolver


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


def dns_brute_force():
    print("DNS Brute Force Tool")
    print("You need a text file containing a list of potential subdomains (one per line). Example: subdomains.txt")
    subdomain_file = input("Enter the path to the subdomain file (e.g., subdomains.txt): ")
    domain = input("Enter the domain to brute force (e.g., example.com): ")

    try:
        with open(subdomain_file, 'r') as file:
            subdomains = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: The file '{subdomain_file}' was not found.")
        return

    resolver = dns.resolver.Resolver()
    results = []

    for subdomain in subdomains:
        full_domain = f"{subdomain}.{domain}"
        try:
            answers = resolver.resolve(full_domain)
            for rdata in answers:
                result_str = f"Found: {full_domain} -> {rdata}"
                print(result_str)
                results.append(result_str)
        except dns.resolver.NXDOMAIN:
            print(f"{full_domain} does not exist.")
        except Exception as e:
            result_str = f"Error checking {full_domain}: {e}"
            print(result_str)
            results.append(result_str)

    # Salva i risultati in un file
    save_results_to_file("dns_brute_force_results", results)


dns_brute_force()
