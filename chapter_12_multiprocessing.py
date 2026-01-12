#!/usr/bin/env python3
"""
Chapter 12: Multiprocessing
This script demonstrates Python's multiprocessing module for parallel execution.
Multiprocessing allows running code on multiple CPU cores simultaneously.
"""

import multiprocessing
import random
import time
import os

def generate_random_number(process_id):
    """
    Worker function that generates a random number.
    
    Args:
        process_id (int): Identifier for this process
    
    Each process runs independently with its own memory space.
    This is true parallelism (unlike threading with GIL).
    """
    
    # Get process information
    pid = os.getpid()
    ppid = os.getppid()
    
    print(f"[Process {process_id}] Started")
    print(f"    PID: {pid}")
    print(f"    Parent PID: {ppid}")
    
    # Simulate some work
    sleep_time = random.uniform(1, 3)
    print(f"[Process {process_id}] Working for {sleep_time:.2f} seconds...")
    time.sleep(sleep_time)
    
    # Generate random number
    random_num = random.randint(1, 1000)
    
    print(f"[Process {process_id}] Generated number: {random_num}")
    print(f"[Process {process_id}] Completed\n")
    
    return random_num


def main():
    """
    Main function demonstrating multiprocessing.
    """
    
    print("\n" + "🗺️"*30)
    print("Chapter 12: The Cave Map - Multiprocessing Quest")
    print("🗺️"*30 + "\n")
    
    print("[*] You've discovered a map in the cave...")
    print("[*] Time to master parallel processing!\n")
    
    # Show current process info
    print("="*60)
    print("Main Process Information")
    print("="*60)
    print(f"Main PID: {os.getpid()}")
    print(f"CPU Count: {multiprocessing.cpu_count()}")
    print("="*60 + "\n")
    
    # Create process list
    num_processes = 5
    print(f"[*] Creating {num_processes} processes...\n")
    
    processes = []
    
    # Create and start processes
    for i in range(num_processes):
        # Create a Process object
        # target= is the function to run
        # args= tuple of arguments for the function
        process = multiprocessing.Process(
            target=generate_random_number,
            args=(i+1,),
            name=f"Worker-{i+1}"
        )
        
        # Add to list
        processes.append(process)
        
        # Start the process
        process.start()
        print(f"[+] Started process {i+1} (PID will be assigned by OS)")
    
    print("\n" + "="*60)
    print("All Processes Started")
    print("="*60)
    print("[*] Open another terminal and run: ps aux | grep python")
    print("[*] You should see multiple python processes running")
    print("[*] Press Enter when ready to continue...")
    input()
    
    # Wait for all processes to complete
    print("\n[*] Waiting for all processes to complete...\n")
    
    for i, process in enumerate(processes, 1):
        process.join()  # Wait for process to finish
        print(f"[+] Process {i} joined (completed)")
    
    # Check process status
    print("\n" + "="*60)
    print("Process Status")
    print("="*60)
    
    for i, process in enumerate(processes, 1):
        print(f"Process {i}:")
        print(f"    Name: {process.name}")
        print(f"    PID: {process.pid}")
        print(f"    Alive: {process.is_alive()}")
        print(f"    Exit Code: {process.exitcode}")
    
    # Cleanup
    print("\n[*] Closing all processes...")
    for process in processes:
        process.close()
    
    print("\n" + "="*60)
    print("Quest Complete!")
    print("="*60)
    print("[✓] Created multiple processes")
    print("[✓] Observed processes with 'ps' command")
    print("[✓] Identified processes by PID")
    print("[✓] Properly closed all processes")
    print("[*] You've mastered multiprocessing!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
