#!/usr/bin/env python3
"""
Chapter 7: Signal Interception
This script demonstrates how to intercept and handle system signals in Python.
Signals are notifications sent to a process by the OS or other processes.
"""

import signal
import sys
import time

# Global variable to track program state
should_exit = False
signal_count = 0


def signal_handler(signum, frame):
    """
    Custom signal handler function that gets called when SIGINT is received.
    
    Args:
        signum (int): The signal number that was received
        frame: The current stack frame (execution context)
    
    How signal handlers work:
    - When a signal arrives, normal execution is interrupted
    - The signal handler function is called immediately
    - After handler completes, execution may resume or terminate
    
    Common signals:
    - SIGINT (2): Interrupt from keyboard (Ctrl+C)
    - SIGTERM (15): Termination request
    - SIGKILL (9): Force kill (cannot be caught!)
    - SIGHUP (1): Hangup detected
    """
    
    global should_exit, signal_count
    
    signal_count += 1
    
    print(f"\n\n{'='*60}")
    print(f"🛡️  Signal Intercepted! 🛡️")
    print(f"{'='*60}")
    print(f"[!] Received signal: {signum} ({signal.Signals(signum).name})")
    print(f"[!] Signal count: {signal_count}")
    
    # Signal information
    if signum == signal.SIGINT:
        print("[*] This is SIGINT - typically from Ctrl+C")
        print("[*] The tavern shakes as you try to leave abruptly...")
    
    # Give user a chance to confirm exit
    if signal_count == 1:
        print("\n[?] Press Ctrl+C again to confirm exit")
        print("[*] Or wait for the program to continue...")
    elif signal_count >= 2:
        print("\n[!] Multiple signals received!")
        print("[!] You've decided to leave the tavern...")
        should_exit = True
    
    print(f"{'='*60}\n")


def setup_signal_handlers():
    """
    Registers signal handlers for various signals.
    
    signal.signal(signum, handler) connects a signal to a handler function:
    - signum: The signal to catch
    - handler: The function to call when signal arrives
    
    Special handlers:
    - signal.SIG_IGN: Ignore the signal
    - signal.SIG_DFL: Use default handler
    - custom_function: Use your own handler
    """
    
    print("\n" + "="*60)
    print("Setting Up Signal Handlers")
    print("="*60)
    
    # Register handler for SIGINT (Ctrl+C)
    # This replaces the default behavior (immediate termination)
    signal.signal(signal.SIGINT, signal_handler)
    print("[+] SIGINT handler registered (Ctrl+C will be intercepted)")
    
    # You can also register handlers for other signals
    # Uncomment these to handle more signals:
    
    # signal.signal(signal.SIGTERM, signal_handler)
    # print("[+] SIGTERM handler registered")
    
    # Note: SIGKILL cannot be caught or ignored!
    # signal.signal(signal.SIGKILL, signal_handler)  # This would cause an error
    
    print("[+] Signal handlers are now active")
    print("="*60 + "\n")


def main_loop():
    """
    Main program loop that continues until interrupted.
    
    This simulates a long-running process that:
    - Performs periodic tasks
    - Can be interrupted gracefully
    - Cleans up properly before exit
    """
    
    global should_exit
    
    print("\n[*] Entering the tavern...")
    print("[*] You can hear the sounds of laughter and music")
    print("[*] The adventure continues...\n")
    
    iteration = 0
    
    # Infinite loop - only exits when should_exit becomes True
    while not should_exit:
        iteration += 1
        
        # Simulate some work being done
        print(f"[{iteration}] Still in the tavern... (Press Ctrl+C to try to leave)")
        
        # Sleep for a short time
        # During sleep, signals can still be received and handled
        try:
            time.sleep(2)  # Wait 2 seconds
        except KeyboardInterrupt:
            # This shouldn't happen since we're catching SIGINT
            # But it's good practice to handle it anyway
            print("\n[!] KeyboardInterrupt caught in sleep")
            should_exit = True
        
        # Check if we should exit
        if should_exit:
            print("\n[!] Exit flag set, breaking out of main loop...")
            break
        
        # Add some variety to the messages
        if iteration % 5 == 0:
            print("    🍺 Alaric offers you another drink...")
        
        if iteration % 3 == 0:
            print("    📜 You listen to tales of the Red Dragon...")


def cleanup():
    """
    Performs cleanup operations before exiting.
    
    This function demonstrates:
    - Graceful shutdown
    - Resource cleanup
    - Final status reporting
    
    In a real application, you might:
    - Close open files
    - Save program state
    - Close network connections
    - Release system resources
    """
    
    print("\n" + "="*60)
    print("Cleanup & Shutdown")
    print("="*60)
    
    print("[*] Performing cleanup operations...")
    
    # Simulate cleanup tasks
    print("    [1/3] Saving quest progress...")
    time.sleep(0.5)
    
    print("    [2/3] Closing tavern tab...")
    time.sleep(0.5)
    
    print("    [3/3] Saying goodbye to Alaric...")
    time.sleep(0.5)
    
    print("\n[+] Cleanup completed successfully")
    print(f"[+] Total signals intercepted: {signal_count}")
    print("\n[✓] You've left the tavern and continue your journey!")
    print("="*60 + "\n")


def main():
    """
    Main entry point of the program.
    
    Flow:
    1. Setup signal handlers
    2. Run main loop
    3. Cleanup on exit
    """
    
    print("\n" + "🍺"*30)
    print("Chapter 7: Alaric's Tavern - Signal Interception Quest")
    print("🍺"*30)
    
    print("\n[*] You wake up in Alaric's tavern with a hangover...")
    print("[*] Despite your condition, the call to adventure is strong!")
    
    # Setup signal interception
    setup_signal_handlers()
    
    print("\n" + "="*60)
    print("Instructions")
    print("="*60)
    print("[*] This program will run in an infinite loop")
    print("[*] Press Ctrl+C once to send SIGINT")
    print("[*] Press Ctrl+C twice to confirm exit")
    print("[*] Watch how the signal is intercepted and handled!")
    print("="*60)
    
    try:
        # Run the main program loop
        main_loop()
    
    except Exception as e:
        # Catch any unexpected errors
        print(f"\n[-] Unexpected error: {e}")
        print("[-] Performing emergency cleanup...")
    
    finally:
        # This always runs, even if there's an exception
        # Perfect for cleanup operations
        cleanup()


if __name__ == "__main__":
    """
    Entry point for the script.
    
    Try running the script and:
    1. Press Ctrl+C once - observe the signal handler
    2. Wait a few seconds and press Ctrl+C again
    3. The program will exit gracefully
    """
    main()
