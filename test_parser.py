#!/usr/bin/env python3
"""
Simple test script to verify proxy parsing works correctly
Run this before running the full application to test basic functionality
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.proxy_parser import parse_proxy_string, parse_proxy_list
from src.utils.validators import validate_proxy_string

def test_parsing():
    """Test proxy parsing functionality"""
    
    print("=" * 60)
    print("IPFighter Checker - Proxy Parser Test")
    print("=" * 60)
    print()
    
    # Test cases
    test_proxies = [
        "us.922s5.net:6300:62455833dA-zone-custom-region-US-city-Manvel-sessid-LjKEgCfz:EO1QSEJN",
        "proxy.example.com:1080:username:password",
        "simple-proxy.com:8080",
        "user:pass@another-proxy.com:5000",
    ]
    
    print("Testing individual proxy parsing:")
    print("-" * 60)
    
    for i, proxy_str in enumerate(test_proxies, 1):
        print(f"\n{i}. Testing: {proxy_str}")
        
        # Validate
        is_valid, error = validate_proxy_string(proxy_str)
        if is_valid:
            print("   ✓ Validation: PASSED")
        else:
            print(f"   ✗ Validation: FAILED - {error}")
            continue
        
        # Parse
        proxy = parse_proxy_string(proxy_str)
        if proxy:
            print(f"   ✓ Parsing: SUCCESS")
            print(f"     - Host: {proxy.host}")
            print(f"     - Port: {proxy.port}")
            if proxy.username:
                print(f"     - Username: {proxy.username}")
            if proxy.password:
                print(f"     - Password: {'*' * len(proxy.password)}")
        else:
            print("   ✗ Parsing: FAILED")
    
    print()
    print("-" * 60)
    
    # Test list parsing
    print("\nTesting multi-line proxy list parsing:")
    print("-" * 60)
    
    proxy_list_text = "\n".join(test_proxies)
    proxies = parse_proxy_list(proxy_list_text)
    
    print(f"Input: {len(test_proxies)} proxy strings")
    print(f"Parsed: {len(proxies)} valid proxies")
    
    if len(proxies) == len(test_proxies):
        print("✓ All proxies parsed successfully!")
    else:
        print(f"⚠ Warning: Only {len(proxies)}/{len(test_proxies)} proxies parsed")
    
    print()
    print("=" * 60)
    print("Test complete! If all tests passed, you're ready to run the app.")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Run setup: ./scripts/setup_linux.sh")
    print("2. Run app: ./scripts/run_linux.sh")
    print()


if __name__ == "__main__":
    try:
        test_parsing()
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

