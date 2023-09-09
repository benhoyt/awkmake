import os, re, sys

slist = {}  # slist[target] is list of target's sources
cmd = {}    # cmd[name] is the shell command to run
age = {}    # age[file] is file's age (larger is older)

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
    ages()  # compute initial ages
    if sys.argv[1] in slist:
        if not update(sys.argv[1]):
            print(sys.argv[1], 'is up to date')
    else:
        error(f'{sys.argv[1]} is not in makefile')

def ages():
    entries = sorted(os.scandir(), key=lambda e: e.stat().st_mtime, reverse=True)
    for t, entry in enumerate(entries, start=1):
        age[entry.name] = t  # all existing files get an age
    for n in slist:
        if n not in age:     # if n has not been created
            age[n] = 9999    # make n really old

def update(n, visited={}):
    if n not in age:
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
        if age[s] <= age[n]:
            changed = True
    visited[n] = 2
    if changed or len(slist.get(n, [])) == 0:
        print(cmd[n], end='')
        os.system(cmd[n])  # execute cmd associated with n
        ages()             # recompute all ages
        age[n] = 0         # make n very new
        return 1
    return 0

def error(msg):
    print('error:', msg, file=sys.stderr)
    sys.exit(1)

if __name__ == '__main__':
    main()
