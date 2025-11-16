"""
Main entry point for IPFighter Checker
"""

import sys
import argparse
from .gui.app import run_app


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="IPFighter Proxy Checker - Check SOCKS5 proxies using IPFighter"
    )
    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=5,
        help="Maximum number of concurrent proxy checks (default: 5)"
    )
    
    args = parser.parse_args()
    
    # Validate workers
    if args.workers < 1:
        print("Error: Number of workers must be at least 1")
        sys.exit(1)
    if args.workers > 20:
        print("Warning: Using more than 20 workers may cause issues")
    
    # Run the application
    print(f"Starting IPFighter Checker with {args.workers} concurrent workers...")
    run_app(max_workers=args.workers)


if __name__ == "__main__":
    main()

