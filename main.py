import sys
from secret_message import print_secret_messages

def main():
    using_url = ""
    if len(sys.argv) > 1:
        using_url = sys.argv[1]
    else:
        print("expecting argument for doc url.")
        return
    print_secret_messages(using_url)

if __name__ == "__main__":
    main()