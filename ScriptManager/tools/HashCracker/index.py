import hashlib
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


def md5_hash_cracker():
    hash_value = input("Enter the MD5 hash to crack: ")
    wordlist = input("Enter comma-separated password list: ").split(',')

    results = []
    for word in wordlist:
        word_hash = hashlib.md5(word.encode()).hexdigest()
        if word_hash == hash_value:
            result_str = f"Password found: {word}"
            print(result_str)
            results.append(result_str)
            break
    else:
        print("Password not found.")
        results.append("Password not found.")

    # Salva i risultati in un file
    save_results_to_file("md5_hash_cracker_results", results)


md5_hash_cracker()
