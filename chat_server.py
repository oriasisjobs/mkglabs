import socket
import select
from constants import SERVER_IP, SERVER_PORT, HEADER_LENGTH
from helper_functions import extract_message_length, extract_message, message_to_bytes


def create_server_socket():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow the server to reuse the address, preventing "address already in use" errors on restart
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    print(f"Listening for connections on {SERVER_IP}:{SERVER_PORT}...")
    return server_socket


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not message_header:
            return False
        message_length = extract_message_length(message_header)
        return {
            "header": message_header,
            "data": client_socket.recv(message_length),
        }  # Format: {'header': <message_header>, 'data': <message_data>}
    except:
        return False


def accept_new_client(server_and_clients_sockets, server_socket, clients_to_username):
    client_socket, client_address = server_socket.accept()
    username_message = receive_message(client_socket)
    if username_message is False:  # In case client disconnect before sending message
        return
    server_and_clients_sockets.append(client_socket)
    clients_to_username[client_socket] = username_message
    print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{extract_message(username_message)}")


def free_socket(socket, server_and_clients_sockets, clients_to_username):
    server_and_clients_sockets.remove(socket)
    del clients_to_username[socket]


def handle_closed_connection(server_and_clients_sockets, read_socket, clients_to_username):
    print(f"Closed connection from: {extract_message(clients_to_username[read_socket])}")
    free_socket(read_socket, server_and_clients_sockets, clients_to_username)


def send_message_to_other_client(read_socket, message, clients_to_username):
    username_message = clients_to_username[read_socket]
    print(f"Received message from {extract_message(username_message)}: {extract_message(message)}")
    for client_socket in clients_to_username:
        if client_socket != read_socket:
            client_socket.send(message_to_bytes(username_message) + message_to_bytes(message))


def accept_new_message(server_and_clients_sockets, read_socket, clients_to_username):
    message = receive_message(read_socket)
    if (message is False):  # When a client disconnects, it sends empty packet, so receive_message will return False for it
        handle_closed_connection(server_and_clients_sockets, read_socket, clients_to_username)
        return
    send_message_to_other_client(read_socket, message, clients_to_username)


def main():
    # Init Server
    server_socket = create_server_socket()
    server_and_clients_sockets = [server_socket]  # After clients connect to the server, they will be added to this list
    clients_to_username = {}  # used for message identification, for improved user experience. Note: username is not a string, it is a message containig a header and a username
    # The main loop (handle new connection and forward messages)
    while True:
        read_sockets, _, exception_sockets = select.select(server_and_clients_sockets, [], server_and_clients_sockets)
        # Handle messages ready read sockets
        for read_socket in read_sockets:
            if read_socket == server_socket:
                accept_new_client(server_and_clients_sockets, server_socket, clients_to_username)
            else:
                accept_new_message(server_and_clients_sockets, read_socket, clients_to_username)
        # Handle exception of sockets
        for exception_socket in exception_sockets:
            free_socket(exception_socket, server_and_clients_sockets, clients_to_username)


if __name__ == "__main__":
    main()
