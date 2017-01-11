import sys, shlex, os
from Serash.constants import *

built_in_cmds = {}

SHELL_STATUS_RUN = 1
SHELL_STATUS_STOP = 0

#Splitting the user's command
#(mkdir "my folder") will return a list ['mkdir', '"my folder"]
def tokenize(string):
    return shlex.split(string)

def execute(cmd_tokens):
    cmd_name = cmd_tokens[0]
    cmd_args = cmd_tokens[1:]

    if cmd_name in built_in_cmds:
        return built_in_cmds[cmd_name](cmd_args)

    pid = os.fork()

    if pid == 0:
        os.execvp(cmd_tokens[0], cmd_tokens)
    elif pid > 0:
        while True:
            wpid, status = os.waitpid(pid, 0)

            if os.WIFEXITED(status) or os.WIFSIGNALED(status):
                break
            
    return SHELL_STATUS_RUN

def shell_loop():
    status = SHELL_STATUS_RUN

    while status == SHELL_STATUS_RUN:
        sys.stdout.write('> ')
        sys.stdout.flush()

        cmd = sys.stdin.readline()

        cmd_tokens = tokenize(cmd)

        status = execute(cmd_tokens)

def register_command(name, func):
    built_in_cmds[name] = func
        
def init():
    register_command("cd", cd)
        
def main():
    init()
    shell_loop()

if __name__ == "__main__":
    main()
