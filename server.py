# Import required modules
import socket
import threading


HOST = '10.0.2.15'
PORT = 41002

active_clients = [] # List of all connected users

# Listen for any upcoming messages
def listen_for_messages(client, username):
    
    while 1:
        
        message = client.recv(1024).decode('utf-8')
        
        if message != '':
            
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)
        else:
            pass
            #print(f"The message is empty that sent by {username}")


# Send a message to a single client
def send_message_to_client(client, message):
    
    client.sendall(message.encode())

# Send a message to all the clients that says
# They are connected
def send_messages_to_all(message):
    
    for user in active_clients:
        send_message_to_client(user[1], message)


# Handle the client
def client_handler(client): 
    
    # Server will receive the username
    while 1:
        username = client.recv(1024).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER~"+f"{username} added to the chat"
            send_messages_to_all(prompt_message)
            break
                        
        else: 
            print("Username is empty")
    
    threading.Thread(target=listen_for_messages,args=(client, username, )).start()

# Main function 
def main():
    # create socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # AF_INET => IpV4 address
    # SOCK_Stream => TCP protocol 
    
    # Exception handling
    try:
        server.bind((HOST, PORT))
        print(f"Server is ready to server {HOST} {PORT}")
    except:
        print(f"Couldn't bind to host {HOST} port {PORT}")

    
    # Server settings
    
    # Set the maximum number of connections
    server.listen(4)
    
    # Keep listening to client connections
    while 1:
        
        client, address = server.accept()
        print(f"Connection established successfully to client {address[0]} {address[1]}")
        
        threading.Thread(target=client_handler, args=(client, )).start()

    
    
    

# It will only call the main function when the server.py runned
if __name__ == '__main__':
        main() 