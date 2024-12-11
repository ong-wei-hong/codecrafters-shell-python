import sys
import os
import subprocess

def get_user_command():
    sys.stdout.write("$ ")
    inp = input().split(' ')
    return inp

def get_file(dirs, filename):
    for dir in dirs:
        filepath = f'{dir}/{filename}'
        if os.path.isfile(filepath):
            return filepath
    return None

def handle_command(inp,dirs):
    match inp:
        case ['exit', '0']:
            sys.exit(0)

        case ['echo', *args]:
            sys.stdout.write(' '.join(args) + '\n')

        case ['type', arg]:
            if arg in ['type', 'exit', 'echo']:
                sys.stdout.write(f'{arg} is a shell builtin\n')
            elif (filepath := get_file(dirs, arg)):
                sys.stdout.write(f'{arg} is {filepath}\n')
            else:
                sys.stdout.write(f'{arg}: not found\n')
        
        case [file, *args]:
            if (filepath := get_file(dirs, file)):
                subprocess.run([filepath, *args])
            else:
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
