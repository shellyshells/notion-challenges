#!/usr/bin/env python3
"""
Chapter 6: Command-Line Options with argparse
This script demonstrates how to create a professional command-line interface
using Python's argparse module for parsing arguments.
"""

import argparse
import sys

def process_spell(spell_name, power_level, target):
    """
    Simulates casting a spell with given parameters.
    
    Args:
        spell_name (str): Name of the spell to cast
        power_level (int): Power level (1-10)
        target (str): Target of the spell
    
    Returns:
        dict: Result of the spell casting
    
    This function demonstrates how parsed arguments are used
    in actual program logic.
    """
    
    result = {
        'success': True,
        'spell': spell_name,
        'power': power_level,
        'target': target,
        'damage': power_level * 10
    }
    
    return result


def display_spell_result(result):
    """
    Displays the results of spell casting in a formatted way.
    
    Args:
        result (dict): The spell result dictionary
    """
    
    print("\n" + "="*60)
    print("⚡ SPELL CASTING RESULT ⚡")
    print("="*60)
    print(f"Spell: {result['spell']}")
    print(f"Target: {result['target']}")
    print(f"Power Level: {result['power']}/10")
    print(f"Damage Dealt: {result['damage']} HP")
    print(f"Status: {'SUCCESS' if result['success'] else 'FAILED'}")
    print("="*60)


def main():
    """
    Main function demonstrating argparse features.
    
    This shows:
    - Creating an argument parser
    - Adding positional and optional arguments
    - Short and long option names
    - Help text and descriptions
    - Argument types and validation
    - Default values
    """
    
    print("\n" + "📜"*30)
    print("Chapter 6: Alaric's Tavern - Command Line Arguments Quest")
    print("📜"*30 + "\n")
    
    # Create the argument parser
    # description= appears at the top of help message
    # epilog= appears at the bottom of help message
    # formatter_class helps with formatting
    parser = argparse.ArgumentParser(
        description='A spell casting system for the Alaric\'s Tavern quest',
        epilog='Example: python3 chapter_06_argparse.py -s "Fireball" -p 7 -t "Red Dragon"',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Add argument 1: Spell name (required, positional or optional)
    # We'll make it optional with -s/--spell
    # Short option: -s (single dash, single letter)
    # Long option: --spell (double dash, full word)
    # help= text shown in help message
    # required=True makes this mandatory despite being an option
    parser.add_argument(
        '-s', '--spell',
        type=str,
        required=True,
        help='Name of the spell to cast (required)'
    )
    
    # Add argument 2: Power level (optional with default)
    # type=int ensures the value is converted to integer
    # default= provides a fallback value if not specified
    # choices= restricts valid values
    parser.add_argument(
        '-p', '--power',
        type=int,
        default=5,
        choices=range(1, 11),  # Only allow 1-10
        metavar='LEVEL',  # Name shown in usage message
        help='Power level of the spell (1-10, default: 5)'
    )
    
    # Add argument 3: Target (optional with default)
    parser.add_argument(
        '-t', '--target',
        type=str,
        default='Training Dummy',
        help='Target of the spell (default: Training Dummy)'
    )
    
    # Add argument 4: Verbose mode (flag/boolean)
    # action='store_true' means this is a flag (no value needed)
    # If present: True, if absent: False
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output (show detailed information)'
    )
    
    # Add argument 5: Silent mode (opposite of verbose)
    # action='store_false' means default is True, becomes False if flag is present
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress all non-essential output'
    )
    
    # Add argument 6: Output file (optional)
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Save spell result to a file'
    )
    
    # Add argument 7: Repetitions (optional with validation)
    # We can add custom validation after parsing
    parser.add_argument(
        '-r', '--repeat',
        type=int,
        default=1,
        help='Number of times to cast the spell (default: 1)'
    )
    
    # Add argument 8: Element type (choice from list)
    parser.add_argument(
        '-e', '--element',
        type=str,
        choices=['fire', 'ice', 'lightning', 'dark', 'light'],
        default='fire',
        help='Element type of the spell (default: fire)'
    )
    
    # Parse the command-line arguments
    # This processes sys.argv and returns a Namespace object
    # All arguments are accessible as attributes of this object
    args = parser.parse_args()
    
    # Custom validation
    if args.repeat < 1 or args.repeat > 10:
        parser.error("Repeat count must be between 1 and 10")
    
    # Display parsed arguments if verbose mode is enabled
    if args.verbose:
        print("\n[DEBUG] Parsed Arguments:")
        print(f"  Spell: {args.spell}")
        print(f"  Power: {args.power}")
        print(f"  Target: {args.target}")
        print(f"  Element: {args.element}")
        print(f"  Repeat: {args.repeat}")
        print(f"  Verbose: {args.verbose}")
        print(f"  Quiet: {args.quiet}")
        print(f"  Output: {args.output}")
        print()
    
    # Main logic - cast the spell(s)
    if not args.quiet:
        print(f"\n[*] Preparing to cast {args.element.capitalize()} {args.spell}...")
        print(f"[*] Target: {args.target}")
        print(f"[*] Casting {args.repeat} time(s)...\n")
    
    results = []
    
    # Cast spell multiple times if repeat > 1
    for i in range(args.repeat):
        if args.verbose:
            print(f"[DEBUG] Cast #{i+1}/{args.repeat}")
        
        # Process the spell with parsed arguments
        result = process_spell(args.spell, args.power, args.target)
        result['element'] = args.element
        result['cast_number'] = i + 1
        results.append(result)
        
        if not args.quiet:
            display_spell_result(result)
    
    # Calculate total damage
    total_damage = sum(r['damage'] for r in results)
    
    if not args.quiet:
        print(f"\n[+] Total Damage Dealt: {total_damage} HP")
        print(f"[+] Successfully cast {len(results)} spell(s)!")
    
    # Save to file if output specified
    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.write("=== Spell Casting Log ===\n\n")
                for result in results:
                    f.write(f"Cast #{result['cast_number']}\n")
                    f.write(f"  Spell: {result['spell']}\n")
                    f.write(f"  Element: {result['element']}\n")
                    f.write(f"  Target: {result['target']}\n")
                    f.write(f"  Power: {result['power']}/10\n")
                    f.write(f"  Damage: {result['damage']} HP\n")
                    f.write("\n")
                f.write(f"Total Damage: {total_damage} HP\n")
            
            print(f"\n[+] Results saved to: {args.output}")
        except IOError as e:
            print(f"\n[-] Error saving to file: {e}")
    
    # Demonstrate passing args to another function
    # This is how you'd use argparse in a modular program
    print("\n[*] Passing arguments to another function...")
    process_args_in_function(args)
    
    print("\n[✓] Quest completed! You've mastered argparse!")


def process_args_in_function(args):
    """
    Demonstrates how to pass the parsed arguments to other functions.
    
    Args:
        args: The argparse Namespace object containing all parsed arguments
    
    This is the recommended way to structure programs:
    - Parse arguments in main()
    - Pass the args object to other functions
    - Each function accesses what it needs from args
    """
    
    print("\n[*] Function received arguments:")
    print(f"    - Spell name: {args.spell}")
    print(f"    - Power level: {args.power}")
    print(f"    - Target: {args.target}")
    
    # You can also convert args to a dictionary if needed
    args_dict = vars(args)
    print("\n[*] Arguments as dictionary:")
    for key, value in args_dict.items():
        print(f"    {key}: {value}")


if __name__ == "__main__":
    """
    Entry point of the script.
    
    Try running with different arguments:
    - python3 chapter_06_argparse.py -h
    - python3 chapter_06_argparse.py -s "Ice Storm" -p 10 -t "Goblin"
    - python3 chapter_06_argparse.py -s "Lightning" -v -r 3
    - python3 chapter_06_argparse.py -s "Fireball" -o results.txt
    """
    main()
