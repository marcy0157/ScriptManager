import os

import requests
from bs4 import BeautifulSoup


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


def web_crawler():
    print("Simple Web Crawler Tool")
    print("You need a text file containing a list of starting URLs (one per line). Example: start_urls.txt")
    url_file = input("Enter the path to the URL file (e.g., start_urls.txt): ")

    try:
        with open(url_file, 'r') as file:
            urls = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: The file '{url_file}' was not found.")
        return

    results = []

    for url in urls:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            for link in links:
                full_link = link['href']
                if full_link.startswith('http'):
                    result_str = f"Found link on {url}: {full_link}"
                    print(result_str)
                    results.append(result_str)
        except requests.ConnectionError:
            print(f"Failed to connect to {url}")

    # Salva i risultati in un file
    save_results_to_file("web_crawler_results", results)


web_crawler()
