# import requests
# from bs4 import BeautifulSoup
# import time
# import os
#
#
# def google_search(query):
#     url = f"https://www.google.com/search?q={query}"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#     }
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         return response.text
#     return None
#
#
# def parse_results(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     links = []
#     for g in soup.find_all('div', class_='g'):
#         anchor = g.find('a')
#         if anchor and anchor['href']:
#             links.append(anchor['href'])
#     return links
#
#
# def generate_unique_filename(base_name, directory):
#     count = 0
#     while True:
#         filename = f"{base_name}{count}.txt" if count > 0 else f"{base_name}.txt"
#         filepath = os.path.join(directory, filename)
#         if not os.path.exists(filepath):
#             return filepath
#         count += 1
#
#
# def main(query_file):
#     # Chiede l'input del sito da analizzare
#     site = input("Inserisci il sito da analizzare (es: example.com): ").strip()
#
#     # Leggi le query dal file
#     try:
#         with open(query_file, 'r') as f:
#             queries = f.readlines()
#     except FileNotFoundError:
#         print(f"File {query_file} non trovato.")
#         return
#
#     results = []
#
#     # Crea la cartella "results" se non esiste
#     results_dir = "results"
#     os.makedirs(results_dir, exist_ok=True)
#
#     # Genera un file di output unico nella cartella "results"
#     result_file = generate_unique_filename("risultati", results_dir)
#
#     for query in queries:
#         query = query.strip()
#         full_query = f"site:{site} {query}"
#         print(f"Eseguendo query: {full_query}")
#
#         html = google_search(full_query)
#         if html:
#             links = parse_results(html)
#             results.append({
#                 'query': full_query,
#                 'results': links
#             })
#
#         # Evita di essere bloccato con una pausa tra le richieste
#         time.sleep(4)
#
#     # Scrive i risultati nel file di output
#     try:
#         with open(result_file, 'w') as f:
#             for result in results:
#                 f.write(f"Query: {result['query']}\n")
#                 f.write("Risultati:\n")
#                 for link in result['results']:
#                     f.write(f"- {link}\n")
#                 f.write("\n")
#         print(f"Risultati salvati in {result_file}")
#     except Exception as e:
#         print(f"Errore durante la scrittura del file: {e}")
#
#
# if __name__ == "__main__":
#     query_file = "query.txt"
#     main(query_file)
