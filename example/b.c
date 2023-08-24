#include <stdio.h>

void hello(void) {
	printf("hello, world\n");
}

int yylex() {
	return 0;
}

void yyerror(char *s) {
}
