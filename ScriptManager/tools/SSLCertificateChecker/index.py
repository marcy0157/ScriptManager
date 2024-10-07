import os
import socket
import ssl
from datetime import datetime


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


def ssl_certificate_checker():
    print("SSL Certificate Checker Tool")
    domain = input("Enter the domain (e.g., example.com): ")

    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                expiry_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                days_left = (expiry_date - datetime.utcnow()).days
                result_str = f"Domain: {domain} - SSL certificate expires in {days_left} days (on {expiry_date})"
                print(result_str)
                results = [result_str]
                # Salva i risultati in un file
                save_results_to_file("ssl_certificate_checker_results", results)
    except Exception as e:
        result_str = f"Error: {e}"
        print(result_str)
        results = [result_str]
        save_results_to_file("ssl_certificate_checker_results", results)


ssl_certificate_checker()
