import sys
import os

def get_user_command():
    sys.stdout.write("$ ")
    inp = input().split(' ')
    return inp

def handle_command(inp,dirs):
    match inp:
        case ['exit', '0']:
            sys.exit(0)

        case ['echo', *args]:
            sys.stdout.write(' '.join(args) + '\n')

        case ['type', arg]:
            if arg in ['type', 'exit', 'echo']:
                sys.stdout.write(f'{arg} is a shell builtin\n')
            else:
                for dir in dirs:
                    filepath = f'{dir}/{arg}'
                    if os.path.isfile(filepath):
                        sys.stdout.write(f'{arg} is {filepath}\n')
                        return
                
                sys.stdout.write(f'{arg}: not found\n')
        
        case _:
            sys.stdout.write(f'{' '.join(inp)}: command not found\n')

def main(dirs):
    # Uncomment this block to pass the first stage
    # Wait for user input
    while True:
        inp = get_user_command()
        handle_command(inp,dirs)

if __name__ == "__main__":
    PATH = os.environ.get("PATH")
    dirs = PATH.split(':')
    main(dirs)
