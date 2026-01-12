#!/usr/bin/env python3
"""
Chapter 9: HTTP Requests
This script demonstrates making HTTP requests using the requests library.
HTTP is the foundation of web communication and APIs.
"""

import requests
import json
import sys

def make_get_request(url):
    """
    Makes a simple GET request to a URL.
    
    Args:
        url (str): The URL to request
    
    Returns:
        requests.Response: The response object
    
    GET requests:
    - Used to retrieve data
    - Parameters in URL query string
    - Safe and idempotent (can be repeated)
    - Can be cached
    """
    
    print("="*60)
    print(f"Making GET Request to: {url}")
    print("="*60)
    
    try:
        # Make the GET request
        # timeout= prevents hanging forever
        response = requests.get(url, timeout=10)
        
        # Check if request was successful
        # 200-299 status codes are success
        response.raise_for_status()
        
        print(f"[+] Status Code: {response.status_code}")
        print(f"[+] Response Time: {response.elapsed.total_seconds():.2f} seconds")
        print(f"[+] Content Length: {len(response.content)} bytes")
        
        return response
        
    except requests.exceptions.Timeout:
        print(f"[-] Request timed out after 10 seconds")
        return None
    except requests.exceptions.ConnectionError:
        print(f"[-] Failed to connect to {url}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"[-] HTTP Error: {e}")
        return None
    except Exception as e:
        print(f"[-] Error: {e}")
        return None


def display_response_headers(response):
    """
    Displays HTTP response headers.
    
    Args:
        response: requests.Response object
    
    Headers contain metadata about the response:
    - Content-Type: Format of the data
    - Content-Length: Size in bytes
    - Server: Web server software
    - Date: When response was generated
    """
    
    print("\n" + "="*60)
    print("Response Headers")
    print("="*60)
    
    for key, value in response.headers.items():
        print(f"{key}: {value}")


def parse_json_response(response):
    """
    Parses JSON response data.
    
    Args:
        response: requests.Response object
    
    Returns:
        dict: Parsed JSON data
    
    Many APIs return JSON format:
    - Lightweight data format
    - Easy to parse in any language
    - Human-readable
    """
    
    print("\n" + "="*60)
    print("Parsing JSON Response")
    print("="*60)
    
    try:
        # Parse JSON from response
        # .json() automatically decodes the response
        data = response.json()
        
        print("[+] Successfully parsed JSON data")
        print("\nData structure:")
        print(json.dumps(data, indent=2))
        
        return data
        
    except json.JSONDecodeError:
        print("[-] Response is not valid JSON")
        print(f"[-] Content: {response.text[:200]}...")
        return None


def make_request_with_params(base_url, params):
    """
    Makes a GET request with query parameters.
    
    Args:
        base_url (str): Base URL
        params (dict): Query parameters
    
    Query parameters are added to the URL:
    - https://api.example.com/search?q=dragon&limit=10
    - Used for filtering, pagination, search
    """
    
    print("\n" + "="*60)
    print("GET Request with Parameters")
    print("="*60)
    
    print(f"[*] Base URL: {base_url}")
    print(f"[*] Parameters: {params}")
    
    try:
        # requests automatically encodes params in the URL
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        
        print(f"[+] Final URL: {response.url}")
        print(f"[+] Status: {response.status_code}")
        
        return response
        
    except Exception as e:
        print(f"[-] Error: {e}")
        return None


def make_post_request(url, data):
    """
    Makes a POST request with data.
    
    Args:
        url (str): The URL to post to
        data (dict): Data to send in request body
    
    Returns:
        requests.Response: The response object
    
    POST requests:
    - Used to send data to server
    - Data in request body (not URL)
    - Used for creating resources, submitting forms
    - Not safe or idempotent
    """
    
    print("\n" + "="*60)
    print(f"Making POST Request to: {url}")
    print("="*60)
    
    print(f"[*] Sending data: {data}")
    
    try:
        # Make POST request with JSON data
        # json= automatically sets Content-Type header
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        
        print(f"[+] Status Code: {response.status_code}")
        print(f"[+] Response: {response.text}")
        
        return response
        
    except Exception as e:
        print(f"[-] Error: {e}")
        return None


def make_request_with_headers(url, custom_headers):
    """
    Makes a request with custom headers.
    
    Args:
        url (str): URL to request
        custom_headers (dict): Custom HTTP headers
    
    Common headers:
    - User-Agent: Identifies the client
    - Authorization: Authentication token
    - Accept: Expected response format
    """
    
    print("\n" + "="*60)
    print("Request with Custom Headers")
    print("="*60)
    
    print(f"[*] Custom headers: {custom_headers}")
    
    try:
        response = requests.get(url, headers=custom_headers, timeout=10)
        response.raise_for_status()
        
        print(f"[+] Request successful")
        return response
        
    except Exception as e:
        print(f"[-] Error: {e}")
        return None


def main():
    """
    Main function demonstrating various HTTP request scenarios.
    """
    
    print("\n" + "💧"*30)
    print("Chapter 9: The Peaceful Cascade - HTTP Requests Quest")
    print("💧"*30 + "\n")
    
    print("[*] You follow the directions to a beautiful cascade...")
    print("[*] Time to master the art of HTTP requests!\n")
    
    # Example 1: Simple GET request to a public API
    print("\n" + "🔵"*30)
    print("Example 1: Simple GET Request")
    print("🔵"*30)
    
    # Using JSONPlaceholder - a free fake API for testing
    url = "https://jsonplaceholder.typicode.com/posts/1"
    response = make_get_request(url)
    
    if response:
        display_response_headers(response)
        parse_json_response(response)
    
    # Example 2: GET request with parameters
    print("\n" + "🔵"*30)
    print("Example 2: GET Request with Parameters")
    print("🔵"*30)
    
    base_url = "https://jsonplaceholder.typicode.com/posts"
    params = {
        'userId': 1,
        '_limit': 3
    }
    response = make_request_with_params(base_url, params)
    
    if response:
        data = parse_json_response(response)
        if data:
            print(f"\n[+] Retrieved {len(data)} posts")
    
    # Example 3: POST request
    print("\n" + "🔵"*30)
    print("Example 3: POST Request")
    print("🔵"*30)
    
    post_url = "https://jsonplaceholder.typicode.com/posts"
    post_data = {
        'title': 'The Legend of the Red Dragon',
        'body': 'An ancient beast threatens the village...',
        'userId': 1
    }
    make_post_request(post_url, post_data)
    
    # Example 4: Request with custom headers
    print("\n" + "🔵"*30)
    print("Example 4: Custom Headers")
    print("🔵"*30)
    
    headers = {
        'User-Agent': 'ArrakisQuest/1.0',
        'Accept': 'application/json'
    }
    response = make_request_with_headers(url, headers)
    
    # Example 5: Checking different HTTP methods
    print("\n" + "🔵"*30)
    print("Example 5: Other HTTP Methods")
    print("🔵"*30)
    
    print("\n[*] Demonstrating different HTTP methods:")
    
    # DELETE request
    try:
        delete_url = "https://jsonplaceholder.typicode.com/posts/1"
        response = requests.delete(delete_url, timeout=10)
        print(f"[+] DELETE request: Status {response.status_code}")
    except Exception as e:
        print(f"[-] DELETE error: {e}")
    
    # PUT request
    try:
        put_url = "https://jsonplaceholder.typicode.com/posts/1"
        put_data = {'title': 'Updated Title', 'body': 'Updated content', 'userId': 1}
        response = requests.put(put_url, json=put_data, timeout=10)
        print(f"[+] PUT request: Status {response.status_code}")
    except Exception as e:
        print(f"[-] PUT error: {e}")
    
    # Summary
    print("\n" + "="*60)
    print("Quest Summary")
    print("="*60)
    print("[✓] Performed GET requests")
    print("[✓] Used query parameters")
    print("[✓] Sent POST requests with data")
    print("[✓] Added custom headers")
    print("[✓] Explored different HTTP methods")
    print("\n[*] You've mastered HTTP requests!")
    print("[*] The cascade's waters flow with knowledge...")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
