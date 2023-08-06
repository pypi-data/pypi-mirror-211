import os
import subprocess
import colorama as ca
from tqdm import tqdm


def p_header(text):
    print(ca.Fore.CYAN + ca.Style.BRIGHT + text)
    print(ca.Style.RESET_ALL, end='')

def p_hint(text):
    print(ca.Fore.LIGHTBLACK_EX + ca.Style.BRIGHT + text)
    print(ca.Style.RESET_ALL, end='')

def p_success(text):
    print(ca.Fore.GREEN + ca.Style.BRIGHT + text)
    print(ca.Style.RESET_ALL, end='')

def p_fail(text):
    print(ca.Fore.RED + ca.Style.BRIGHT + text)
    print(ca.Style.RESET_ALL, end='')

def p_warning(text):
    print(ca.Fore.YELLOW + ca.Style.BRIGHT + text)
    print(ca.Style.RESET_ALL, end='')

def replace_str(fpath, d):
    ''' Replace the string in a given text file according
    to the dictionary `d`
    '''
    with open(fpath, 'r') as f:
        text = f.read()
        for k, v in d.items():
            search_text = k
            replace_text = v
            text = text.replace(search_text, replace_text)

    with open(fpath, 'w') as f:
        f.write(text)

def run_shell(cmd, timeout=None):
    print(f'CMD >>> {cmd}')
    try:
        subprocess.run(cmd, timeout=timeout, shell=True)
    except:
        pass

def svn_export(url, fpath=None):
    if fpath is None:
        fpath = os.path.basename(url)

    if os.path.exists(fpath): os.remove(fpath)
    run_shell(f'svn export {url} {fpath}')
    return fpath

def exec_script(fpath, args=None, timeout=None):
    run_shell(f'chmod +x {fpath}')
    if args is None:
        run_shell(f'./{fpath}', timeout=timeout)
    else:
        run_shell(f'./{fpath} {args}', timeout=timeout)