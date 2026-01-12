#!/usr/bin/env python3
"""
Chapter 2: SSH Connection Script
This script demonstrates SSH connectivity using the Spur library.
It establishes a secure connection to a remote server using credentials.
"""

import spur

def connect_ssh(hostname, username, password, port=22):
    """
    Establishes an SSH connection to a remote server.
    
    Args:
        hostname (str): The IP address or hostname of the SSH server
        username (str): Username for authentication
        password (str): Password for authentication
        port (int): SSH port number (default is 22)
    
    Returns:
        shell: A Spur shell object representing the SSH connection
    
    How it works:
    - Spur is a Python library that wraps paramiko for easier SSH operations
    - It creates a shell object that we can use to run commands remotely
    - The connection uses password authentication (in production, key-based auth is preferred)
    """
    try:
        # Create a shell connection object with the provided credentials
        # This doesn't connect yet, just creates the configuration
        shell = spur.SshShell(
            hostname=hostname,
            username=username,
            password=password,
            port=port,
            missing_host_key=spur.ssh.MissingHostKey.accept  # Auto-accept host keys (use cautiously)
        )
        
        print(f"[+] Attempting to connect to {hostname}:{port}...")
        
        # Test the connection by running a simple command
        # The run() method executes a command on the remote server
        result = shell.run(["echo", "Connection successful!"])
        
        # result.output is the stdout from the command in bytes
        # We decode it to convert from bytes to a readable string
        print(f"[+] {result.output.decode('utf-8').strip()}")
        print(f"[+] Successfully connected to {hostname} as {username}")
        
        return shell
        
    except spur.ssh.ConnectionError as e:
        # This catches connection failures (wrong IP, port closed, etc.)
        print(f"[-] Connection error: {e}")
        return None
    except spur.RunProcessError as e:
        # This catches errors when running commands on the remote system
        print(f"[-] Command execution error: {e}")
        return None
    except Exception as e:
        # Catch any other unexpected errors
        print(f"[-] Unexpected error: {e}")
        return None


def execute_command(shell, command_list):
    """
    Executes a command on the remote SSH server.
    
    Args:
        shell: The Spur SSH shell object
        command_list (list): Command and arguments as a list (e.g., ["ls", "-la"])
    
    Returns:
        str: The command output
    
    Why use a list instead of a string?
    - Using a list prevents command injection vulnerabilities
    - It's clearer and safer than using shell=True in subprocess
    - Each element is treated as a separate argument, not parsed as shell code
    """
    try:
        print(f"\n[+] Executing command: {' '.join(command_list)}")
        
        # Run the command and capture the result
        result = shell.run(command_list)
        
        # Decode the output from bytes to string
        output = result.output.decode('utf-8')
        
        print("[+] Command output:")
        print(output)
        
        return output
        
    except spur.RunProcessError as e:
        # This happens when the command returns a non-zero exit code
        print(f"[-] Command failed with error: {e}")
        # stderr contains error messages from the command
        print(f"[-] Error output: {e.stderr_output.decode('utf-8')}")
        return None
    except Exception as e:
        print(f"[-] Unexpected error: {e}")
        return None


def main():
    """
    Main function to demonstrate SSH connectivity.
    
    In a real scenario, you would:
    1. Never hardcode credentials (use environment variables or config files)
    2. Use SSH keys instead of passwords
    3. Implement proper error handling and logging
    """
    # Configuration - Replace these with your actual server details
    SSH_HOST = "192.168.1.100"  # Replace with your server IP
    SSH_USER = "your_username"   # Replace with your SSH username
    SSH_PASS = "your_password"   # Replace with your SSH password
    SSH_PORT = 22                # Default SSH port
    
    print("="*60)
    print("Chapter 2: SSH Connection with Spur")
    print("="*60)
    
    # Establish the SSH connection
    shell = connect_ssh(SSH_HOST, SSH_USER, SSH_PASS, SSH_PORT)
    
    if shell:
        # If connection successful, execute some commands
        print("\n" + "="*60)
        print("Testing Remote Command Execution")
        print("="*60)
        
        # Example 1: Check current directory
        execute_command(shell, ["pwd"])
        
        # Example 2: List files in home directory
        execute_command(shell, ["ls", "-lh", "~"])
        
        # Example 3: Check system information
        execute_command(shell, ["uname", "-a"])
        
        # Example 4: Check who is logged in
        execute_command(shell, ["whoami"])
        
        print("\n[+] All commands executed successfully!")
        print("[+] Closing SSH connection...")
        
        # The connection will be automatically closed when the shell object is garbage collected
        # But it's good practice to explicitly close it
        # Note: Spur doesn't have an explicit close() method, 
        # the connection is managed automatically
        
    else:
        print("[-] Failed to establish SSH connection")
        print("[-] Please check your credentials and network connectivity")


if __name__ == "__main__":
    """
    This ensures the script only runs when executed directly,
    not when imported as a module in another script.
    """
    main()
