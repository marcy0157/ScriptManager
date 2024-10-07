import os
import socket


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


def dns_lookup():
    domain = input("Enter the domain to lookup: ")
    results = []
    try:
        ip = socket.gethostbyname(domain)
        result_str = f"IP Address of {domain} is {ip}"
        print(result_str)
        results.append(result_str)
    except socket.error as err:
        result_str = f"Error: {err}"
        print(result_str)
        results.append(result_str)

    # Salva i risultati in un file
    save_results_to_file("dns_lookup_results", results)


dns_lookup()
