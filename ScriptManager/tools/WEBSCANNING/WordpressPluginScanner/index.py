import requests
import os


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


def wordpress_plugin_scanner():
    print("Wordpress Plugin Scanner Tool")
    site_url = input("Enter the WordPress site URL (e.g., http://example.com): ")

    url = f"{site_url}/wp-json/wp/v2/plugins"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            plugins = response.json()
            results = []
            for plugin in plugins:
                plugin_name = plugin.get('name', 'Unknown Plugin')
                plugin_version = plugin.get('version', 'Unknown Version')
                result_str = f"Plugin: {plugin_name}, Version: {plugin_version}"
                print(result_str)
                results.append(result_str)
            save_results_to_file("wordpress_plugin_scanner_results", results)
        else:
            result_str = f"Error: Unable to retrieve plugin list from {site_url} - Status Code: {response.status_code}"
            print(result_str)
            save_results_to_file("wordpress_plugin_scanner_error", [result_str])
    except Exception as e:
        result_str = f"Error: {e}"
        print(result_str)
        save_results_to_file("wordpress_plugin_scanner_error", [result_str])


wordpress_plugin_scanner()
