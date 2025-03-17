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

def test_preprocessor():
    tokenizer = Tokenizer()
    preprocessor = Preprocessor(tokenizer, [], {}, filereader = dummy_reader)
    preprocessor.preprocess('#include "base.h"', './cache/test-preprocessor')
    print(str(preprocessor))
