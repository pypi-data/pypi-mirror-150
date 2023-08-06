import argparse
from colorama import Fore,init
from seqits import seqits_retest_version
import re,os
init(autoreset=True)
def get_help(prog):
    return argparse.HelpFormatter('seqits.formatseq')
def get_version():
    return 'Seqits: retest {}'.format(seqits_retest_version)
parser = argparse.ArgumentParser(formatter_class=get_help,description="Seqits: fasta file format")
parser.add_argument('input',
                    help='input file')
parser.add_argument('re',
                    help='regulate expression')
parser.add_argument('-v', '--version', action='version',
                   version=get_version(),help='display version')
args = parser.parse_args()
filename=args.input
if os.path.isfile(filename):
    with open(filename) as f:
        file=f.read()
else:
    print(Fore.RED+'Cannot find the input file!')
    exit(0)
result_list=re.findall(args.re,file)
result_list=list(set(result_list))
result_list.sort()
if len(result_list)==0:
    print(Fore.RED+'No result!')
print(Fore.GREEN+'result:')
print(result_list)
