import argparse
import os
from colorama import Fore,init
from seqits import seqits_version,package_list
init(autoreset=True)

package_list()
def get_version():
    return 'Seqits {}'.format(seqits_version)
def get_list():
    start_info='Seqits version {} author: Fujun Sun\n'.format(seqits_version)
    info=start_info+'package: version\n'
    info+=package_list()
    return info

def get_help(prog):
    return argparse.HelpFormatter('seqits')
parse = argparse.ArgumentParser(formatter_class=get_help,description=get_version()+'\tAuthor: Fujun Sun')
parse.add_argument('-v', '--version', action='version', version=get_version(),help='display version')
parse.add_argument('list',  default='',help='show all tools in seqits')
args = parse.parse_args()

if args.list=='list':
    print(get_list())
else:
    print(Fore.RED+'command error!')
    exit(0)
