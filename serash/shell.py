import sys, shlex, os
from serash.constants import *
from serash.builtins import *

built_in_cmds = {}

stat_r = 1
stat_s = 0

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
        try :
            status = os.execvp(cmd_tokens[0], cmd_tokens)
        except OSError as FileNotFoundError :
            print ("commande not fount !")
            return stat_r
    elif pid > 0:
        while True:
            wpid, status = os.waitpid(pid, 0)

            if os.WIFEXITED(status) or os.WIFSIGNALED(status):
                break
            
    return stat_r

def shell_loop():
    status = stat_r

    while status == stat_r:
        sys.stdout.write('seraf@ > ')
        sys.stdout.flush()

        cmd = sys.stdin.readline()

        cmd_tokens = tokenize(cmd)

        status = execute(cmd_tokens)

def register_command(name, func):
    built_in_cmds[name] = func
        
def init():
    register_command("cd", cd)
    register_command("exit", exit)
    
def main():
    init()
    shell_loop()

if __name__ == "__main__":
    main()
