import sys

def get_user_command():
    sys.stdout.write("$ ")
    inp = input()
    return inp

def handle_command(inp):
    match inp:
        case "exit 0":
            sys.exit(0)
            return

    print(f'{inp}: command not found')

def main():
    # Uncomment this block to pass the first stage
    # Wait for user input
    while True:
        inp = get_user_command()
        handle_command(inp)



if __name__ == "__main__":
    main()
