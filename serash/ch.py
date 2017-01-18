import sys, os, shlex

cmds_posix = {}

status_run = 1
status_stop = 0

def tokenize(string):
    return shlex.split(string)

def execute(tokens):
    cmd_pos = tokens[0]
    cmd_arg = tokens[1:]

    if cmd_pos in cmds_posix:
        return cmds_posix[cmd_pos](cmd_args)

    pid = os.fork()

    if pid == 0:
        os.execvp(tokens[0], tokens)
    elif pid > 0:
        while True:
            wpid, status = os.waitpid(pid, 0)

            if os.WIFEXITED(status) or os.WIFSIGNALED(status):
                break
    return status_run

def loop():
    status = status_run

    while status == status_run:
        sys.stdout.write('Seraf BASH ' + os.getcwd() + ' :~$')
        sys.stdout.flush()

        cmd = sys.stdin.readline()

        cmd_tokens = tokenize(cmd)

        status = execute(cmd_tokens)

def cd(args):
    os.chdir(args[0])
    return status_run

def exit(args):
    return status_stop

def add_cmd(name, function):
    cmds_posix[name] = function

def init():
    add_cmd("cd", cd)
    add_cmd("exit", exit)

def main():
    init()
    loop()

if __name__ == "__main__":
    main()
