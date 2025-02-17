from exert.utilities.tokenizer import Tokenizer
from exert.utilities.preprocessor import Preprocessor

FILES = {
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

def test_preprocessor():
    tokenizer = Tokenizer()
    preprocessor = Preprocessor(tokenizer, [], dummy_reader)
    preprocessor.preprocess('#include "foo.h"')
    print(str(preprocessor))
    assert False
