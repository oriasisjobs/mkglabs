import errno
import threading
import time
import sys
from chat_client import create_client_socket, get_username, send_message, receive_message
from helper_functions import get_ai_generated_string, get_ai_generated_response


def receive_messages(client_socket, response_mode, response_frequency):
    message_count = 0
    messages = ""
    while True:
        try:
            while True:
                message = receive_message(client_socket, "")
                messages += message + ","
                message_count += 1
                if response_mode == "lines" and message_count % response_frequency == 0:
                    send_message(client_socket, get_ai_generated_response(messages))
                    messages = ""
        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print("Reading error", str(e))
                sys.exit()
        except Exception as e:
            print("Reading error", str(e))
            sys.exit()


def send_periodic_messages(client_socket, response_mode, response_frequency):
    while True:
        if response_mode == "seconds":
            time.sleep(response_frequency)
            send_message(client_socket, get_ai_generated_string())


def main():
    # Get AI bot name, mode, and frequency from the user
    _, encoded_username, username_header = get_username("Enter AI bot name: ")
    response_mode = input("Enter response mode (lines/seconds): ")
    response_frequency = int(input(f"Enter response frequency (number of {response_mode}): "))
    # Create client socket and send first message with username
    client_socket = create_client_socket(username_header + encoded_username)

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, response_mode, response_frequency))
    receive_thread.start()

    if response_mode == "seconds":
        send_thread = threading.Thread(target=send_periodic_messages,args=(client_socket, response_mode, response_frequency),)
        send_thread.start()


if __name__ == "__main__":
    main()
