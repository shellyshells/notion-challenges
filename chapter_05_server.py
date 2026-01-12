#!/usr/bin/env python3
"""
Chapter 5: Socket Programming - Server Script
This script creates a TCP server that can handle multiple client connections using threading.
Sockets are the foundation of network programming - they allow programs to communicate over networks.
"""

import socket
import threading
import sys

# Global variables for server configuration
HOST = '0.0.0.0'  # Listen on all available network interfaces
PORT = 9999       # Port number to listen on (choose > 1024 to avoid needing root)
BUFFER_SIZE = 1024  # Maximum bytes to receive at once

# Thread-safe counter for active connections
active_connections = 0
connection_lock = threading.Lock()


def handle_client(client_socket, client_address):
    """
    Handles communication with a single client in a separate thread.
    
    Args:
        client_socket: The socket object for this client connection
        client_address: Tuple of (ip_address, port) for the client
    
    How threading helps:
    - Each client gets its own thread
    - Server can handle multiple clients simultaneously
    - One slow client won't block others
    """
    
    global active_connections
    
    # Increment active connection counter (thread-safe)
    with connection_lock:
        active_connections += 1
        current_connections = active_connections
    
    print(f"\n[+] New connection from {client_address[0]}:{client_address[1]}")
    print(f"[+] Active connections: {current_connections}")
    
    try:
        # Send a welcome message to the client
        welcome_msg = f"Welcome, brave adventurer! You are connected to the Mage's Tower.\n"
        welcome_msg += f"Your connection ID: {threading.current_thread().name}\n"
        client_socket.send(welcome_msg.encode('utf-8'))
        
        # Main communication loop
        while True:
            # Receive data from the client
            # recv() blocks until data is received or connection is closed
            data = client_socket.recv(BUFFER_SIZE)
            
            if not data:
                # Empty data means client disconnected
                print(f"[-] Client {client_address[0]}:{client_address[1]} disconnected")
                break
            
            # Decode the received bytes to a string
            message = data.decode('utf-8').strip()
            print(f"[>] Received from {client_address[0]}: {message}")
            
            # Process the message and create a response
            response = process_message(message, client_address)
            
            # Send response back to client
            client_socket.send(response.encode('utf-8'))
            print(f"[<] Sent to {client_address[0]}: {response.strip()}")
            
    except ConnectionResetError:
        # Client forcefully closed the connection
        print(f"[-] Connection reset by {client_address[0]}:{client_address[1]}")
    except Exception as e:
        print(f"[-] Error handling client {client_address[0]}: {e}")
    finally:
        # Clean up: close the socket and decrement counter
        client_socket.close()
        
        with connection_lock:
            active_connections -= 1
        
        print(f"[-] Closed connection to {client_address[0]}:{client_address[1]}")
        print(f"[+] Active connections: {active_connections}")


def process_message(message, client_address):
    """
    Processes incoming messages and generates appropriate responses.
    
    Args:
        message (str): The message received from the client
        client_address: The client's address tuple
    
    Returns:
        str: Response message to send back
    
    This function demonstrates:
    - Message parsing
    - Command handling
    - Response generation
    """
    
    # Convert message to lowercase for case-insensitive comparison
    message_lower = message.lower()
    
    # Command handling - you can expand this with more commands
    if message_lower == "help":
        response = """
Available commands:
- HELP: Show this help message
- STATUS: Show server status
- SPELL: Cast a random spell
- QUIT: Disconnect from server
"""
    
    elif message_lower == "status":
        response = f"Server Status: Running | Active connections: {active_connections}\n"
    
    elif message_lower == "spell":
        import random
        spells = [
            "Lightning Bolt strikes! ⚡",
            "Fireball erupts! 🔥",
            "Ice Shard freezes the enemy! ❄️",
            "Dark Magic overwhelms! 🌑",
            "Healing Light restores health! ✨"
        ]
        response = f"The Mage casts: {random.choice(spells)}\n"
    
    elif message_lower == "quit":
        response = "Farewell, adventurer! May your journey continue...\n"
    
    else:
        # Echo back the message with a prefix
        response = f"[Echo from Mage's Tower] {message}\n"
    
    return response


def start_server():
    """
    Initializes and starts the TCP server.
    
    This function:
    1. Creates a socket
    2. Binds it to a host and port
    3. Listens for connections
    4. Accepts connections and spawns threads
    
    Socket workflow:
    - socket() -> create socket
    - bind() -> attach to address/port
    - listen() -> enable connection queue
    - accept() -> wait for and accept connections
    """
    
    print("="*60)
    print("Starting Mage's Tower Server")
    print("="*60)
    
    # Create a TCP socket
    # AF_INET = IPv4 addressing
    # SOCK_STREAM = TCP (reliable, connection-oriented)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Set socket options
    # SO_REUSEADDR allows reusing the address immediately after closing
    # This prevents "Address already in use" errors when restarting quickly
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Bind the socket to the host and port
        # This reserves the port for our server
        server_socket.bind((HOST, PORT))
        print(f"[+] Server bound to {HOST}:{PORT}")
        
        # Start listening for connections
        # The argument (5) is the backlog - maximum queued connections
        server_socket.listen(5)
        print(f"[+] Server listening... (Max queued connections: 5)")
        print(f"[+] Waiting for brave adventurers to connect...\n")
        
        # Main server loop - accept connections forever
        while True:
            # accept() blocks until a client connects
            # Returns a new socket for this client and the client's address
            client_socket, client_address = server_socket.accept()
            
            # Create a new thread to handle this client
            # target= is the function to run in the thread
            # args= are the arguments to pass to the function
            # daemon=True means thread will close when main program exits
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address),
                daemon=True
            )
            
            # Start the thread
            client_thread.start()
    
    except KeyboardInterrupt:
        # User pressed Ctrl+C
        print("\n\n[!] Server shutdown requested by user")
    except Exception as e:
        print(f"[-] Server error: {e}")
    finally:
        # Clean up: close the server socket
        print("\n[*] Closing server socket...")
        server_socket.close()
        print("[*] Server stopped")


def main():
    """
    Main entry point for the server script.
    """
    
    print("\n" + "🏰"*30)
    print("Chapter 5: The Mage's Tower - Socket Server")
    print("🏰"*30 + "\n")
    
    print("[*] This server will handle multiple client connections")
    print("[*] Each client gets its own thread for concurrent communication")
    print(f"[*] Server will listen on {HOST}:{PORT}\n")
    
    # Start the server
    start_server()


if __name__ == "__main__":
    main()
