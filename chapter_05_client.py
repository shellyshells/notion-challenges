#!/usr/bin/env python3
"""
Chapter 5: Socket Programming - Client Script
This script creates a TCP client that connects to the server and sends messages.
The client can send a custom message provided as a command-line argument.
"""

import socket
import sys
import argparse

# Default server configuration
DEFAULT_HOST = '127.0.0.1'  # localhost - change this to server's IP if remote
DEFAULT_PORT = 9999
BUFFER_SIZE = 1024


def connect_to_server(host, port):
    """
    Establishes a connection to the server.
    
    Args:
        host (str): Server IP address or hostname
        port (int): Server port number
    
    Returns:
        socket: Connected socket object, or None if connection fails
    
    Client socket workflow:
    - socket() -> create socket
    - connect() -> connect to server
    - send()/recv() -> exchange data
    - close() -> close connection
    """
    
    print("="*60)
    print("Connecting to Mage's Tower")
    print("="*60)
    
    try:
        # Create a TCP socket
        # AF_INET = IPv4, SOCK_STREAM = TCP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        print(f"[*] Attempting to connect to {host}:{port}...")
        
        # Connect to the server
        # This blocks until connection is established or timeout occurs
        client_socket.connect((host, port))
        
        print(f"[+] Successfully connected to {host}:{port}")
        
        return client_socket
        
    except ConnectionRefusedError:
        # Server is not running or not accepting connections
        print(f"[-] Connection refused - Is the server running on {host}:{port}?")
        return None
    except socket.timeout:
        print(f"[-] Connection timeout - Server not responding")
        return None
    except Exception as e:
        print(f"[-] Connection error: {e}")
        return None


def send_message(client_socket, message):
    """
    Sends a message to the server and receives the response.
    
    Args:
        client_socket: Connected socket object
        message (str): Message to send
    
    Returns:
        str: Response from server, or None if error
    
    How TCP communication works:
    - Data is sent as bytes (must encode strings)
    - Data is received as bytes (must decode to strings)
    - TCP guarantees delivery and ordering
    """
    
    try:
        # Convert string to bytes and send to server
        # encode('utf-8') converts string to bytes using UTF-8 encoding
        print(f"\n[>] Sending message: {message}")
        client_socket.send(message.encode('utf-8'))
        
        # Receive response from server
        # recv() blocks until data arrives or connection closes
        # BUFFER_SIZE is the maximum bytes to receive at once
        response_data = client_socket.recv(BUFFER_SIZE)
        
        if not response_data:
            print("[-] Server closed the connection")
            return None
        
        # Convert bytes back to string
        response = response_data.decode('utf-8')
        print(f"[<] Received response:")
        print("-"*60)
        print(response)
        print("-"*60)
        
        return response
        
    except BrokenPipeError:
        print("[-] Connection broken - server may have closed")
        return None
    except Exception as e:
        print(f"[-] Error during communication: {e}")
        return None


def interactive_mode(client_socket):
    """
    Runs an interactive session where user can send multiple messages.
    
    Args:
        client_socket: Connected socket object
    
    This mode allows:
    - Sending multiple messages without reconnecting
    - Interactive conversation with the server
    - Graceful exit with 'quit' command
    """
    
    print("\n" + "="*60)
    print("Interactive Mode")
    print("="*60)
    print("[*] Type your messages and press Enter")
    print("[*] Type 'quit' to disconnect\n")
    
    try:
        while True:
            # Get user input
            user_input = input("[You] > ").strip()
            
            if not user_input:
                # Skip empty messages
                continue
            
            # Send message and get response
            response = send_message(client_socket, user_input)
            
            if response is None:
                # Connection lost
                break
            
            # Check if user wants to quit
            if user_input.lower() == 'quit':
                print("[*] Disconnecting from server...")
                break
                
    except KeyboardInterrupt:
        # User pressed Ctrl+C
        print("\n\n[!] Interrupted by user")
    except EOFError:
        # End of input (Ctrl+D on Unix, Ctrl+Z on Windows)
        print("\n[*] End of input")


def main():
    """
    Main function - parses arguments and runs the client.
    
    This demonstrates:
    - Command-line argument parsing
    - Two modes: single message or interactive
    - Proper connection handling and cleanup
    """
    
    print("\n" + "⚔️"*30)
    print("Chapter 5: Socket Client - Journey to the Mage's Tower")
    print("⚔️"*30 + "\n")
    
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="TCP Client for connecting to the Mage's Tower server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Send a single message
  python3 chapter_05_client.py -m "Hello from the village"
  
  # Interactive mode
  python3 chapter_05_client.py -i
  
  # Connect to remote server
  python3 chapter_05_client.py -H 192.168.1.100 -p 9999 -m "Greetings"
        """
    )
    
    # Add arguments
    parser.add_argument(
        '-H', '--host',
        default=DEFAULT_HOST,
        help=f'Server hostname or IP address (default: {DEFAULT_HOST})'
    )
    
    parser.add_argument(
        '-p', '--port',
        type=int,
        default=DEFAULT_PORT,
        help=f'Server port number (default: {DEFAULT_PORT})'
    )
    
    parser.add_argument(
        '-m', '--message',
        help='Message to send to the server'
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode (send multiple messages)'
    )
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Validate arguments
    if not args.message and not args.interactive:
        print("[-] Error: You must specify either -m/--message or -i/--interactive")
        print("[-] Use -h for help")
        sys.exit(1)
    
    # Connect to server
    client_socket = connect_to_server(args.host, args.port)
    
    if client_socket is None:
        print("[-] Failed to connect to server")
        sys.exit(1)
    
    try:
        # Receive welcome message from server
        welcome_data = client_socket.recv(BUFFER_SIZE)
        if welcome_data:
            welcome_msg = welcome_data.decode('utf-8')
            print("\n[Server Welcome Message]")
            print("-"*60)
            print(welcome_msg)
            print("-"*60)
        
        # Run in appropriate mode
        if args.interactive:
            # Interactive mode - multiple messages
            interactive_mode(client_socket)
        else:
            # Single message mode
            send_message(client_socket, args.message)
        
    finally:
        # Always close the socket when done
        print("\n[*] Closing connection...")
        client_socket.close()
        print("[+] Connection closed")
        print("\n[✓] Quest completed! You've mastered socket communication!")


if __name__ == "__main__":
    main()
