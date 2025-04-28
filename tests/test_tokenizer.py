import exert.parser.tokenmanager as tm
from exert.parser.tokenizer import Tokenizer

TK = Tokenizer()

def roundtrip(string: str, out: (str | None) = None) -> None:
    assert tm.tok_seq(TK.tokenize(string)) == (string if out is None else out)

def test():
    roundtrip('0')
    roundtrip('<:', '[')
    roundtrip('%:%:', '##')
    roundtrip('0x7F', '127')
    roundtrip('0b110', '6')
    roundtrip('017', '15')
    roundtrip('1')
    roundtrip('typedef long int a ;')
    roundtrip('void /* ooh, comment */ foo ( int a ) ;', 'void foo ( int a ) ;')
    roundtrip('#include <abc>')
    roundtrip('#include <abc> // Lookie here', '#include <abc>')
    roundtrip('1ds', 'ds')
    roundtrip('ABC == 2')
    roundtrip("""
        #ifndef ABC
        #define ABC(_1, _2, ...) __VA_ARGS__
        typedef int[3] vec3;
        #endif
    """, "#ifndef ABC  #define ABC (_1 , _2 , ... ) __VA_ARGS__  typedef int [ 3 ] vec3 ; #endif")
    roundtrip("""
    // This is a multi-line \\
    // single-line comment
    """, '')
    roundtrip("""
    #define MULTILINE_DEFN \\
        DEFN1 \\
        DEFN2
    """, '#define MULTILINE_DEFN DEFN1 DEFN2')
    assert TK.tokenize('%:define') == [('directive', '#'), tm.mk_id('define'), ('newline', '')]
    assert TK.tokenize('#define A(B)') == [('directive', '#'), tm.mk_id('define'),
        tm.mk_id('A'), ('directive', '('), tm.mk_id('B'), tm.mk_op(')'), ('newline', '')]

    roundtrip("""
        #if ABC == 2
            #define DEF 1
            int A = 2; // ABC; // TODO: Guarantee
        #elifdef DEF
            int A = 2;
        #endif
    """, '#if ABC == 2  #define DEF 1  int A = 2 ; #elifdef DEF  int A = 2 ; #endif')
