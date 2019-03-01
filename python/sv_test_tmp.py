"""
Created on Fri Apr 13 12:01:56 2018

@author: jgs
"""

import os
import click


class sv_tools:
    '''
    sv analysis for target sequence
    '''
    def __init__(self, bam, srs, name, sv):
        self.sr_extact = srs
        self.name = name
        self.bam = bam
        self.sv = sv
       
    def extract_reads(self, out_dir): 
        '''
        generate bams of discordinate and split reads respectively
        '''
        out_dir = out_dir +  '/' if not out_dir.endswith('/') else out_dir
        mapping = {'b':self.bam, 'n':self.name, 'o':out_dir, 'sr':self.sr_extact}
        os.system('samtools view -b -F 1294 {b} > {o}{n}.discordants.unsorted.bam &&\
                  samtools sort -o {o}{n}.discordants.bam {o}{n}.discordants.unsorted.bam'\
                  .format(**mapping))
        os.system('samtools view -h {b} \
                  | {sr} -n 1000 -m 0 -i stdin \
                  | samtools view -Sb - \
                  > {o}{n}.splitters.unsorted.bam &&\
                  samtools sort -o {o}{n}.splitters.bam {o}{n}.splitters.unsorted.bam'\
                  .format(**mapping))
 
    def svaba(self, out_dir, ref, bed=None):
        out_dir = out_dir +  '/' if not out_dir.endswith('/') else out_dir
        mapping = {'b':self.bam, 'n':self.name, 'o':out_dir, 'r':ref, 'bed':bed, 'svaba':self.sv}
        if bed:
            os.system('cd {o} ; {svaba} run -t {b} -k {bed} -a {n}.filter -G {r}'\
                      .format(**mapping))
        else:
            os.system('cd {o} ; {svaba} run -t {b} -a {n}.no_filter -G {r}'\
                      .format(**mapping))
            
@click.command()
@click.option('--inbam', '-i', help='input bam')
@click.option('--outpath','-o', default='./', help='dir for outputs')
@click.option('--bedfile','-b', help='bed file of filter region')
@click.option('--refernece','-r', help='reference genome')
@click.option('--name', '-n', help='prefix of output file')
@click.option('--split', '-s', help='path of split reads extract script')
@click.option('--sv', '-v', help='path of svaba programe')
def sv_analysis(inbam, outpath, bedfile, refernece, name, split, sv):
    bam = sv_tools(inbam, split, name, sv)
#    bam.extract_reads(outpath)
    bam.svaba(outpath, refernece, bedfile)

    
if __name__ == '__main__':
    sv_analysis()

