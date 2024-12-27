import sys
import os
import subprocess

def mysplit(input):
    res = ['']
    current_quote = ''

    i=0
    while i < len(input):
        c = input[i]
        if c == '\\':
            ch = input[i+1]
            if current_quote == "'":
                res[-1] += c
            elif current_quote == '"':
                ch = input[i+1]
                if ch in ['\\', '$', '"', '\n']:
                    res[-1] += ch
                else:
                    res[-1] += '\\' + ch
                
                i += 1
            else:
                res[-1] += input[i+1]
                i += 1
        elif c in ['"',"'"]:
            if current_quote == '':
                current_quote = c
            elif current_quote == c:
                current_quote = ''
            else:
                res[-1] += c
        elif c == ' ' and current_quote == '':
            if res[-1] != '':
                res.append('')
        else:
            res[-1] += c

        i += 1
        
    if res[-1] == '':
        res.pop()

    return res

def get_user_command():
    sys.stdout.write("$ ")
    out, err = sys.stdout, sys.stderr
    inp = mysplit(input())
    inp_idx = len(inp)

    if '1>' in inp:
        inp_idx = inp.index('1>')
        out = inp[inp_idx+1]
    elif '>' in inp:
        inp_idx = inp.index('>')
        out = inp[inp_idx+1]

    if '2>' in inp:
        idx = inp.index('2>')
        err = inp[idx+1]
        inp_idx = min(inp_idx, idx)

    inp = inp[:inp_idx]

    return inp, out, err

def get_file(dirs, filename):
    for dir in dirs:
        filepath = f'{dir}/{filename}'
        if os.path.isfile(filepath):
            return filepath
    return None

def handle_command(inp,dirs,HOME,out,err):
    toCloseOut, toCloseErr = False, False
    if type(out) is str:
        toCloseOut = True
        out = open(out, 'w+')

    if type(err) is str:
        toCloseErr = True
        err = open(err, 'w+')

    match inp:
        case ['exit', '0']:
            sys.exit(0)

        case ['echo', *args]:
            out.write(' '.join(args) + '\n')

        case ['type', arg]:
            if arg in ['type', 'exit', 'echo', 'pwd', 'cd']:
                out.write(f'{arg} is a shell builtin\n')
            elif (filepath := get_file(dirs, arg)):
                out.write(f'{arg} is {filepath}\n')
            else:
                out.write(f'{arg}: not found\n')

        case ['pwd']:
            out.write(f'{os.getcwd()}\n')
        
        case ['cd', '~']:
            os.chdir(HOME)

        case ['cd', path]:
            if os.path.isdir(path):
                os.chdir(path)
            else:
                err.write(f'cd: {path}: No such file or directory\n')
       
        case [file, *args]:
            if (filepath := get_file(dirs, file)):
                subprocess.run([filepath, *args],stdout=out, stderr=err)
            else:
                err.write(f'{' '.join(inp)}: command not found\n')

    if toCloseOut:
        out.close()

    if toCloseErr:
        err.close()

def main(dirs,HOME):
    # Uncomment this block to pass the first stage
    # Wait for user input
    while True:
        inp, out, err = get_user_command()
        handle_command(inp,dirs,HOME,out,err)

if __name__ == "__main__":
    PATH = os.environ.get("PATH")
    dirs = PATH.split(':')
    HOME = os.environ.get("HOME")
    main(dirs, HOME)