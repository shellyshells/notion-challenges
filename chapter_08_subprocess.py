#!/usr/bin/env python3
"""
Chapter 8: Process Management with MySQL
This script demonstrates using the subprocess module to interact with MySQL database.
It shows how to execute external commands and processes from Python.
"""

import subprocess
import sys
import json

# MySQL connection configuration
DB_HOST = "localhost"
DB_USER = "your_username"  # Change this
DB_PASSWORD = "your_password"  # Change this
DB_NAME = "arrakis_quest"
DB_TABLE = "goblin_encounters"


def run_command(command, shell=False, capture_output=True):
    """
    Executes a system command using subprocess.
    
    Args:
        command (list or str): Command to execute
        shell (bool): Whether to use shell interpretation
        capture_output (bool): Whether to capture stdout/stderr
    
    Returns:
        subprocess.CompletedProcess: Result of the command
    
    Why use subprocess?
    - Execute external programs from Python
    - Capture output and error streams
    - Check exit codes
    - More secure than os.system()
    
    subprocess.run() vs other methods:
    - subprocess.run(): Simple, blocking, returns CompletedProcess
    - subprocess.Popen(): More control, non-blocking
    - subprocess.call(): Older, just returns exit code
    """
    
    try:
        # Run the command
        # capture_output=True captures stdout and stderr
        # text=True decodes output as text (not bytes)
        # check=False means don't raise exception on non-zero exit
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=capture_output,
            text=True,
            check=False
        )
        
        return result
    
    except FileNotFoundError:
        print(f"[-] Command not found: {command[0] if isinstance(command, list) else command}")
        return None
    except Exception as e:
        print(f"[-] Error running command: {e}")
        return None


def check_mysql_installed():
    """
    Checks if MySQL client is installed on the system.
    
    Returns:
        bool: True if MySQL is available, False otherwise
    """
    
    print("="*60)
    print("Checking MySQL Installation")
    print("="*60)
    
    # Try to run mysql --version
    result = run_command(["mysql", "--version"])
    
    if result and result.returncode == 0:
        print(f"[+] MySQL is installed: {result.stdout.strip()}")
        return True
    else:
        print("[-] MySQL client not found")
        print("[-] Install with: sudo apt install mysql-client")
        return False


def create_database():
    """
    Creates the database if it doesn't exist.
    
    Uses MySQL command-line client through subprocess.
    
    SQL Command breakdown:
    - CREATE DATABASE IF NOT EXISTS: Only creates if doesn't exist
    - CHARACTER SET utf8mb4: Support for all Unicode characters
    - COLLATE: Sorting and comparison rules
    """
    
    print("\n" + "="*60)
    print("Creating Database")
    print("="*60)
    
    # SQL command to create database
    sql = f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    
    # Build MySQL command
    # -h: host
    # -u: username
    # -p: password (we'll pass it via environment or prompt)
    # -e: execute this SQL command
    mysql_cmd = [
        "mysql",
        "-h", DB_HOST,
        "-u", DB_USER,
        f"-p{DB_PASSWORD}",  # Note: no space between -p and password
        "-e", sql
    ]
    
    print(f"[*] Executing: CREATE DATABASE {DB_NAME}")
    result = run_command(mysql_cmd)
    
    if result and result.returncode == 0:
        print(f"[+] Database '{DB_NAME}' created or already exists")
        return True
    else:
        print(f"[-] Failed to create database")
        if result:
            print(f"[-] Error: {result.stderr}")
        return False


def create_table():
    """
    Creates a table for storing goblin encounter data.
    
    Table structure:
    - id: Auto-incrementing primary key
    - encounter_date: When the encounter happened
    - location: Where it happened
    - goblin_count: Number of goblins
    - status: Outcome of the encounter
    """
    
    print("\n" + "="*60)
    print("Creating Table")
    print("="*60)
    
    # SQL command to create table
    sql = f"""
    CREATE TABLE IF NOT EXISTS {DB_TABLE} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        encounter_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        location VARCHAR(255) NOT NULL,
        goblin_count INT NOT NULL,
        status VARCHAR(50) NOT NULL,
        notes TEXT
    );
    """
    
    # Execute SQL command
    mysql_cmd = [
        "mysql",
        "-h", DB_HOST,
        "-u", DB_USER,
        f"-p{DB_PASSWORD}",
        DB_NAME,  # Use this database
        "-e", sql
    ]
    
    print(f"[*] Creating table: {DB_TABLE}")
    result = run_command(mysql_cmd)
    
    if result and result.returncode == 0:
        print(f"[+] Table '{DB_TABLE}' created successfully")
        return True
    else:
        print(f"[-] Failed to create table")
        if result:
            print(f"[-] Error: {result.stderr}")
        return False


def insert_sample_data():
    """
    Inserts sample encounter data into the table.
    """
    
    print("\n" + "="*60)
    print("Inserting Sample Data")
    print("="*60)
    
    # Sample data - goblin encounters
    encounters = [
        ("Dark Forest Path", 5, "Victory", "Ambushed by goblins, defeated them all"),
        ("Cave Entrance", 3, "Victory", "Guarding the cave entrance"),
        ("Village Outskirts", 8, "Fled", "Too many goblins, strategic retreat"),
        ("Mountain Pass", 2, "Victory", "Scouts, easily defeated"),
    ]
    
    for location, count, status, notes in encounters:
        sql = f"""
        INSERT INTO {DB_TABLE} (location, goblin_count, status, notes)
        VALUES ('{location}', {count}, '{status}', '{notes}');
        """
        
        mysql_cmd = [
            "mysql",
            "-h", DB_HOST,
            "-u", DB_USER,
            f"-p{DB_PASSWORD}",
            DB_NAME,
            "-e", sql
        ]
        
        result = run_command(mysql_cmd)
        
        if result and result.returncode == 0:
            print(f"[+] Inserted: {location} - {count} goblins - {status}")
        else:
            print(f"[-] Failed to insert data for {location}")


def query_database():
    """
    Performs a SELECT query and displays the results.
    
    Demonstrates:
    - Running SQL queries
    - Formatting output
    - Processing query results
    """
    
    print("\n" + "="*60)
    print("Querying Database")
    print("="*60)
    
    # SQL query to retrieve all encounters
    sql = f"SELECT * FROM {DB_TABLE} ORDER BY encounter_date DESC;"
    
    # Execute query
    # Note: we're not using -e here, we're piping SQL into mysql
    mysql_cmd = [
        "mysql",
        "-h", DB_HOST,
        "-u", DB_USER,
        f"-p{DB_PASSWORD}",
        DB_NAME,
        "-e", sql
    ]
    
    print(f"[*] Querying table: {DB_TABLE}")
    result = run_command(mysql_cmd)
    
    if result and result.returncode == 0:
        print("\n[+] Query Results:")
        print("-"*60)
        print(result.stdout)
        print("-"*60)
        
        # Parse and analyze the results
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:  # More than just header
            encounter_count = len(lines) - 1
            print(f"\n[+] Total encounters recorded: {encounter_count}")
            
            # Count victories
            victories = result.stdout.count("Victory")
            print(f"[+] Victories: {victories}")
            print(f"[+] Other outcomes: {encounter_count - victories}")
        
        return True
    else:
        print("[-] Failed to query database")
        if result:
            print(f"[-] Error: {result.stderr}")
        return False


def demonstrate_subprocess_features():
    """
    Demonstrates various subprocess module features.
    
    Shows:
    - Different ways to run commands
    - Capturing output
    - Handling errors
    - Piping between commands
    """
    
    print("\n" + "="*60)
    print("Subprocess Module Features")
    print("="*60)
    
    # Example 1: Simple command
    print("\n[1] Running simple command: echo")
    result = subprocess.run(["echo", "Hello from the goblin quest!"], 
                          capture_output=True, text=True)
    print(f"    Output: {result.stdout.strip()}")
    print(f"    Return code: {result.returncode}")
    
    # Example 2: Command with pipe (using shell)
    print("\n[2] Using shell for pipes:")
    result = subprocess.run("echo 'Goblin\nDragon\nMage' | grep 'Dragon'", 
                          shell=True, capture_output=True, text=True)
    print(f"    Output: {result.stdout.strip()}")
    
    # Example 3: Checking if command succeeded
    print("\n[3] Checking command success:")
    result = subprocess.run(["ls", "/nonexistent"], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"    Command failed with code: {result.returncode}")
        print(f"    Error: {result.stderr.strip()}")
    
    # Example 4: Using Popen for more control
    print("\n[4] Using Popen for real-time output:")
    process = subprocess.Popen(
        ["echo", "Line 1\nLine 2\nLine 3"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=False
    )
    
    # Wait for process to complete and get output
    stdout, stderr = process.communicate()
    print(f"    Process output:\n{stdout}")
    print(f"    Process return code: {process.returncode}")


def main():
    """
    Main function orchestrating the database operations.
    """
    
    print("\n" + "⚔️"*30)
    print("Chapter 8: Goblin Encounter Database - Process Management Quest")
    print("⚔️"*30)
    
    print("\n[*] You venture into the dark forest...")
    print("[*] Goblins lurk in every shadow...")
    print("[*] Time to track your encounters!\n")
    
    # Check if MySQL is installed
    if not check_mysql_installed():
        print("\n[-] MySQL is not available")
        print("[*] Install MySQL first, then run this script")
        print("[*] Or modify the script to use SQLite instead")
        return
    
    # Important security note
    print("\n" + "="*60)
    print("IMPORTANT: Configuration Required")
    print("="*60)
    print("[!] Before running, edit this script and set:")
    print("    - DB_USER: Your MySQL username")
    print("    - DB_PASSWORD: Your MySQL password")
    print("\n[!] WARNING: Storing passwords in scripts is not secure!")
    print("[!] In production, use environment variables or config files")
    print("="*60)
    
    response = input("\n[?] Have you configured the database credentials? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("[*] Please configure the credentials first")
        return
    
    # Create database
    if not create_database():
        print("[-] Failed to create database, exiting...")
        return
    
    # Create table
    if not create_table():
        print("[-] Failed to create table, exiting...")
        return
    
    # Insert sample data
    insert_sample_data()
    
    # Query and display data
    query_database()
    
    # Demonstrate subprocess features
    demonstrate_subprocess_features()
    
    print("\n" + "="*60)
    print("Quest Complete!")
    print("="*60)
    print("[✓] Successfully demonstrated process management with subprocess")
    print("[✓] Created database and table using MySQL CLI")
    print("[✓] Inserted and queried data from Python")
    print("\n[*] The goblins have been documented in the database!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
