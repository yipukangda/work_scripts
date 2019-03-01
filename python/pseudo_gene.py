"""
Created on Mon Apr  2 09:45:38 2018

@author: jgs
"""

import os
import re
import click
import pandas as pd

def cyp_p_des(sample, out_path, reference, marker_bed, bam, picard):
    
    if not out_path.endswith('/'):
        out_path = out_path + r'/'
    mapping = {'n':sample, 'o':out_path, 'r':reference, 'm':marker_bed, 'b':bam, 'p':picard}
    os.system('samtools mpileup -f {r} \
              --positions {m} -q 5 --output-QNAME \
              {b} \
              -o {o}{n}_pileup.cyp.txt'\
              .format(**mapping))
    
    with open('{o}{n}_pileup.cyp.txt'.format(**mapping)) as p:
        dfm = pd.DataFrame({'read_id':[]})
        idx = 1
        f = open('{o}{n}_read_id.list'.format(**mapping),'w')
        l = p.read().strip().split('\n')
        for i in l:       
            i = i.split('\t')
            m = i[4]
            ri = i[6].split(',')
            m1 = re.sub('(\^[\w\W]{1})|\$','', m)
            m = re.sub('(\^[\w\W]{1})|\$','', m, flags=re.UNICODE)
            m = re.sub('-[0-9]+[ACGTNacgtn]+','', m)
            m = re.sub('\+[0-9]+[ACGTNacgtn]+','', m)
            for r in re.finditer('(\.|,)',m):
                f.write(ri[r.start()] + '\n')
                rl = []
                rl.append(ri[r.start()])
            mk = [1] * len(rl)
            dft = pd.DataFrame({'read_id':rl, 'marder_%s'%(idx):mk})
            dfm = dfm.merge(dft, on='read_id', how='outer')
            idx += 1
        f.close()
    dfm.to_csv('{o}{n}_reads_stats.xls'.format(**mapping), sep='\t', index=False)    
    os.system('java -jar {p} FilterSamReads \
              I={b} \
              O={o}{n}_extract_bam.bam \
              READ_LIST_FILE={o}{n}_read_id.list FILTER=includeReadList'\
              .format(**mapping))
    os.system('java -jar {p} BuildBamIndex \
              INPUT={o}{n}_extract_bam.bam && \
              samtools index {o}{n}_extract_bam.bam'\
              .format(**mapping))
    os.system('bedtools multicov -bams {o}{n}_extract_bam.bam {b} \
              -bed {m} > {o}{n}.bedcov.bed && \
              sed -i \'1i chr\tstart\tstop\textract\traw\' {o}{n}.bedcov.bed'\
              .format(**mapping))
    
@click.command()
@click.option('--inbam', '-i', help='input bam')
@click.option('--outpath','-o', default='./', help='dir for outputs')
@click.option('--bedfile','-b', help='bed file of diff markers of real/pseudo genes')
@click.option('--refernece','-r', help='use pseudogene masked reference')
@click.option('--name', '-n', help='prefix of output file')
@click.option('--picard', '-p', help='path of picard.jar')
def analysis_cyp_gene(inbam, outpath, refernece, bedfile, name, picard):
    cyp_p_des(name, outpath, refernece, bedfile, inbam, picard)

if __name__ == '__main__':
    analysis_cyp_gene()

