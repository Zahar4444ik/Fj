grammar FSA;

file
    : alphabet states start accepting transitions EOF
    ;

alphabet
    : ALPHABET COLON LBRACE symbol (COMMA symbol)* COMMA? RBRACE
    ;

states
    : STATES COLON LBRACE stateEntry (COMMA stateEntry)* COMMA? RBRACE
    ;

stateEntry
    : ID (EQUAL STRING)?
    ;

start
    : START COLON ID
    ;

accepting
    : ACCEPTING COLON LBRACE ID (COMMA ID)* COMMA? RBRACE
    ;

transitions
    : TRANSITIONS COLON LBRACE transition (COMMA transition)* COMMA? RBRACE
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

ALPHABET    : 'alphabet' ;
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
