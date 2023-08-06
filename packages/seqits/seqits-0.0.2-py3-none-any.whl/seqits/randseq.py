import random
import argparse
from colorama import Fore,init
from seqits import seqits_randseq_version

init(autoreset=True)
def get_help(prog):
    return argparse.HelpFormatter('seqits.randseq')
def get_version():
    return 'Seqits: randseq {}'.format(seqits_randseq_version)
parser = argparse.ArgumentParser(formatter_class=get_help,description="Seqits: generate sequences randomly")
parser.add_argument('type',
                    help='nucl/prot, cds or protein sequence(s)')
parser.add_argument('num',
                    type=int,
                    help='number of sequences(s) to generate')
parser.add_argument('-o','--out',
                    default='output.fa',
                    help='output file')
parser.add_argument('-s','--show',
                    default='false',
                    help='true/false, show the output on the screen')
parser.add_argument('-v', '--version', action='version',
                   version=get_version(),help='display version')
args = parser.parse_args()
s=''
if args.type=='nucl':
    print('Generate cDNA sequence(s) randomly ... ')
    condon=["AAA","AAT","AAC","AAG","ATA","ATT","ATC","ACA","ACT","ACC","ACG","AGA","AGT","AGC","AGG","TAT","TAC","TTA","TTT","TTC","TTG","TCA","TCT","TCC","TCG","TGT","TGC","TGG","CAA","CAT","CAC","CAG","CTA","CTT","CTC","CTG","CCA","CCT","CCC","CCG","CGA","CGT","CGC","CGG","GAA","GAT","GAC","GAG","GTA","GTT","GTC","GTG","GCA","GCT","GCC","GCG","GGA","GGT","GGC","GGG"]
    final_codon=['TAA','TAG','TGA']
    seq=''
    for i in range(args.num):
        q='ATG'
        q+=''.join([random.choice(condon) for i in range(random.randrange(100,800))])
        q+=random.choice(final_codon)
        n=0
        seq+='>Untitled'+str(i+1)+'\n'
        for j in q:
            seq+=j
            n+=1
            if n%60==0:
                seq+='\n'
        if n%60!=0:
            seq+='\n'
elif args.type=='prot':
    print('Generate protein sequence(s) randomly ... ')
    aa='ARNDCQEGHILKMFPSTWYV'
    seq=''
    for i in range(args.num):
        q='M'
        q+=''.join([random.choice(aa) for i in range(random.randrange(100,800))])
        n=0
        seq+='>Untitled'+str(i+1)+'\n'
        for j in q:
            seq+=j
            n+=1
            if n%60==0:
                seq+='\n'
        if n%60!=0:
            seq+='\n'
else:
    print(Fore.RED+'sequence(s) type error!')
    exit(0)
if args.show=='true':
    print(seq)
elif args.show!='false':
    print(Fore.RED+'show mode error!')
    exit(0)
if args.out:
    with open(args.out,'w') as f:
        f.write(seq)
    print(Fore.GREEN + 'saved to "'+args.out +'" successfully!')
