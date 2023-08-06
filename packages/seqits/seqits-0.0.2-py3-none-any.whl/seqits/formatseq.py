import argparse
from colorama import Fore,init
from seqits import seqits_formatseq_version
import os
init(autoreset=True)
def get_help(prog):
    return argparse.HelpFormatter('seqits.formatseq')
def get_version():
    return 'Seqits: formatseq {}'.format(seqits_formatseq_version)
parser = argparse.ArgumentParser(formatter_class=get_help,description="Seqits: fasta file format")
parser.add_argument('input',
                    help='input raw fasta file')
parser.add_argument('-n','--num',
                    type=int,
                    default=60,
                    help='number of characters per line')
parser.add_argument('-o','--out',
                    default='output.fa',
                    help='output file')
parser.add_argument('-s','--show',
                    default='false',
                    help='true/false, show the output on the screen')
parser.add_argument('-v', '--version', action='version',
                   version=get_version(),help='display version')

args = parser.parse_args()
filename=args.input
print('Waiting for formatting ...')
if os.path.isfile(filename):
    with open(filename) as f:
        file=f.read()
else:
    print(Fore.RED+'Cannot find the input file!')
    exit(0)
remove_list=['\r','\t',' ','\n','\b']
s=''
for i in file.split('>')[1:]:
    temp=i.split('\n')
    n=0
    s+='>'+temp[0]+'\n'
    for j in ''.join(temp[1:]):
        if j not in remove_list:
            s+=j.upper()
            n+=1
            if n%args.num==0:
                s+='\n'
    if n%args.num!=0:
        s+='\n'
if args.show=='true':
    print(s)
elif args.show!='false':
    print(Fore.RED+'show mode error!')
    exit(0)
if args.out:
    with open(args.out,'w') as f:
        f.write(s)
    print(Fore.GREEN+'saved to "'+args.out +'" successfully.')
