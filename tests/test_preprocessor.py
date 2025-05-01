from collections.abc import Callable
from exert.parser.defoption import DefOption
import exert.parser.tokenmanager as tm
from exert.parser.tokenizer import Tokenizer
from exert.parser.preprocessor import Preprocessor, read_file

FILES: dict[str, str] = {
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

def dummy_reader(path: str) -> (str | None):
    return FILES.get(path)

def test_read_file() -> None:
    assert read_file('exert.py')
    assert not read_file('__dummy_does_not_exist__.abc')

TK = Tokenizer()
CACHE = './cache/test-preprocessor'

def check(incls: list[str | Callable[[str], (str | None)]], defns: dict[str, str], str_in: str, str_out: str) -> None:
    pp = Preprocessor(TK, 32, incls, defns, filereader = dummy_reader)
    pp.preprocess(str_in, CACHE, reset_cache = True)
    pp.load(CACHE)
    assert pp.tokens == TK.tokenize(str_out)

def test_string_concat() -> None:
    check([], {}, '"Hello " "there!\n"', '"Hello there!\n"')
    check([], {}, 'L"Hello " "there!\n"', 'L"Hello there!\n"')
    check([], {}, '"Hello " u"there!\n"', 'u"Hello there!\n"')
    try:
        check([], {}, 'L"Hello " u"there!\n"', 'u"Hello there!\n"')
        raise ValueError
    except AssertionError:
        pass

def test_standard() -> None:
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

def test_defines() -> None:
    check([], {}, """
        #define ABC typedef int[3] vec3
        ABC;
        #undef ABC
        ABC;
    """, """
        typedef int[3] vec3;
        ABC;
    """)

def test_blocks() -> None:
    pp = Preprocessor(TK, 32, [], {}, filereader = dummy_reader)
    pp.preprocess("""
        #ifndef ABC
        #define ABC 1
        int A = ABC;
        #else
        #undef ABC
        #define ABC 2
        int A = ABC;
        #endif
        int B = ABC;
    """, CACHE, True).load(CACHE)
    assert pp.tokens == [
        ('any', '', {
            DefOption(TK.tokenize('int A = 1;')),
            DefOption(TK.tokenize('int A = 2;'))
        }),
        tm.mk_kw('int'),
        tm.mk_id('B'),
        tm.mk_op('='),
        ('any', 'ABC', {
            DefOption([tm.mk_int(1)]),
            DefOption([tm.mk_int(2)])
        }),
        tm.mk_op(';')
    ]

    pp = Preprocessor(TK, 32, [], {}, filereader = dummy_reader)
    pp.preprocess("""
        #ifdef ABC
        int A;
        #elifndef DEF
        int B;
        #endif
    """, CACHE, True).load(CACHE)
    assert pp.tokens == [
        ('any', '', {
            DefOption(TK.tokenize('int A;')),
            DefOption(TK.tokenize('int B;')),
            DefOption([])
        }),
    ]

    pp = Preprocessor(TK, 32, [], {}, filereader = dummy_reader)
    pp.preprocess("""
        #ifdef ABC
            #if ABC == 2
                #define DEF 1
                int A = 2; // ABC; // TODO: Guarantee extraction from wildcards
            #elifdef DEF
                #warning DEF already defined
                #undef ABC
                #define ABC 2
                int A = ABC;
            #endif
            int B = 3;
        #elifndef DEF
            int B = 4;
            #error DEF not defined
        #elif DEF != 1
            #undef DEF
            #define DEF 1
            int B = DEF;
        #else
            int B = 7;
        #endif
        int C = 6;
    """, CACHE, True).load(CACHE)
    assert len(pp.tokens[0]) > 2
    print([str(p) for p in pp.tokens[0][2]])
    assert pp.tokens == [
        ('any', '', {
            DefOption([
                ('any', '', {
                    DefOption(TK.tokenize('int A = 2;')),
                    DefOption([])
                }),
                *TK.tokenize('int B = 3;')
            ]),
            DefOption(TK.tokenize('int B = 1;')),
            DefOption(TK.tokenize('int B = 7;'))
        }),
        *TK.tokenize('int C = 6;')
    ]

def test_line_and_include() -> None:
    pass

def test_misc_directives() -> None:
    pass
