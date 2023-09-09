import os, re, sys

slist = {}  # slist[name] is list of rule's sources
cmd = {}    # cmd[name] is shell command to run for rule

def main():
    for line in open('makefile'):
        if re.match('[A-Za-z]', line):
            line = line.replace(':', '')
            fields = line.split()
            nm = fields[0]
            if nm in slist:
                error(f'{nm} is multiply defined')
            slist[nm] = fields[1:]    # remember targets
        elif line.startswith('\t'):   # remember cmd for current name
            cmd[nm] = cmd.get(nm, '') + line
        elif line.strip():
            error(f'illegal line in makefile: {line}')
    if sys.argv[1] in slist:
        if not update(sys.argv[1]):
            print(sys.argv[1], 'is up to date')
    else:
        error(f'{sys.argv[1]} is not in makefile')

def mtime(n):
    try:
        return os.stat(n).st_mtime
    except FileNotFoundError:
        return 0  # mark as old if it doesn't exist

def update(n, visited={}):
    ntime = mtime(n)
    if n not in slist and ntime == 0:
        error(f'{n} does not exist')
    if n not in slist:
        return 0
    changed = False
    visited[n] = 1
    for s in slist.get(n, []):
        if s not in visited:
            update(s)
        elif visited[s] == 1:
            error(f'{s} and {n} are circularly defined')
        if mtime(s) > ntime:
            changed = True
    visited[n] = 2
    if changed or len(slist.get(n, [])) == 0:
        print(cmd[n], end='')
        os.system(cmd[n])  # execute cmd associated with n
        return 1
    return 0

def error(msg):
    print('error:', msg, file=sys.stderr)
    sys.exit(1)

if __name__ == '__main__':
    main()
