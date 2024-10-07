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


def open_redirect_tester():
    print("Open Redirect Tester Tool")
    print("You need a text file containing a list of base URLs (one per line). Example: urls.txt")
    url_file = input("Enter the path to the URL file (e.g., urls.txt): ")
    malicious_url = input("Enter the malicious URL for testing (e.g., http://malicious.com): ")

    try:
        with open(url_file, 'r') as file:
            urls = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: The file '{url_file}' was not found.")
        return

    results = []

    for base_url in urls:
        redirect_url = f"{base_url}?redirect={malicious_url}"
        try:
            response = requests.get(redirect_url, allow_redirects=False)
            if response.status_code in [301, 302] and 'Location' in response.headers:
                result_str = f"Potential Open Redirect: {base_url} redirects to {malicious_url}"
                print(result_str)
                results.append(result_str)
            else:
                print(f"No open redirect on {base_url}")
        except requests.RequestException as e:
            result_str = f"Error testing {base_url}: {e}"
            print(result_str)
            results.append(result_str)

    # Salva i risultati in un file
    save_results_to_file("open_redirect_tester_results", results)


open_redirect_tester()
