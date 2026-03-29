import sys

def main():
    """Main entry point of the script."""
    print("Hello, world! This script is running directly.")
    
    # You can access command-line arguments using sys.argv
    if len(sys.argv) > 1:
        print(f"Arguments passed: {sys.argv[1:]}")
    else:
        print("No arguments passed.")

if __name__ == "__main__":
    # The code in this block runs only when the file is executed as a script.
    main()