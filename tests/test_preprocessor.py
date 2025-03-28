import exert.parser.definitions as dm
import exert.parser.tokenmanager as tm
from exert.parser.tokenizer import Tokenizer
from exert.parser.preprocessor import Preprocessor, read_file

FILES = {
    'base.h': """
        #ifndef _BASE_H
        #define _BASE_H
        #include "foo.h"
        
        #define SOME_MACRO_VALUE 1
        #define SOME_MACRO_FUNC(x, y) (a, b)
        #define SOME_MACRO_VARARGS(z, ...) (z, __VA_ARGS__)
        
        #if SOME_MACRO_VALUE != 1
        #error Hello!
        #elif SOME_MACRO_VALUE == 2
        #warning Warn: This is a test
        #else
        #pragma dummy
        #endif
        
        #ifndef SOME_MACRO_VALUE
        static int value2 = SOME_MACRO_VALUE(1, 2, 3);
        #endif
        
        static int value = SOME_MACRO_VALUE;
        
        #endif
    """,
    'foo.h': """
        #ifndef _FOO_H
        #define _FOO_H
        typedef int sint;
        #include "bar.h"
        #endif
    """,
    'bar.h': """
        #ifndef _BAR_H
        #define _BAR_H
        typedef unsigned int uint;
        #include "foo.h"
        #endif
    """
}

def dummy_reader(path):
    return FILES.get(path)

def test_read_file():
    assert read_file('exert.py')
    assert not read_file('__dummy_does_not_exist__.abc')

TK = Tokenizer()
CACHE = './cache/test-preprocessor'

def check(incls, defns, str_in, str_out):
    pp = Preprocessor(TK, 32, incls, defns, filereader = dummy_reader)
    pp.preprocess(str_in, CACHE, reset_cache = True)
    pp.load(CACHE)
    assert pp.tokens == TK.tokenize(str_out)

def test_standard():
    check([], {}, """
        typedef int dummy;
        int main(int argc, char **argv) {
            printf("Hello!\n");
            return 0;
        }
    """, """
        typedef int dummy;
        int main(int argc, char **argv) {
            printf("Hello!\n");
            return 0;
        }
    """)
    #TODO string concat

def test_defines():
    check([], {}, """
        #define ABC typedef int[3] vec3
        ABC;
        #undef ABC
        ABC;
    """, """
        typedef int[3] vec3;
        ABC;
    """)
    #TODO ident stringification
    #TODO ident concat

def test_blocks():
    pp = Preprocessor(TK, 32, [], {}, filereader = dummy_reader)
    pp.preprocess("""
        #ifndef ABC
        #define ABC 1
        #else
        #undef ABC
        #define ABC 2
        #endif
        ABC;
    """, CACHE, reset_cache = True)
    pp.load(CACHE)
    assert pp.tokens == [
        ('optional', TK.tokenize('(!defined ABC)')),
        ('optional', []),
        ('optional', TK.tokenize('!(!defined ABC) && (1)')),
        ('optional', []),
        ('any', 'ABC', {
            dm.DefOption([tm.mk_int(1)]),
            dm.DefOption([tm.mk_int(2)])
        }),
        tm.mk_op(';')
    ]

    # assert pp.preprocess("""
    #     #ifdef ABC
    #         #if ABC == 2
    #             #define DEF 1
    #         #elifdef DEF
    #             #warning DEF already defined
    #         #endif
    #     #elifndef DEF
    #         #error DEF not defined
    #     #elif DEF != 1
    #         #undef DEF
    #         #define DEF 1
    #     #endif
    # """, CACHE, True).load(CACHE).tokens == [
    #     ('optional', TK.tokenize('(defined ABC)')),
    #     ('optional', TK.tokenize('(ABC == 2)')),
    #     ('optional', []),
    #     ('optional', TK.tokenize('!(ABC == 2) && (defined DEF)')),
    #     ('optional', []),
    #     ('optional', []),
    #     ('optional', TK.tokenize('!(defined ABC) && (!defined DEF)')),
    #     ('optional', []),
    #     ('optional', TK.tokenize('!(defined ABC) && !(!defined DEF) && (DEF != 1)')),
    #     ('optional', []),
    # ]

def test_line_and_include():
    pass

def test_misc_directives():
    pass
