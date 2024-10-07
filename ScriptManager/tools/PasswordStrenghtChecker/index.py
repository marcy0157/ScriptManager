import os
import re


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


def password_strength_checker():
    password = input("Enter a password to check strength: ")
    results = []

    if len(password) < 8:
        results.append("Weak: Password length is less than 8 characters.")
    if not re.search("[a-z]", password):
        results.append("Weak: No lowercase letters.")
    if not re.search("[A-Z]", password):
        results.append("Weak: No uppercase letters.")
    if not re.search("[0-9]", password):
        results.append("Weak: No numbers.")
    if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
        results.append("Weak: No special characters.")

    if not results:
        results.append("Password is strong.")
        print("Password is strong.")
    else:
        for result in results:
            print(result)

    # Salva i risultati in un file
    save_results_to_file("password_strength_results", results)


password_strength_checker()
