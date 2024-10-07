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


def ping_sweep():
    network = input("Enter the network (e.g., 192.168.1): ")

    results = []
    for i in range(1, 255):
        ip = f"{network}.{i}"
        response = os.system(f"ping -c 1 {ip}")
        if response == 0:
            result_str = f"Host {ip} is up."
            print(result_str)
            results.append(result_str)
        else:
            print(f"Host {ip} is down.")

    # Salva i risultati in un file
    save_results_to_file("ping_sweep_results", results)


ping_sweep()
