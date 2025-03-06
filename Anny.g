grammar Anny;

programa: inicio bloque fin EOF;

inicio: 'inicio';
fin: 'fin';

bloque: (instruccion)*;


instruccion: declaracion
           | asignacion
           | imprimir
           | leer
           | si
           | mientras
           | para
           | funcion
           | llamadaFuncion
           ;

declaracion: ('entero' | 'decimal' | 'cadena' | 'booleano') ID ('=' expresion)? ';';


asignacion: ID '=' expresion ';';


expresion: expresion ('+'|'-'|'*'|'/'|'%') expresion  
         | expresion ('=='|'!='|'<'|'>'|'<='|'>=') expresion
         | '(' expresion ')'  
         | ID  
         | NUMERO  
         | CADENA  
         | BOOLEANO
         ;


si: 'si' '(' expresion ')' 'entonces' bloque ('sino' bloque)? 'fin_si';


mientras: 'mientras' '(' expresion ')' 'hacer' bloque 'fin_mientras';

para: 'para' ID '=' expresion 'hasta' expresion ('con paso' expresion)? 'hacer' bloque 'fin_para';


funcion: 'funcion' ID '(' parametros? ')' 'hacer' bloque retorno? 'fin_funcion';

retorno: 'retorna' expresion ';';

parametros: ID (',' ID)*;


llamadaFuncion: ID '(' argumentos? ')' ';';
argumentos: expresion (',' expresion)*;


imprimir: 'imprimir' '(' expresion (',' expresion)* ')' ';';
leer: 'leer' '(' ID ')' ';';


NUMERO: [0-9]+('.'[0-9]+)?;
CADENA: '"' ~["]* '"';
BOOLEANO: 'verdadero' | 'falso';


ID: [a-zA-Z_][a-zA-Z0-9_]*;


WS: [ \t\r\n]+ -> skip;
COMENTARIO: '//' ~[\r\n]* -> skip;
