import os, re, sys

names = set()  # names of rules (usually output files)
slist = {}     # slist[name,i] is one of name's sources
scnt = {}      #   where i is 1..scnt[name]
cmd = {}       # cmd[name] is the shell command to run
age = {}       # age[file] is file's age (bigger is older)

def main():
    for line in open('makefile'):
        if re.match('[A-Za-z]', line):
            line = line.replace(':', '')
            fields = line.split()
            nm = fields[0]
            if nm in names:
                error(f'{nm} is multiply defined')
            names.add(nm)
            for field in fields[1:]:  # remember targets
                scnt[nm] = scnt.get(nm, 0) + 1
                slist[nm, scnt[nm]] = field
        elif line.startswith('\t'):   # remember cmd for current name
            cmd[nm] = cmd.get(nm, '') + line
        elif line.strip():
            error(f'illegal line in makefile: {line}')
    ages()  # compute initial ages
    if sys.argv[1] in names:
        if not update(sys.argv[1]):
            print(f'{sys.argv[1]} is up to date')
    else:
        error(f'{sys.argv[1]} is not in makefile')

def ages():
    entries = sorted(os.scandir('.'), key=lambda e: e.stat().st_mtime, reverse=True)
    for t, entry in enumerate(entries, start=1):
        age[entry.name] = t  # all existing files get an age
    for n in names:
        if n not in age:    # if n has not been created
            age[n] = 9999   # make n really old

def update(n, visited={}):
    if n not in age:
        error(f'{n} does not exist')
    if n not in names:
        return 0
    changed = 0
    visited[n] = 1
    for i in range(1, scnt.get(n, 0)+1):
        s = slist[n, i]
        if s not in visited:
            update(s)
        elif visited[s] == 1:
            error(f'{s} and {n} are circularly defined')
        if age[s] <= age[n]:
            changed += 1
    visited[n] = 2
    if changed or n not in scnt:
        print(cmd[n], end='')
        os.system(cmd[n])  # execute cmd associated with n
        ages()             # recompute all ages
        age[n] = 0         # make n very new
        return 1
    return 0

def error(msg):
    print(f'error: {msg}', file=sys.stderr)
    sys.exit(1)

if __name__ == '__main__':
    main()
