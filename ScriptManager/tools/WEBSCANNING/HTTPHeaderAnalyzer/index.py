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


def http_header_analyzer():
    url = input("Enter the URL to analyze headers: ")

    try:
        response = requests.head(url)
        headers = response.headers
        results = [f"{key}: {value}" for key, value in headers.items()]
        for result in results:
            print(result)
    except Exception as e:
        results = [f"Error: {e}"]
        print(f"Error: {e}")

    # Salva i risultati in un file
    save_results_to_file("http_header_analyzer_results", results)


http_header_analyzer()
