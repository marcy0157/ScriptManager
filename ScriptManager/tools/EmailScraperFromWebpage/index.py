import os
import re

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


def email_scraper():
    print("Email Scraper Tool")
    print("You need a text file containing a list of URLs (one per line). Example: urls.txt")
    url_file = input("Enter the path to the URL file (e.g., urls.txt): ")

    try:
        with open(url_file, 'r') as file:
            urls = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: The file '{url_file}' was not found.")
        return

    email_pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
    results = []

    for url in urls:
        try:
            response = requests.get(url)
            emails = re.findall(email_pattern, response.text)
            if emails:
                for email in emails:
                    result_str = f"Email found on {url}: {email}"
                    print(result_str)
                    results.append(result_str)
            else:
                print(f"No emails found on {url}")
        except requests.ConnectionError:
            print(f"Failed to connect to {url}")

    # Salva i risultati in un file
    save_results_to_file("email_scraper_results", results)


email_scraper()
