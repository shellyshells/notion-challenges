#!/usr/bin/env python3
"""
Chapter 26: MAC Address Changer
This script changes the MAC address of a network interface.
MAC addresses are hardware identifiers for network interfaces.
"""

import subprocess
import re
import argparse
import random

def get_current_mac(interface):
    """
    Gets the current MAC address of an interface.
    
    Args:
        interface (str): Network interface name (e.g., eth0, wlan0)
    
    Returns:
        str: Current MAC address or None
    
    MAC Address format: XX:XX:XX:XX:XX:XX (6 pairs of hex digits)
    """
    
    try:
        # Run ifconfig to get interface info
        result = subprocess.run(
            ['ifconfig', interface],
            capture_output=True,
            text=True
        )
        
        # Search for MAC address pattern
        mac_search = re.search(r'([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}', result.stdout)
        
        if mac_search:
            return mac_search.group(0)
        else:
            return None
            
    except FileNotFoundError:
        print("[-] ifconfig not found. Install with: sudo apt install net-tools")
        return None
    except Exception as e:
        print(f"[-] Error: {e}")
        return None


def change_mac(interface, new_mac):
    """
    Changes the MAC address of an interface.
    
    Args:
        interface (str): Network interface name
        new_mac (str): New MAC address
    
    Returns:
        bool: True if successful
    
    Steps:
    1. Bring interface down
    2. Change MAC address
    3. Bring interface up
    """
    
    print(f"[*] Changing MAC address of {interface} to {new_mac}")
    
    try:
        # Bring interface down
        print("[*] Bringing interface down...")
        subprocess.run(['ifconfig', interface, 'down'], check=True)
        
        # Change MAC address
        print("[*] Changing MAC address...")
        subprocess.run(['ifconfig', interface, 'hw', 'ether', new_mac], check=True)
        
        # Bring interface up
        print("[*] Bringing interface up...")
        subprocess.run(['ifconfig', interface, 'up'], check=True)
        
        print("[+] MAC address changed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"[-] Command failed: {e}")
        return False
    except Exception as e:
        print(f"[-] Error: {e}")
        return False


def validate_mac(mac):
    """
    Validates MAC address format.
    
    Args:
        mac (str): MAC address to validate
    
    Returns:
        bool: True if valid format
    
    Valid format: XX:XX:XX:XX:XX:XX
    Where X is a hexadecimal digit (0-9, A-F)
    """
    
    # MAC address regex pattern
    pattern = r'^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$'
    
    if re.match(pattern, mac):
        return True
    else:
        return False


def generate_random_mac():
    """
    Generates a random MAC address.
    
    Returns:
        str: Random MAC address
    
    Note: First byte should be even for unicast addresses
    """
    
    # Generate 6 random bytes
    mac_bytes = [random.randint(0x00, 0xff) for _ in range(6)]
    
    # Make sure first byte is even (unicast address)
    mac_bytes[0] = mac_bytes[0] & 0xfe
    
    # Format as MAC address
    mac = ':'.join([f'{byte:02x}' for byte in mac_bytes])
    
    return mac


def validate_interface(interface):
    """
    Validates that the interface name is in correct format.
    
    Args:
        interface (str): Interface name to validate
    
    Returns:
        bool: True if valid
    
    Valid formats: eth0, wlan0, ens33, enp0s3, etc.
    """
    
    # Common interface name patterns
    pattern = r'^(eth|wlan|ens|enp|wlp|lo)[0-9]+[a-z0-9]*$'
    
    if re.match(pattern, interface):
        return True
    else:
        return False


def list_interfaces():
    """
    Lists available network interfaces.
    """
    
    print("\n" + "="*60)
    print("Available Network Interfaces")
    print("="*60)
    
    try:
        result = subprocess.run(['ifconfig', '-a'], capture_output=True, text=True)
        
        # Extract interface names
        interfaces = re.findall(r'^(\w+):', result.stdout, re.MULTILINE)
        
        for iface in interfaces:
            current_mac = get_current_mac(iface)
            print(f"  {iface}: {current_mac if current_mac else 'No MAC'}")
            
    except Exception as e:
        print(f"[-] Error listing interfaces: {e}")


def main():
    """
    Main function for MAC address changer.
    """
    
    print("\n" + "🏚️"*30)
    print("Chapter 26: The Mysterious Inn - MAC Address Quest")
    print("🏚️"*30 + "\n")
    
    # Create argument parser
    parser = argparse.ArgumentParser(
        description='Change MAC address of a network interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  sudo python3 chapter_26_mac_changer.py -i eth0 -m 00:11:22:33:44:55
  sudo python3 chapter_26_mac_changer.py -i wlan0 -r
  python3 chapter_26_mac_changer.py -l
        '''
    )
    
    parser.add_argument(
        '-i', '--interface',
        type=str,
        help='Network interface to modify (e.g., eth0, wlan0)'
    )
    
    parser.add_argument(
        '-m', '--mac',
        type=str,
        help='New MAC address (format: XX:XX:XX:XX:XX:XX)'
    )
    
    parser.add_argument(
        '-r', '--random',
        action='store_true',
        help='Generate and use a random MAC address'
    )
    
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List available network interfaces'
    )
    
    args = parser.parse_args()
    
    # List interfaces mode
    if args.list:
        list_interfaces()
        return
    
    # Validate arguments
    if not args.interface:
        parser.error("Interface is required (-i/--interface)")
    
    if not args.mac and not args.random:
        parser.error("Either MAC address (-m) or random (-r) is required")
    
    # Validate interface format
    if not validate_interface(args.interface):
        print(f"[-] Invalid interface format: {args.interface}")
        print("[*] Valid formats: eth0, wlan0, ens33, enp0s3, etc.")
        return
    
    # Check root privileges
    import os
    if os.geteuid() != 0:
        print("[-] This script requires root privileges")
        print("[*] Run with: sudo python3 chapter_26_mac_changer.py ...")
        return
    
    # Get current MAC
    print("="*60)
    print("Current Configuration")
    print("="*60)
    current_mac = get_current_mac(args.interface)
    
    if current_mac:
        print(f"[*] Interface: {args.interface}")
        print(f"[*] Current MAC: {current_mac}")
    else:
        print(f"[-] Could not get current MAC for {args.interface}")
        print(f"[-] Interface may not exist")
        return
    
    # Determine new MAC address
    if args.random:
        new_mac = generate_random_mac()
        print(f"[*] Generated random MAC: {new_mac}")
    else:
        new_mac = args.mac
        
        # Validate MAC format
        if not validate_mac(new_mac):
            print(f"[-] Invalid MAC address format: {new_mac}")
            print("[*] Format should be: XX:XX:XX:XX:XX:XX")
            return
    
    # Change MAC address
    print("\n" + "="*60)
    print("Changing MAC Address")
    print("="*60)
    
    if change_mac(args.interface, new_mac):
        # Verify change
        new_current_mac = get_current_mac(args.interface)
        
        print("\n" + "="*60)
        print("Verification")
        print("="*60)
        print(f"[*] Old MAC: {current_mac}")
        print(f"[*] New MAC: {new_current_mac}")
        
        if new_current_mac == new_mac:
            print("[✓] MAC address successfully changed!")
        else:
            print("[!] MAC address may not have changed correctly")
    else:
        print("[-] Failed to change MAC address")
    
    print("\n" + "="*60)
    print("Quest Complete!")
    print("="*60)
    print("[✓] Changed MAC address manually")
    print("[✓] Created Python script for MAC changing")
    print("[✓] Validated interface format")
    print("[✓] Verified interface format validation")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
