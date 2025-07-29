#!/usr/bin/env python3
"""
Simple script to format code with black and isort.
Run this before committing to ensure code passes formatting checks.
"""

import subprocess
import sys


def run_command(cmd):
    """Run a command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"Running: {cmd}")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running {cmd}: {e}")
        return False


def main():
    """Format code with black and isort."""
    print("Formatting code with black and isort...")
    
    success = True
    
    # Format with black
    if not run_command("black apps/ config/ --line-length=127"):
        print("❌ Black formatting failed")
        success = False
    else:
        print("✅ Black formatting completed")
    
    # Format with isort
    if not run_command("isort apps/ config/ --profile=black --line-length=127"):
        print("❌ isort formatting failed")
        success = False
    else:
        print("✅ isort formatting completed")
    
    if success:
        print("🎉 All formatting completed successfully!")
        print("You can now commit your changes.")
    else:
        print("💥 Some formatting failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()