// Code inpired from ToTemBioNet


grammar IG;

prog        :   var_block
                reg_block
                hybrid_hoare_block
                KCYCLIC?
                'END'
            ;

/* Interaction graph description : variables and  regulations (multiplexes) */

var_block       :   KVAR var_decl+
                ;
var_decl        :   ID EQ NUM '..' NUM SEMI
                ;

reg_block       :   KREG reg_decl+
                ;
reg_decl        :   ID '['reg_expr']' CIBLE ID+ SEMI
                ;
reg_expr        :   NEG reg_expr                                #expr_neg
                |   reg_expr BOOL_OP reg_expr                   #expr_bool_op
                |   '('reg_expr')'                              #expr_brackets
                |   ID SEUIL NUM                                #expr_atome
                |   ID                                          #expr_mux_name
                ;

/* Hybrid Hoare triple description : pre and post condition + trace */

hybrid_hoare_block      :   KHYBRIDHOARE hybrid_hoare_decl
                ;

hybrid_hoare_decl       :   hybrid_hoare_pre_decl
                            hybrid_hoare_trace_decl
                            hybrid_hoare_post_decl
                        ;

hybrid_hoare_pre_decl   :   KPRE ':' '{' '}'
                        ;

hybrid_hoare_post_decl  :   KPOST ':' '{' (discrete_condition (',')? )+ ';' (hybrid_condition (',')? )+ '}'
                        ;
discrete_condition      :   'eta' '(' ID ')' EQ NUM
                        |   NOKB
                        ;
hybrid_condition        :   'pi' '(' ID ')' EQ FLOAT
                        |   NOKB
                        ;

hybrid_hoare_trace_decl :   KTRACE ':' ( hybrid_hoare_trace SEMI )+
                        ;
hybrid_hoare_trace      :   '(' FLOAT ',' ( hybrid_hoare_slide (AND)? )+ ',' hybrid_hoare_dpa ')'
/*|OR */
                        ;
hybrid_hoare_dpa        :   ID OPER
                        |   NOKB
                        ;
hybrid_hoare_slide      :   SLIDE (OPER)? '(' ID ')'
                        |   NOSLIDE (OPER)? '(' ID ')'
                        |   NOKB
                        ;

/* ADD GRAMMAR RULE HERE */


/* Lexical Analysis - Lexer rules */

KVAR            :   'VAR';
KREG            :   'REG';
KHYBRIDHOARE    :   'HYBRID HOARE';
KPRE            :   'PRE';
KTRACE          :   'TRACE';
KPOST           :   'POST';
KCYCLIC         :   'CYCLIC';

NOKB            :   'True';
AND             :   'and';
/* OR              :   'or'; */

SLIDE           :   'slide';
NOSLIDE         :   'noslide';

ID              :   [a-zA-Z][a-zA-Z0-9_]*;
NUM             :   [0-9];
FLOAT           :   [+-]?[0-9]+.[0-9]+;

EQ              :   '=';
SEMI            :   ';';
NEG             :   '!';
BOOL_OP         :   ('&'|'|');
SEUIL           :   '>=';
CIBLE           :   '=>';
OPER            :   ('+'|'-');

WS              :   [ \r\n\t]+      -> skip;
COMMENT         :   '#' ~('\n')*    -> skip;
