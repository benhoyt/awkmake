prog:	a.o b.o c.o
		cc a.o b.o c.o -o prog
a.o:	prog.h a.c
		cc -c prog.h a.c
b.o:	prog.h b.c
		cc -c prog.h b.c
c.o:	c.c
		cc -c c.c
c.c:	c.y
		yacc c.y
		mv y.tab.c c.c
print:
		pr prog.h a.c b.c c.y
