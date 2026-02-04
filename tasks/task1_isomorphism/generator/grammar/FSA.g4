grammar FSA;

file
    : states start accepting transitions EOF
    ;

states
    : STATES COLON LBRACE stateEntry (COMMA stateEntry)* RBRACE
    ;

stateEntry
    : ID (EQUAL STRING)?
    ;

start
    : START COLON ID
    ;

accepting
    : ACCEPTING COLON LBRACE ID (COMMA ID)* RBRACE
    ;

transitions
    : TRANSITIONS COLON transition+
    ;

transition
    : ID DASH symbol ARROW ID
    ;

symbol
    : SYMBOL
    | ID
    | EPSILON
    ;

/* ---------- Lexer ---------- */

STATES      : 'states' ;
START       : 'start' ;
ACCEPTING   : 'accepting' ;
TRANSITIONS : 'transitions' ;

COLON   : ':' ;
COMMA   : ',' ;
LBRACE  : '{' ;
RBRACE  : '}' ;
EQUAL   : '=' ;
DASH    : '-' ;
ARROW   : '->' ;

SYMBOL
    : [0-9]
    ;

ID
    : [a-zA-Z_] [a-zA-Z_0-9]*
    ;

EPSILON
    : 'ε'
    | 'eps'
    | 'epsilon'
    ;

STRING
    : '"' ( '\\' . | ~["\\] )* '"'
    ;

WS
    : [ \t\r\n]+ -> skip
    ;
