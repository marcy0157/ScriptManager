import os

import requests


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


def subdomain_finder():
    print("Subdomain Finder")
    print("You need a text file containing a list of subdomains (one per line). Example: subdomains.txt")
    subdomain_file = input("Enter the path to the subdomain file (e.g., subdomains.txt): ")

    try:
        with open(subdomain_file, 'r') as file:
            subdomains = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: The file '{subdomain_file}' was not found.")
        return

    target_domain = input("Enter the target domain: ")

    results = []
    for subdomain in subdomains:
        url = f"http://{subdomain}.{target_domain}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                result_str = f"Subdomain found: {url}"
                print(result_str)
                results.append(result_str)
        except requests.ConnectionError:
            print(f"Subdomain not found: {url}")

    # Salva i risultati in un file
    save_results_to_file("subdomain_finder_results", results)


subdomain_finder()
