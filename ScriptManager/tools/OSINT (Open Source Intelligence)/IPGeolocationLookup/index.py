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


def ip_geolocation_lookup():
    ip = input("Enter the IP address to lookup: ")
    url = f"http://ip-api.com/json/{ip}"

    try:
        response = requests.get(url)
        data = response.json()
        if data['status'] == 'success':
            results = [
                f"IP: {data['query']}",
                f"City: {data['city']}",
                f"Region: {data['regionName']}",
                f"Country: {data['country']}",
                f"Latitude: {data['lat']}",
                f"Longitude: {data['lon']}",
                f"ISP: {data['isp']}"
            ]
            for result in results:
                print(result)
        else:
            results = [f"Error: {data['message']}"]
            print(f"Error: {data['message']}")
    except Exception as e:
        results = [f"Error: {e}"]
        print(f"Error: {e}")

    # Salva i risultati in un file
    save_results_to_file("ip_geolocation_results", results)


ip_geolocation_lookup()
