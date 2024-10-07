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


def xss_scanner():
    print("XSS Vulnerability Scanner Tool")
    url = input("Enter the target URL with a query parameter (e.g., http://example.com/search?q=): ")
    test_script = "<script>alert('XSS');</script>"

    target_url = f"{url}{test_script}"

    try:
        response = requests.get(target_url)
        if test_script in response.text:
            result_str = f"XSS Vulnerability detected on {url}"
            print(result_str)
            save_results_to_file("xss_vulnerability_results", [result_str])
        else:
            print(f"No XSS vulnerability detected on {url}")
    except Exception as e:
        result_str = f"Error: {e}"
        print(result_str)
        save_results_to_file("xss_scanner_error", [result_str])


xss_scanner()
