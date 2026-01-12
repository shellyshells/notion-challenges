#!/usr/bin/env python3
"""
Chapter 4: ICMP Packet Dissection
This script demonstrates creating, inspecting, sending ICMP packets using Scapy.
ICMP (Internet Control Message Protocol) is used for network diagnostics (like ping).
"""

from scapy.all import *
import sys

def create_icmp_packet(destination_ip):
    """
    Creates an ICMP Echo Request packet (ping packet).
    
    Args:
        destination_ip (str): The target IP address
    
    Returns:
        packet: A Scapy packet object
    
    How ICMP works:
    - ICMP packets are encapsulated in IP packets
    - Type 8 = Echo Request (ping)
    - Type 0 = Echo Reply (pong)
    - Used for network diagnostics, error reporting
    """
    
    print("="*60)
    print("Creating ICMP Packet")
    print("="*60)
    
    # Create an IP layer with the destination address
    # IP() creates an IPv4 header
    # dst= sets the destination IP address
    ip_layer = IP(dst=destination_ip)
    
    # Create an ICMP layer
    # ICMP() creates an ICMP header with default type=8 (Echo Request)
    # This is what the 'ping' command uses
    icmp_layer = ICMP()
    
    # Combine the layers using the / operator
    # This is Scapy's way of stacking protocol layers
    # Bottom layer (IP) / Top layer (ICMP)
    packet = ip_layer / icmp_layer
    
    print(f"[+] Created ICMP packet for destination: {destination_ip}")
    print(f"[+] ICMP Type: {icmp_layer.type} (Echo Request)")
    print(f"[+] ICMP Code: {icmp_layer.code}")
    
    return packet


def inspect_packet(packet):
    """
    Displays detailed information about the packet structure.
    
    Args:
        packet: A Scapy packet object
    
    This shows:
    - All protocol layers in the packet
    - Field values for each layer
    - Packet size and structure
    """
    
    print("\n" + "="*60)
    print("Inspecting Packet Structure")
    print("="*60)
    
    # show() displays a summary of all layers and their fields
    print("\n[+] Packet Summary:")
    packet.show()
    
    # Get a one-line summary of the packet
    print("\n[+] Packet One-Line Summary:")
    print(f"    {packet.summary()}")
    
    # Display individual layer information
    print("\n[+] Layer-by-Layer Analysis:")
    
    # Check if IP layer exists
    if packet.haslayer(IP):
        ip_layer = packet[IP]
        print(f"\n  [IP Layer]")
        print(f"    Source IP: {ip_layer.src}")
        print(f"    Destination IP: {ip_layer.dst}")
        print(f"    TTL (Time To Live): {ip_layer.ttl}")
        print(f"    Protocol: {ip_layer.proto} (1 = ICMP)")
    
    # Check if ICMP layer exists
    if packet.haslayer(ICMP):
        icmp_layer = packet[ICMP]
        print(f"\n  [ICMP Layer]")
        print(f"    Type: {icmp_layer.type} (8 = Echo Request, 0 = Echo Reply)")
        print(f"    Code: {icmp_layer.code}")
        print(f"    Checksum: {icmp_layer.chksum}")
        print(f"    ID: {icmp_layer.id}")
        print(f"    Sequence: {icmp_layer.seq}")
    
    # Display packet in hexadecimal format
    print("\n[+] Hexadecimal Dump:")
    hexdump(packet)
    
    # Get packet size
    print(f"\n[+] Packet Size: {len(packet)} bytes")


def send_icmp_packet(packet, verbose=True):
    """
    Sends an ICMP packet and waits for a response.
    
    Args:
        packet: The Scapy packet to send
        verbose (bool): Whether to display detailed output
    
    Returns:
        tuple: (answered, unanswered) packets
    
    How sr() works:
    - sr() = Send and Receive
    - Sends packets at layer 3 (network layer)
    - Waits for responses
    - timeout= how long to wait for response (in seconds)
    """
    
    print("\n" + "="*60)
    print("Sending ICMP Packet")
    print("="*60)
    
    try:
        print(f"[+] Sending packet to {packet[IP].dst}...")
        print("[+] Waiting for response (timeout: 2 seconds)...")
        
        # sr() sends packets and captures responses
        # timeout=2 means wait 2 seconds for a reply
        # verbose=0 suppresses Scapy's default output
        answered, unanswered = sr(packet, timeout=2, verbose=0)
        
        if answered:
            print(f"[+] Received {len(answered)} response(s)")
            return answered, unanswered
        else:
            print("[-] No response received (host may be down or blocking ICMP)")
            return None, unanswered
            
    except PermissionError:
        print("[-] Error: Need root/admin privileges to send raw packets")
        print("[-] Try running with: sudo python3 chapter_04_icmp.py")
        return None, None
    except Exception as e:
        print(f"[-] Error sending packet: {e}")
        return None, None


def analyze_response(answered_packets):
    """
    Analyzes the response(s) received from the target.
    
    Args:
        answered_packets: List of (sent_packet, received_packet) tuples
    
    This shows:
    - Response time (latency)
    - Response packet details
    - Whether the ping was successful
    """
    
    if not answered_packets:
        print("\n[-] No responses to analyze")
        return
    
    print("\n" + "="*60)
    print("Analyzing Response")
    print("="*60)
    
    # answered_packets is a list of (sent, received) tuples
    for sent, received in answered_packets:
        
        print(f"\n[+] Response received from {received[IP].src}")
        
        # Check if response contains ICMP layer
        if received.haslayer(ICMP):
            icmp_response = received[ICMP]
            
            # Type 0 = Echo Reply (successful ping)
            # Type 3 = Destination Unreachable
            # Type 11 = Time Exceeded
            if icmp_response.type == 0:
                print(f"[+] ICMP Type: {icmp_response.type} (Echo Reply - Success!)")
                print(f"[+] The Red Dragon legend location confirmed!")
            elif icmp_response.type == 3:
                print(f"[+] ICMP Type: {icmp_response.type} (Destination Unreachable)")
            elif icmp_response.type == 11:
                print(f"[+] ICMP Type: {icmp_response.type} (Time Exceeded)")
            else:
                print(f"[+] ICMP Type: {icmp_response.type}")
            
            print(f"[+] ICMP Code: {icmp_response.code}")
        
        # Display response packet details
        print("\n[+] Response Packet Details:")
        received.show()
        
        # Calculate round-trip time if available
        # This would require timestamp data which basic ICMP doesn't include
        # But we can show the packet was received successfully
        print("\n[+] Packet successfully sent and response received!")
        print("[+] Network path to 8.8.8.8 is accessible")


def main():
    """
    Main function demonstrating ICMP packet creation and sending.
    
    This script:
    1. Creates an ICMP Echo Request packet
    2. Inspects the packet structure
    3. Sends it to 8.8.8.8 (Google DNS)
    4. Analyzes the response
    """
    
    print("\n" + "🐉"*30)
    print("Chapter 4: The Legend of the Red Dragon - ICMP Quest")
    print("🐉"*30 + "\n")
    
    # Target IP address - 8.8.8.8 is Google's public DNS server
    # This is commonly used for network testing as it's highly available
    target_ip = "8.8.8.8"
    
    print(f"[*] Target: {target_ip} (Google Public DNS)")
    print("[*] This server is used for testing as it's reliable and always responds\n")
    
    # Step 1: Create the ICMP packet
    packet = create_icmp_packet(target_ip)
    
    # Step 2: Inspect the packet contents
    inspect_packet(packet)
    
    # Step 3: Send the packet and receive response
    answered, unanswered = send_icmp_packet(packet)
    
    # Step 4: Analyze the response
    if answered:
        analyze_response(answered)
    
    # Summary
    print("\n" + "="*60)
    print("Quest Summary")
    print("="*60)
    print("[+] Successfully created ICMP packet")
    print("[+] Inspected packet structure and contents")
    print(f"[+] Sent packet to {target_ip}")
    if answered:
        print("[+] Received and analyzed response")
        print("\n[✓] Quest Completed! The ancient magic of ICMP has been mastered!")
    else:
        print("[-] No response received, but packet was successfully created")
        print("\n[!] Quest partially completed - packet creation and sending successful")
    
    print("="*60)


if __name__ == "__main__":
    """
    Entry point - checks for root privileges before running.
    """
    
    # Check if running with sufficient privileges
    # Raw socket operations typically require root/admin access
    if os.geteuid() != 0:
        print("\n[!] Warning: This script typically requires root privileges")
        print("[!] If you get permission errors, try running:")
        print("[!] sudo python3 chapter_04_icmp.py\n")
    
    main()
