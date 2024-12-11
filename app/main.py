import sys

def get_user_command():
    sys.stdout.write("$ ")
    inp = input().split(' ')
    return inp

def handle_command(inp):
    match inp:
        case ['exit', '0']:
            sys.exit(0)

        case ['echo', *args]:
            sys.stdout.write(' '.join(args) + '\n')

        case ['type', arg]:
            if arg in ['type', 'exit', 'echo']:
                sys.stdout.write(f'{arg} is a shell builtin\n')
            else:
                sys.stdout.write(f'{arg}: not found\n')
        
        case _:
            sys.stdout.write(f'{' '.join(inp)}: command not found\n')

def main():
    # Uncomment this block to pass the first stage
    # Wait for user input
    while True:
        inp = get_user_command()
        handle_command(inp)

if __name__ == "__main__":
    main()
