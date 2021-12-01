# parsetree

Lexical Parser and Syntactical Parser.

# Grammars used

-   program --> VOID MAIN "(" ")" <block>
-   block --> "{" {<statement>} "}" “;”
-   assign --> id = < term>
-   term --> <factor> { ( + | - | * | / | %) <factor> }
-   factor --> identifier | int | float 
-   returnstmt --> return <factor>
-   statement --> <ifstmt>  <assign> |<return>; |<forstmt>| <foreachstmt>| <dowhilestmt>| <whilestmt> | <switchstmt>
-   forstmt --> for "(" <ID>”;” <boolstmt> “;”  <assign> ")" <block>
-   ifstmt --> if (<boolstmt>) <block> else <block>
-   foreachstmt --> foreach "(" <id>  <id>")" <block>
-   dowhilestmt --> do <block> while "(" <boolstmt> ")"
-   whilestmt --> while "(" <boolstmt> ")" <block>
-   switchstmt --> switch "(" <id>")"  "{"  {<case_stmt>}  "}" 
-   casestmt --> case <factor>  “:” <block>
-   boolstmt --> <factor> (>|<) <factor>
