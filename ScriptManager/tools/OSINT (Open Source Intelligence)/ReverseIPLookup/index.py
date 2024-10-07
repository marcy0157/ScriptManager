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


def reverse_ip_lookup():
    print("Reverse IP Lookup Tool")
    ip = input("Enter the IP address: ")

    url = f"https://api.hackertarget.com/reverseiplookup/?q={ip}"
    response = requests.get(url)

    if response.status_code == 200:
        results = response.text.splitlines()
        for result in results:
            print(result)
        # Salva i risultati in un file
        save_results_to_file("reverse_ip_lookup_results", results)
    else:
        print("Error retrieving data.")


reverse_ip_lookup()
