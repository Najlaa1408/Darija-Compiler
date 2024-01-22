import ply.lex as lex
import ply.yacc as yacc
tokens = (
    'ACTION',
    'ENTITY',
    'RELATION',
    'MODIFIER',
    'SPECIFIC',
    'GROUP',
    'IDENTIFIER',  # General identifier token
)

# Define the expressions for each token
def t_ACTION(t):
    r'الاب|الحر|دخول|اللي|الفياق|عند|سول|شوف|طلاب|لبس|مولى|الله|السلهام|نسا'
    t.value = t.value  # Set the token value to the matched string
    return t

def t_ENTITY(t):
    r'المجرب|الجار|بالغمزه|يطلب|قدك|القلب|ينجيك|والعمامة|الهم|يربي|الحمام|بغا|بكري|رخصو|تلف'
    t.value = t.value
    return t

def t_RELATION(t):
    r'لا|قبل|ومراته|والعبد|يواتيك|الصافي|والام|من|وقلة|ينساك|ماشي|الزين|بالذهب|تخلي|يشد'
    t.value = t.value
    return t

def t_MODIFIER(t):
    r'تسول|ديما|بالدبزه|المشتاق|الفهامة|تخبي|الدار|تصدق|الارض|نصو|بحال|يصبر|مشري'
    t.value = t.value
    return t

def t_SPECIFIC(t):
    r'الى|خروجو|طبيب|زهرو|للتقيب'
    t.value = t.value
    return t

def t_GROUP(t):
    r'الوذنين|حافي|داق'
    t.value = t.value
    return t

# General identifier token
def t_IDENTIFIER(t):
    r'[^\s]+'
    t.value = t.value
    return t

# Ignore spaces
t_ignore = ' '

# Error handling for lexer
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

# Define the start symbol
start = 'sentence'

# Define the grammar rules
# Define the grammar rules
def p_sentence(p):
    '''
    sentence : ACTION ENTITY RELATION MODIFIER SPECIFIC GROUP
             | ACTION ENTITY RELATION MODIFIER SPECIFIC
             | ACTION ENTITY RELATION MODIFIER
             | ACTION ENTITY RELATION
             | ACTION ENTITY
             | ACTION
    '''
    #print("Parsed Sentence")
def p_error(p):
    print(f"Syntax error near '{p.value}'")

parser = yacc.yacc()