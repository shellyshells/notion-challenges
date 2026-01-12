#!/usr/bin/env python3
"""
Chapter 15: Preparation (Second Phase)
This is another preparation chapter - verifying environment is ready for offensive chapters.
"""

import sys
import subprocess

def check_python_version():
    """Checks Python version."""
    print("="*60)
    print("Python Version Check")
    print("="*60)
    
    version = sys.version_info
    print(f"[+] Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 6:
        print("[✓] Python version is sufficient")
        return True
    else:
        print("[!] Python 3.6+ recommended")
        return False


def check_virtualization():
    """Checks for virtualization tools."""
    print("\n" + "="*60)
    print("Virtualization Check")
    print("="*60)
    
    commands = {
        'VirtualBox': 'vboxmanage --version',
        'VMware': 'vmware -v',
        'QEMU': 'qemu-system-x86_64 --version',
        'Docker': 'docker --version'
    }
    
    found = False
    for tool, cmd in commands.items():
        try:
            result = subprocess.run(cmd.split(), capture_output=True, text=True)
            if result.returncode == 0:
                print(f"[✓] {tool} is installed")
                found = True
        except FileNotFoundError:
            print(f"[ ] {tool} not found")
    
    if not found:
        print("\n[!] No virtualization tool detected")
        print("[!] Install VirtualBox, VMware, QEMU, or Docker")
    
    return found


def main():
    """Main preparation check."""
    print("\n" + "📜"*30)
    print("Chapter 15: Second Preparation Phase")
    print("📜"*30 + "\n")
    
    print("[*] You've defeated the Black Mage...")
    print("[*] Preparing for the final challenges!\n")
    
    python_ok = check_python_version()
    vm_ok = check_virtualization()
    
    print("\n" + "="*60)
    print("Preparation Status")
    print("="*60)
    
    if python_ok and vm_ok:
        print("[✓] All checks passed!")
        print("[✓] Ready for offensive security chapters")
    else:
        print("[!] Some checks failed")
        print("[!] Review requirements above")
    
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
