
This repo is intended to go with my article, ["The AWK book's 60-line version of Make"](https://benhoyt.com/writings/awk-make/). It contains `make.awk`, the minimalist Make program written in AWK that's included in *The AWK Programming Language*, as well as `make.py`, my Python port of the program.

To try the programs, clone the repo and `cd` to the `example` directory:

```
$ git clone https://github.com/benhoyt/awkmake
$ cd example
```

To run the AWK version (ignore the `yacc` warnings):

```
$ awk -f ../make.awk prog
		gcc -c prog.h a.c
		gcc -c prog.h b.c
		yacc c.y
		mv y.tab.c c.c
c.y: warning: 1 reduce/reduce conflict [-Wconflicts-rr]
c.y: note: rerun with option '-Wcounterexamples' to generate conflict counterexamples
		gcc -c c.c
c.c: In function ‘yyparse’:
c.c:1034:16: warning: implicit declaration of function ‘yylex’ [-Wimplicit-function-declaration]
 1034 |       yychar = yylex ();
      |                ^~~~~
y.tab.c:1169:7: warning: implicit declaration of function ‘yyerror’; did you mean ‘yyerrok’? [-Wimplicit-function-declaration]
		gcc a.o b.o c.o -o prog

$ awk -f ../make.awk prog
prog is up to date

$ touch a.c
$ awk -f ../make.awk prog
		gcc -c prog.h a.c
		gcc a.o b.o c.o -o prog

$ awk -f ../make.awk prog
prog is up to date
```

To run the Python version:

```
$ python3 ../make.py prog
prog is up to date
```
