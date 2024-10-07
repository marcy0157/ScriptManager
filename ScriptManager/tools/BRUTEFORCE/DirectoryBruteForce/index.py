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


def dir_brute_force():
    print("Directory Brute Force")
    print("You need a text file containing a list of directories or pages (one per line). Example: directories.txt")
    wordlist_file = input("Enter the path to the wordlist file (e.g., directories.txt): ")

    try:
        with open(wordlist_file, 'r') as file:
            wordlist = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: The file '{wordlist_file}' was not found.")
        return

    target_url = input("Enter target URL (e.g., http://example.com): ")

    results = []
    for word in wordlist:
        url = f"{target_url}/{word}"
        response = requests.get(url)
        if response.status_code == 200:
            result_str = f"Found: {url}"
            print(result_str)
            results.append(result_str)
        else:
            print(f"Not Found: {url}")

    # Salva i risultati in un file
    save_results_to_file("dir_brute_force_results", results)


dir_brute_force()
