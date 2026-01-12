#!/usr/bin/env python3
"""
Chapter 11: Packet Sniffing with Scapy
This script demonstrates network traffic capture and analysis using Scapy.
Packet sniffing allows you to inspect network communications.
"""

from scapy.all import *
import sys

def packet_callback(packet):
    """
    Callback function called for each captured packet.
    
    Args:
        packet: Scapy packet object
    
    This function is called by sniff() for every packet captured.
    It's where you analyze and display packet information.
    """
    
    print("\n" + "="*60)
    print("Packet Captured")
    print("="*60)
    
    # Show packet summary
    print(f"[*] Summary: {packet.summary()}")
    
    # Check for IP layer
    if packet.haslayer(IP):
        ip_layer = packet[IP]
        print(f"\n[IP Layer]")
        print(f"  Source IP: {ip_layer.src}")
        print(f"  Destination IP: {ip_layer.dst}")
        print(f"  Protocol: {ip_layer.proto}")
        print(f"  TTL: {ip_layer.ttl}")
    
    # Check for TCP layer
    if packet.haslayer(TCP):
        tcp_layer = packet[TCP]
        print(f"\n[TCP Layer]")
        print(f"  Source Port: {tcp_layer.sport}")
        print(f"  Destination Port: {tcp_layer.dport}")
        print(f"  Flags: {tcp_layer.flags}")
        print(f"  Sequence: {tcp_layer.seq}")
    
    # Check for UDP layer
    if packet.haslayer(UDP):
        udp_layer = packet[UDP]
        print(f"\n[UDP Layer]")
        print(f"  Source Port: {udp_layer.sport}")
        print(f"  Destination Port: {udp_layer.dport}")
        print(f"  Length: {udp_layer.len}")
    
    # Check for ICMP layer
    if packet.haslayer(ICMP):
        icmp_layer = packet[ICMP]
        print(f"\n[ICMP Layer]")
        print(f"  Type: {icmp_layer.type}")
        print(f"  Code: {icmp_layer.code}")
    
    # Check for DNS layer
    if packet.haslayer(DNS):
        dns_layer = packet[DNS]
        print(f"\n[DNS Layer]")
        if dns_layer.qr == 0:  # Query
            print(f"  Type: Query")
            if dns_layer.qd:
                print(f"  Query: {dns_layer.qd.qname.decode()}")
        else:  # Response
            print(f"  Type: Response")
    
    # Show raw packet data (first 50 bytes)
    print(f"\n[Raw Data (first 50 bytes)]")
    print(bytes(packet)[:50])
    
    print("="*60)


def start_sniffer(interface=None, packet_count=10, filter_str=None):
    """
    Starts the packet sniffer.
    
    Args:
        interface (str): Network interface to sniff on (None = all)
        packet_count (int): Number of packets to capture (0 = infinite)
        filter_str (str): BPF filter string
    
    BPF (Berkeley Packet Filter) examples:
    - "tcp": Only TCP packets
    - "port 80": HTTP traffic
    - "host 8.8.8.8": Traffic to/from specific IP
    - "icmp": Only ICMP packets
    """
    
    print("="*60)
    print("Starting Packet Sniffer")
    print("="*60)
    
    if interface:
        print(f"[*] Interface: {interface}")
    else:
        print(f"[*] Interface: All interfaces")
    
    print(f"[*] Packet count: {packet_count if packet_count > 0 else 'Unlimited'}")
    
    if filter_str:
        print(f"[*] Filter: {filter_str}")
    
    print("\n[*] Starting capture... (Press Ctrl+C to stop)\n")
    
    try:
        # sniff() captures packets
        # iface= specifies network interface
        # count= number of packets to capture
        # prn= callback function for each packet
        # filter= BPF filter string
        # store= whether to store packets (False saves memory)
        packets = sniff(
            iface=interface,
            count=packet_count,
            prn=packet_callback,
            filter=filter_str,
            store=False
        )
        
        print("\n[+] Packet capture completed")
        
    except KeyboardInterrupt:
        print("\n\n[!] Capture interrupted by user")
    except PermissionError:
        print("\n[-] Permission denied - try running with sudo")
    except Exception as e:
        print(f"\n[-] Error: {e}")


def generate_test_traffic():
    """
    Generates test network traffic for sniffing demonstration.
    
    This creates various types of packets so you have something to capture.
    """
    
    print("\n" + "="*60)
    print("Generating Test Traffic")
    print("="*60)
    
    try:
        print("[*] Sending ICMP ping to 8.8.8.8...")
        send(IP(dst="8.8.8.8")/ICMP(), verbose=0)
        
        print("[*] Sending DNS query...")
        send(IP(dst="8.8.8.8")/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname="example.com")), verbose=0)
        
        print("[*] Sending TCP SYN to port 80...")
        send(IP(dst="8.8.8.8")/TCP(dport=80, flags="S"), verbose=0)
        
        print("[+] Test traffic generated")
        print("[*] You should see these packets in the sniffer output")
        
    except PermissionError:
        print("[-] Need root privileges to send packets")
    except Exception as e:
        print(f"[-] Error generating traffic: {e}")


def display_interface_info():
    """
    Displays available network interfaces.
    
    Helps user choose which interface to sniff on.
    """
    
    print("\n" + "="*60)
    print("Available Network Interfaces")
    print("="*60)
    
    try:
        # Get all network interfaces
        interfaces = get_if_list()
        
        print("\nInterface list:")
        for i, iface in enumerate(interfaces, 1):
            print(f"  [{i}] {iface}")
        
        return interfaces
        
    except Exception as e:
        print(f"[-] Error getting interfaces: {e}")
        return []


def main():
    """
    Main function for the packet sniffer.
    """
    
    print("\n" + "🧝"*30)
    print("Chapter 11: The Elven City - Packet Sniffing Quest")
    print("🧝"*30 + "\n")
    
    print("[*] You've escaped to the elven city...")
    print("[*] Time to learn the art of network packet sniffing!\n")
    
    # Check privileges
    if os.geteuid() != 0:
        print("[!] WARNING: This script requires root privileges")
        print("[!] Run with: sudo python3 chapter_11_scapy_sniffer.py\n")
    
    # Display available interfaces
    interfaces = display_interface_info()
    
    # Configuration
    print("\n" + "="*60)
    print("Sniffer Configuration")
    print("="*60)
    
    # Ask for interface
    print("\n[?] Enter interface number (or press Enter for all interfaces):")
    choice = input("    Interface: ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= len(interfaces):
        interface = interfaces[int(choice) - 1]
    else:
        interface = None
    
    # Ask for packet count
    print("\n[?] Number of packets to capture (0 for unlimited):")
    count_input = input("    Count: ").strip()
    packet_count = int(count_input) if count_input.isdigit() else 10
    
    # Ask for filter
    print("\n[?] BPF filter (press Enter for none):")
    print("    Examples: tcp, port 80, icmp, host 8.8.8.8")
    filter_str = input("    Filter: ").strip()
    filter_str = filter_str if filter_str else None
    
    # Ask if user wants to generate test traffic
    print("\n[?] Generate test traffic? (yes/no):")
    gen_traffic = input("    Generate: ").strip().lower()
    
    if gen_traffic in ['yes', 'y']:
        print("\n[*] Generating traffic in 3 seconds...")
        import time
        time.sleep(3)
        generate_test_traffic()
        print("\n[*] Starting sniffer in 2 seconds...")
        time.sleep(2)
    
    # Start sniffing
    start_sniffer(interface, packet_count, filter_str)
    
    # Summary
    print("\n" + "="*60)
    print("Quest Complete!")
    print("="*60)
    print("[✓] Successfully captured and analyzed network packets")
    print("[*] The elves have taught you the art of network observation!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
