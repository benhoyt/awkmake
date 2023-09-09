BEGIN {
    while (getline <"makefile" > 0)
        if ($0 ~ /^[A-Za-z]/) {  #  $1: $2 $3 ...
            sub(/:/, "")
            if (slist[nm = $1])
                error(nm " is multiply defined")
            sub(/^\S+\s*/, "")        # remove first field
            slist[nm] = $0            # remember targets
        } else if ($0 ~ /^\t/)        # remember cmd for
            cmd[nm] = cmd[nm] $0 "\n" #   current name
        else if (NF > 0)
            error("illegal line in makefile: " $0)
    if (ARGV[1] in slist) {
        if (update(ARGV[1]) == 0)
            print ARGV[1] " is up to date"
    } else
        error(ARGV[1] " is not in makefile")
}

function mtime(f,      cmd,t,ret) {
    cmd = "TZ=UTC stat --format %y " f " 2>/dev/null"
    cmd | getline t
    close(cmd)
    return t  # will be "" if f doesn't exist
}
function update(n,   changed,i,s,ndeps,deps,ntime) {
    ntime = mtime(n)
    if (!(n in slist) && ntime == "") error(n " does not exist")
    if (!(n in slist)) return 0
    changed = 0
    visited[n] = 1
    ndeps = split(slist[n], deps)
    for (i = 1; i <= ndeps; i++) {
        if (visited[s = deps[i]] == 0) update(s)
        else if (visited[s] == 1)
            error(s " and " n " are circularly defined")
        if (mtime(s) > ntime) changed++
    }
    visited[n] = 2
    if (changed || slist[n] == "") {
        printf("%s", cmd[n])
        system(cmd[n])  # execute cmd associated with n
        return 1
    }
    return 0
}
function error(s) { print "error: " s; exit }
