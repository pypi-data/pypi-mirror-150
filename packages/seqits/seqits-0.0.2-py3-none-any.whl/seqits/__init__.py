seqits_version='0.0.2'
seqits_search_version='0.0.2'
seqits_randseq_version='0.0.1'
seqits_formatseq_version='0.0.1'
seqits_retest_version='0.0.1'
def package_list():
    s=''
    for i in globals().items():
        if 'seqits_' in i[0] and i[0]!='seqits_version' and '_version' in i[0]:
            s+=i[0].replace('seqits_','').replace('_version','')+': '+i[1]+'\n'
    return s
