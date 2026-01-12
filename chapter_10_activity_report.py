#!/usr/bin/env python3
"""
Chapter 10: Activity Report - SAR Data Analysis
This script analyzes server activity using SAR (System Activity Reporter) data.
It parses CPU idle time and creates visualizations.
"""

import subprocess
import re
import matplotlib.pyplot as plt
from datetime import datetime
import sys

def get_sar_data():
    """
    Retrieves SAR data from the system.
    
    SAR (System Activity Report) is a Linux tool that:
    - Collects system performance data
    - Records CPU, memory, I/O statistics
    - Stored in /var/log/sa/ directory
    
    Returns:
        str: SAR command output
    """
    
    print("="*60)
    print("Retrieving SAR Data")
    print("="*60)
    
    try:
        # Run sar command to get CPU statistics
        # -u: CPU utilization
        # ALL: all CPUs
        result = subprocess.run(
            ['sar', '-u', 'ALL'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("[+] Successfully retrieved SAR data")
            return result.stdout
        else:
            print(f"[-] SAR command failed: {result.stderr}")
            return None
            
    except FileNotFoundError:
        print("[-] SAR not found. Install with: sudo apt install sysstat")
        return None
    except Exception as e:
        print(f"[-] Error: {e}")
        return None


def parse_sar_data(sar_output):
    """
    Parses SAR output to extract %idle values.
    
    Args:
        sar_output (str): Raw SAR command output
    
    Returns:
        list: List of tuples (timestamp, idle_percentage)
    
    SAR output format example:
    12:00:01 AM     CPU     %user     %nice   %system   %iowait    %steal     %idle
    12:10:01 AM     all      5.23      0.00      2.15      0.45      0.00     92.17
    """
    
    print("\n" + "="*60)
    print("Parsing SAR Data")
    print("="*60)
    
    data_points = []
    lines = sar_output.split('\n')
    
    for line in lines:
        # Skip header lines and empty lines
        if not line.strip() or 'CPU' in line or 'Average' in line or 'Linux' in line:
            continue
        
        # Split line by whitespace
        parts = line.split()
        
        # Try to parse the line
        try:
            # Typically: time, AM/PM, CPU, %user, %nice, %system, %iowait, %steal, %idle
            if len(parts) >= 9:
                time_str = parts[0] + ' ' + parts[1]
                idle_value = float(parts[-1])  # %idle is usually last column
                
                data_points.append((time_str, idle_value))
                
        except (ValueError, IndexError):
            # Skip lines that don't match expected format
            continue
    
    print(f"[+] Parsed {len(data_points)} data points")
    
    return data_points


def create_activity_graph(data_points, filename='server_activity.png'):
    """
    Creates a graph showing server activity over time.
    
    Args:
        data_points: List of (timestamp, idle_percentage) tuples
        filename: Output filename for the graph
    
    The graph shows:
    - X-axis: Time
    - Y-axis: CPU idle percentage
    - Lower idle% = higher activity (busier server)
    """
    
    print("\n" + "="*60)
    print("Creating Activity Graph")
    print("="*60)
    
    if not data_points:
        print("[-] No data to plot")
        return False
    
    # Separate timestamps and values
    timestamps = [point[0] for point in data_points]
    idle_values = [point[1] for point in data_points]
    
    # Calculate CPU usage (100 - idle)
    usage_values = [100 - idle for idle in idle_values]
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    
    # Plot CPU usage
    plt.plot(range(len(timestamps)), usage_values, 
             marker='o', linestyle='-', linewidth=2, 
             markersize=6, color='red', label='CPU Usage %')
    
    # Plot idle percentage for comparison
    plt.plot(range(len(timestamps)), idle_values, 
             marker='s', linestyle='--', linewidth=1, 
             markersize=4, color='green', alpha=0.5, label='CPU Idle %')
    
    # Customize the plot
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Percentage', fontsize=12)
    plt.title('Server Activity Monitor - CPU Usage Over Time', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Rotate x-axis labels for better readability
    # Only show subset of labels if too many
    step = max(1, len(timestamps) // 10)
    plt.xticks(range(0, len(timestamps), step), 
               [timestamps[i] for i in range(0, len(timestamps), step)],
               rotation=45, ha='right')
    
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"[+] Graph saved to: {filename}")
    
    # Also display statistics
    print("\n[Statistics]")
    print(f"  Average CPU Usage: {sum(usage_values)/len(usage_values):.2f}%")
    print(f"  Average CPU Idle: {sum(idle_values)/len(idle_values):.2f}%")
    print(f"  Peak CPU Usage: {max(usage_values):.2f}%")
    print(f"  Lowest CPU Usage: {min(usage_values):.2f}%")
    
    return True


def generate_sample_data():
    """
    Generates sample SAR data for demonstration purposes.
    Use this if SAR is not available on the system.
    
    Returns:
        list: Sample data points
    """
    
    print("\n[*] Generating sample SAR data...")
    
    import random
    
    data_points = []
    base_time = "12:00:00"
    
    for i in range(20):
        # Generate time
        hour = 12 + (i // 6)
        minute = (i % 6) * 10
        time_str = f"{hour:02d}:{minute:02d}:00 PM"
        
        # Generate idle percentage with some variation
        # Simulate server under load
        base_idle = 70
        variation = random.uniform(-20, 20)
        idle = max(30, min(95, base_idle + variation))
        
        data_points.append((time_str, idle))
    
    return data_points


def apply_server_load():
    """
    Generates artificial load on the server for testing.
    
    This creates CPU-intensive operations to observe
    the impact on the activity graph.
    """
    
    print("\n" + "="*60)
    print("Applying Server Load")
    print("="*60)
    
    print("[*] Starting stress test...")
    print("[*] This will consume CPU for monitoring purposes")
    print("[*] Press Ctrl+C to stop")
    
    try:
        # Simple CPU-intensive operation
        # In practice, use tools like 'stress' or 'stress-ng'
        import time
        start = time.time()
        
        while time.time() - start < 30:  # Run for 30 seconds
            # Intensive computation
            sum([i**2 for i in range(10000)])
            
        print("\n[+] Load test completed")
        
    except KeyboardInterrupt:
        print("\n[!] Load test interrupted")


def main():
    """
    Main function for activity reporting.
    """
    
    print("\n" + "🏔️"*30)
    print("Chapter 10: The Mage's Tower - Activity Report Quest")
    print("🏔️"*30 + "\n")
    
    print("[*] You journey toward the distant tower...")
    print("[*] Time to monitor server activity!\n")
    
    # Check if user wants to use real or sample data
    print("="*60)
    print("Data Source Selection")
    print("="*60)
    print("[1] Use real SAR data (requires sysstat)")
    print("[2] Use sample generated data")
    
    choice = input("\nEnter choice (1/2): ").strip()
    
    if choice == '1':
        # Try to get real SAR data
        sar_output = get_sar_data()
        
        if sar_output:
            data_points = parse_sar_data(sar_output)
        else:
            print("\n[!] Falling back to sample data")
            data_points = generate_sample_data()
    else:
        # Use sample data
        data_points = generate_sample_data()
    
    # Create visualization
    if data_points:
        create_activity_graph(data_points)
        
        # Ask if user wants to apply load
        print("\n" + "="*60)
        print("Load Testing")
        print("="*60)
        
        response = input("\n[?] Apply server load for testing? (yes/no): ").strip().lower()
        
        if response in ['yes', 'y']:
            apply_server_load()
            print("\n[*] You can run SAR again to see the impact")
    
    print("\n" + "="*60)
    print("Quest Complete!")
    print("="*60)
    print("[✓] Analyzed server activity data")
    print("[✓] Created activity visualization")
    print("[*] The tower's secrets are revealed through monitoring!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
