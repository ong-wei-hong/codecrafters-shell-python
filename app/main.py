import sys
import os
import subprocess

def mysplit(input):
    res = ['']
    current_quote = ''
    blackslash = False
    for c in input:
        if blackslash:
            blackslash = False
            res[-1] += c
        elif c == '\\' and current_quote == '':
            blackslash = True
        elif c in ["'", '"']:
            if current_quote == '':
                current_quote = c
            elif c == current_quote:
                current_quote = ''
            else:
                res[-1] += c
        elif c == ' ' and current_quote == '':
            if res[-1] != '':
                res.append('')
        else:
            res[-1] += c

    if res[-1] == '':
        res.pop()

    return res

def get_user_command():
    sys.stdout.write("$ ")
    inp = mysplit(input())
    return inp

def get_file(dirs, filename):
    for dir in dirs:
        filepath = f'{dir}/{filename}'
        if os.path.isfile(filepath):
            return filepath
    return None

def handle_command(inp,dirs,HOME):
    match inp:
        case ['exit', '0']:
            sys.exit(0)

        case ['echo', *args]:
            sys.stdout.write(' '.join(args) + '\n')

        case ['type', arg]:
            if arg in ['type', 'exit', 'echo', 'pwd', 'cd']:
                sys.stdout.write(f'{arg} is a shell builtin\n')
            elif (filepath := get_file(dirs, arg)):
                sys.stdout.write(f'{arg} is {filepath}\n')
            else:
                sys.stdout.write(f'{arg}: not found\n')

        case ['pwd']:
            sys.stdout.write(f'{os.getcwd()}\n')
        
        case ['cd', '~']:
            os.chdir(HOME)

        case ['cd', path]:
            if os.path.isdir(path):
                os.chdir(path)
            else:
                sys.stdout.write(f'cd: {path}: No such file or directory\n')
       
        case [file, *args]:
            if (filepath := get_file(dirs, file)):
                subprocess.run([filepath, *args])
            else:
                sys.stdout.write(f'{' '.join(inp)}: command not found\n')

def main(dirs,HOME):
    # Uncomment this block to pass the first stage
    # Wait for user input
    while True:
        inp = get_user_command()
        handle_command(inp,dirs,HOME)

if __name__ == "__main__":
    PATH = os.environ.get("PATH")
    dirs = PATH.split(':')
    HOME = os.environ.get("HOME")
    main(dirs, HOME)