#!/usr/bin/env python3
"""
Chapter 3: Temporary Files Management
This script demonstrates secure handling of temporary files using the tempfile module.
Temporary files are useful for storing data during program execution without cluttering the filesystem.
"""

import tempfile
import os

def create_and_use_temp_file():
    """
    Demonstrates creating a temporary file, writing to it, reading from it, and deletion.
    
    Why use tempfile?
    - Automatically handles file creation in the appropriate temp directory (/tmp on Linux)
    - Provides unique filenames to avoid conflicts
    - Can auto-delete files when closed (secure cleanup)
    - Cross-platform compatible (works on Windows, Linux, macOS)
    """
    
    print("="*60)
    print("Creating Temporary File with tempfile.NamedTemporaryFile()")
    print("="*60)
    
    # Create a named temporary file
    # mode='w+t' means: write and read, text mode
    # delete=False means: keep the file after closing (we'll manually delete it)
    # suffix and prefix help identify our temp files
    with tempfile.NamedTemporaryFile(mode='w+t', delete=False, 
                                      suffix='.txt', 
                                      prefix='arrakis_') as temp_file:
        
        # Get the full path to the temporary file
        temp_filepath = temp_file.name
        print(f"[+] Temporary file created at: {temp_filepath}")
        
        # Write some content to the temporary file
        content = """This is temporary data from the Arrakis quest.
The dark forest of Nephyr holds many secrets.
The Black Mage's tower awaits the brave adventurer.
This file will be deleted after reading."""
        
        print(f"\n[+] Writing content to temporary file...")
        temp_file.write(content)
        print(f"[+] Successfully wrote {len(content)} characters")
        
        # Important: flush() ensures all data is written to disk
        # Without this, some data might still be in the buffer
        temp_file.flush()
        print("[+] Data flushed to disk")
    
    # The file is now closed (exited the 'with' block)
    # But it still exists because we set delete=False
    
    print(f"\n[+] File closed, but still exists on disk")
    print(f"[+] File exists: {os.path.exists(temp_filepath)}")
    
    # Now read the content back from the file
    print("\n" + "="*60)
    print("Reading Content from Temporary File")
    print("="*60)
    
    # Open the file in read mode
    with open(temp_filepath, 'r') as temp_file:
        read_content = temp_file.read()
        
        print("[+] Content read from file:")
        print("-"*60)
        print(read_content)
        print("-"*60)
    
    # Now delete the temporary file manually
    print("\n" + "="*60)
    print("Cleaning Up Temporary File")
    print("="*60)
    
    try:
        # os.remove() deletes the file from the filesystem
        os.remove(temp_filepath)
        print(f"[+] Successfully deleted temporary file: {temp_filepath}")
        print(f"[+] File exists: {os.path.exists(temp_filepath)}")
    except OSError as e:
        print(f"[-] Error deleting file: {e}")


def demonstrate_auto_delete():
    """
    Demonstrates automatic deletion when delete=True (default behavior).
    This is more secure as it guarantees cleanup even if the program crashes.
    """
    
    print("\n" + "="*60)
    print("Demonstrating Auto-Delete Feature")
    print("="*60)
    
    # With delete=True, the file is automatically deleted when closed
    with tempfile.NamedTemporaryFile(mode='w+t', delete=True, 
                                      suffix='.txt', 
                                      prefix='auto_delete_') as temp_file:
        
        filepath = temp_file.name
        print(f"[+] Created auto-delete temp file: {filepath}")
        
        # Write some data
        temp_file.write("This will be automatically deleted!\n")
        temp_file.flush()
        
        # While inside the 'with' block, file exists
        print(f"[+] File exists while open: {os.path.exists(filepath)}")
    
    # After exiting the 'with' block, file is automatically deleted
    print(f"[+] File exists after closing: {os.path.exists(filepath)}")
    print("[+] File was automatically deleted!")


def demonstrate_temp_directory():
    """
    Demonstrates creating a temporary directory for multiple files.
    Useful when you need to work with several temporary files at once.
    """
    
    print("\n" + "="*60)
    print("Creating Temporary Directory")
    print("="*60)
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory(prefix='arrakis_quest_') as temp_dir:
        
        print(f"[+] Temporary directory created: {temp_dir}")
        
        # Create multiple files in the temp directory
        file1_path = os.path.join(temp_dir, "quest_notes.txt")
        file2_path = os.path.join(temp_dir, "mage_spells.txt")
        
        # Write to first file
        with open(file1_path, 'w') as f1:
            f1.write("Quest: Find the Black Mage\n")
            f1.write("Location: Dark Forest of Nephyr\n")
        
        # Write to second file
        with open(file2_path, 'w') as f2:
            f2.write("Spell 1: Lightning Bolt\n")
            f2.write("Spell 2: Dark Magic\n")
        
        # List files in the temporary directory
        print(f"\n[+] Files in temporary directory:")
        for filename in os.listdir(temp_dir):
            filepath = os.path.join(temp_dir, filename)
            print(f"    - {filename} ({os.path.getsize(filepath)} bytes)")
        
        print(f"\n[+] Directory exists: {os.path.exists(temp_dir)}")
    
    # After exiting the 'with' block, entire directory is deleted
    print(f"[+] Directory exists after cleanup: {os.path.exists(temp_dir)}")
    print("[+] Temporary directory and all contents automatically deleted!")


def demonstrate_mkstemp():
    """
    Demonstrates tempfile.mkstemp() - a lower-level function that returns a file descriptor.
    This gives more control but requires manual cleanup.
    """
    
    print("\n" + "="*60)
    print("Using tempfile.mkstemp() for Low-Level Control")
    print("="*60)
    
    # mkstemp() returns a tuple: (file_descriptor, filepath)
    # file_descriptor is an OS-level handle to the file
    fd, filepath = tempfile.mkstemp(suffix='.log', prefix='system_', text=True)
    
    print(f"[+] Created temp file: {filepath}")
    print(f"[+] File descriptor: {fd}")
    
    try:
        # Write to the file using the file descriptor
        # os.write() requires bytes, not strings
        message = b"System log entry: Quest initiated\n"
        os.write(fd, message)
        
        print(f"[+] Wrote {len(message)} bytes to file")
        
        # Important: close the file descriptor
        os.close(fd)
        print("[+] File descriptor closed")
        
        # Read the content back
        with open(filepath, 'r') as f:
            content = f.read()
            print(f"[+] Content: {content.strip()}")
        
    finally:
        # Always clean up - remove the file
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"[+] Cleaned up temp file: {filepath}")


def main():
    """
    Main function to demonstrate all tempfile module features.
    """
    
    print("\n" + "🏰"*30)
    print("Chapter 3: The Dark Forest of Néphyr - Temporary Files Quest")
    print("🏰"*30 + "\n")
    
    # Demonstration 1: Basic temp file with manual deletion
    create_and_use_temp_file()
    
    # Demonstration 2: Auto-delete temp file
    demonstrate_auto_delete()
    
    # Demonstration 3: Temporary directory
    demonstrate_temp_directory()
    
    # Demonstration 4: Low-level file descriptor approach
    demonstrate_mkstemp()
    
    print("\n" + "="*60)
    print("Quest Completed! You've mastered temporary file management!")
    print("="*60)
    
    # Show where temporary files are created on this system
    temp_dir = tempfile.gettempdir()
    print(f"\n[INFO] System temporary directory: {temp_dir}")


if __name__ == "__main__":
    """
    Entry point of the script.
    This ensures code only runs when the script is executed directly.
    """
    main()
