grammar FSA;

file
    : section+ EOF
    ;

section
    : alphabet
    | states
    | start
    | accepting
    | transitions
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
START       : 'initial_state' ;
ACCEPTING   : 'accepting_states' ;
TRANSITIONS : 'transitions' ;

COLON   : ':' ;
COMMA   : ',' ;
LBRACE  : '{' ;
RBRACE  : '}' ;
EQUAL   : '=' ;
DASH    : '-' ;
ARROW   : '->' ;

ID
    : [a-zA-Z_] [a-zA-Z_0-9]*
    ;

SYMBOL
    : [a-zA-Z0-9]
    ;

EPSILON
    : 'ε'
    | 'eps'
    | 'epsilon'
    ;

STRING
    : '"' ( '\\' . | ~["\\] )* '"'
    ;

COMMENT
    : '#' ~[\r\n]* -> skip
    ;

WS
    : [ \t\r\n]+ -> skip
    ;
