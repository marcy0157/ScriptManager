import os
import subprocess


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


def traceroute():
    print("Traceroute Tool")
    target = input("Enter the target domain or IP address: ")

    results = []
    try:
        if os.name == 'nt':  # Windows
            command = f"tracert {target}"
        else:  # Linux/Unix
            command = f"traceroute {target}"

        traceroute_output = subprocess.check_output(command, shell=True).decode()
        results = traceroute_output.splitlines()
        for line in results:
            print(line)

        # Salva i risultati in un file
        save_results_to_file("traceroute_results", results)
    except Exception as e:
        result_str = f"Error executing traceroute: {e}"
        print(result_str)
        save_results_to_file("traceroute_error", [result_str])


traceroute()
