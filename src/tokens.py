from lexer import Token

# Token types used by the Banana lexer:
#
# Keywords:
# LET PRINT IF ELSE WHILE FUNC RETURN TRUE FALSE
#
# Identifiers and literals:
# ID NUMBER
#
# Arithmetic:
# PLUS MINUS STAR SLASH
#
# Comparison:
# EQ NE LT GT LE GE
#
# Assignment:
# ASSIGN PLUS_ASSIGN MINUS_ASSIGN STAR_ASSIGN SLASH_ASSIGN
#
# Delimiters:
# LPAREN RPAREN LBRACE RBRACE COMMA SEMICOLON
#
# End of input:
# EOF
#
# The Token dataclass is defined in lexer.py and stores:
# type, lexeme, line, and column.
