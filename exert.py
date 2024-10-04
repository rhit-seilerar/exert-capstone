import argparse
import sys
import os
#-h --help - give help information
#-t --test - run test
#-o --osi - generate OSI information
#-d --docker - add docker setup
#exert osi *filename* -d *output dir*
#argparse
def main(args):
    parser = argparse.ArgumentParser(
            prog='EXERT')

    parser.add_argument('-d','--docker',action='store_true',help='Run this command in the Pandare docker container. Will initialize the container if it does not exist.')
    subparsers = parser.add_subparsers(title='subcommands',description='valid subcommands')
    osi_parser = subparsers.add_parser('osi',help='Generate OSI information for the given kernel image')
    osi_parser.add_argument('image',help='The kernel image to generate OSI information for.')
    osi_parser.set_defaults(func=osi)
    test_parser = subparsers.add_parser('test',help='Run the automated tests')
    test_parser.set_defaults(func=test)

    parsed = parser.parse_args(args)
    parsed.func(parsed)


#0x8000
#0x8800
#0x9000
#0x9800
def osi(parsed):
    

    try:
        fo =  open(parsed.image,'rb')
        cursor = 0x8000
        size = os.stat(parsed.image).st_size
        valid = cursor + 5 < size
        while cursor + 7 < size and valid:
            fo.seek(cursor)
            header_type = int.from_bytes(fo.read(1))
            header_identifier = fo.read(5).decode('ascii')
            header_version = int.from_bytes(fo.read(1))
            if header_identifier != 'CD001':
                valid = False
            if header_version != 1:
                valid = False
            if header_type == 255:
                break
            if header_type < 0 or header_type > 3:
                valid = False
            cursor += 0x800
        if not valid:
            print(f'The file {parsed.image} is not a valid kernel image.')
            return
    except FileNotFoundError:
        print(f'Could not find {parsed.image}.')
        return
    print('OSI not implemented.')


def test(parsed):
    print('Test not implemented.')


main(sys.argv[1:])
