import ftplib
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

def ftp_anonymous_login_scanner():
    print("FTP Anonymous Login Scanner")
    target_ip = input("Enter the target FTP server IP: ")

    try:
        ftp = ftplib.FTP(target_ip)
        ftp.login()
        result_str = f"FTP anonymous login allowed on {target_ip}"
        print(result_str)
        results = [result_str]
        ftp.quit()
    except ftplib.error_perm:
        result_str = f"FTP anonymous login not allowed on {target_ip}"
        print(result_str)
        results = [result_str]
    except Exception as e:
        result_str = f"Error: {e}"
        print(result_str)
        results = [result_str]

    save_results_to_file("ftp_anonymous_login_results", results)

ftp_anonymous_login_scanner()
