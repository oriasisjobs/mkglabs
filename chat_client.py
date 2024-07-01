import socket
import errno
import threading
import sys
from constants import SERVER_IP, SERVER_PORT, HEADER_LENGTH
from helper_functions import extract_message_length, extract_message_header


def create_client_socket(username_message):
    client_socket = socket.socket()
    client_socket.connect((SERVER_IP, SERVER_PORT))
    client_socket.setblocking(False)  # Set socket to non blocking mode
    client_socket.send(username_message)
    return client_socket


def receive_message(client_socket, my_username):
    # Note: the server send 2 parts in the message, with 2 headers, for username and message
    # Process first part of message (that contain username)
    username_header = client_socket.recv(HEADER_LENGTH)
    if not username_header:  # When the server disconnects, it sends empty packet
        print("Connection closed by the server")
        sys.exit()
    username_length = extract_message_length(username_header)
    username = client_socket.recv(username_length).decode("utf-8")
    # Process second part of message (that contain the message itself)
    message_header = client_socket.recv(HEADER_LENGTH)
    message_length = extract_message_length(message_header)
    message = client_socket.recv(message_length).decode("utf-8")

    print(f"\n{username} send >>> {message} \n{my_username} > ")

    return message  # Note: only used by AI chat client


def receive_messages(client_socket, my_username):
    while True:
        try:
            while True:
                receive_message(client_socket, my_username)
        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print("Reading error", str(e))
                return
        except Exception as e:
            print("Reading error", str(e))
            return


def send_message(client_socket, message):
    message = message.encode("utf-8")
    message_header = extract_message_header(message)
    client_socket.send(message_header + message)


def send_messages(client_socket, my_username):
    while True:
        message = input(f"{my_username} > ")
        if message:
            send_message(client_socket, message)


def get_username(prompt):
    my_username = input(prompt)
    encoded_username = my_username.encode("utf-8")
    username_header = extract_message_header(encoded_username)
    return my_username, encoded_username, username_header


def main():
    # Handle username
    my_username, encoded_username, username_header = get_username("Username: ")
    print(f"Hi {my_username}. To send messages to other clients, type a message and press enter. you can send as much messages as you want :)")
    # Create client socket and send first message with username
    client_socket = create_client_socket(username_header + encoded_username)
    # Start threads of receive & send messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, my_username))
    receive_thread.start()
    send_thread = threading.Thread(target=send_messages, args=(client_socket, my_username))
    send_thread.start()


if __name__ == "__main__":
    main()
