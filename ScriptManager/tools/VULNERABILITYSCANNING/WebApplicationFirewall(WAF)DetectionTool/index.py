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


def waf_detection_tool():
    print("Web Application Firewall (WAF) Detection Tool")
    target_url = input("Enter the target URL (e.g., http://example.com): ")

    headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/x-www-form-urlencoded'}

    # Payload for potential WAF triggering
    payloads = ["<script>alert(1)</script>", "' OR 1=1 --", "<?php system('id'); ?>"]

    results = []

    for payload in payloads:
        try:
            response = requests.post(target_url, data={"input": payload}, headers=headers)
            if response.status_code == 403 or "waf" in response.text.lower() or "blocked" in response.text.lower():
                result_str = f"WAF detected on {target_url} using payload: {payload}"
                print(result_str)
                results.append(result_str)
            else:
                print(f"No WAF detected with payload: {payload}")
        except Exception as e:
            result_str = f"Error: {e}"
            print(result_str)
            results.append(result_str)

    save_results_to_file("waf_detection_results", results)


waf_detection_tool()
