import argparse
from colorama import Fore,init
from seqits import seqits_search_version
import re,os
init(autoreset=True)
def get_help(prog):
    return argparse.HelpFormatter('seqits.search')
def get_version():
    return 'Seqits: search {}'.format(seqits_search_version)
parser = argparse.ArgumentParser(formatter_class=get_help,description="Seqits: gene search tool")
parser.add_argument('input',
                    help='input raw fasta file')
parser.add_argument('gene',
                    help='input gene(s)')
parser.add_argument('-t','--type',
                    default='string',
                    help='re/string/file, type of input gene(s). re means regulate expression, for file, one gene one line; for string, gene(s) should be seperated with \',\' ')
parser.add_argument('-m','--mode',
                    default='fast',
                    help='fast/order, "fast" mode may faster than "order" mode, but "order" mode can show your output accoring to the order of input gene(s)')
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
gene_list=args.gene
gene_type=args.type
if os.path.isfile(filename):
    with open(filename) as f:
        file=f.read()
else:
    print(Fore.RED+'Cannot find the input file!')
    exit(0)
if gene_type=='string':
    gene_list=args.gene.split(',')
elif gene_type=='file':
    with open(args.gene) as f:
        gene_list=f.read()
    gene_list=gene_list.split('\n')
elif gene_type=='regulate':
    gene_list=re.findall(args.gene,file)
    gene_list=list(set(gene_list))
    gene_list.sort()
else:
    print(Fore.RED+'type of input gene(s) error!')
    exit(0)
if len(gene_list)==0:
    print(Fore.RED+'No gene!')
    exit(0)
if '' in gene_list:
    gene_list.remove('')
s=''
if args.mode=='fast':
    for i in file.split('>')[1:]:
        temp=i.split('\n')
        if temp[0].split(' ')[0] in gene_list:
            s+='>'+temp[0]+'\n'+'\n'.join(temp[1:])
elif args.mode=='order':
    for i in gene_list:
        for j in file.split('>')[1:]:
            temp=j.split('\n')
            if temp[0].split(' ')[0]==i:
                s+='>'+temp[0]+'\n'+'\n'.join(temp[1:])
                break
else:
    print(Fore.RED+'search mode error!')
    exit(0)
if args.show=='true':
    print(s)
elif args.show!='false':
    print(Fore.RED+'show mode error!')
    exit(0)
if args.out:
    with open(args.out,'w') as f:
        f.write(s)
    print(Fore.GREEN+'saved to "'+args.out +'" successfully.')
