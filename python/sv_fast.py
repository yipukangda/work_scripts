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
    def __init__(self, bam, srs, name, svaba):
        self.sr_extact = srs
        self.name = name
        self.bam = bam
        self.sv = svaba

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
                  samtools sort -o {o}{n}.splitters.bam  {o}{n}.splitters.unsorted.bam'\
                  .format(**mapping))
        os.system('rm {o}{n}.splitters.unsorted.bam {o}{n}.discordants.unsorted.bam && \
                   picard MergeSamFiles I={o}{n}.discordants.bam I={o}{n}.splitters.bam O={o}{n}.sv.bam && \
                   rm {o}{n}.splitters.bam {o}{n}.discordants.bam && samtools index {o}{n}.sv.bam'\
                   .format(**mapping))

    def svaba(self, out_dir, ref, t, bed=''):
        out_dir = out_dir +  '/' if not out_dir.endswith('/') else out_dir
        mapping = {'b':self.bam, 'n':self.name, 'o':out_dir, 'sr':self.sr_extact, 'r':ref, 'bed':bed, 'svaba':self.sv, 'threads':t}
        if not bed:
            os.system('cd {o} ; {svaba} run -t {o}{n}.sv.bam -a {n}.no_filter -G {r} -p {threads}'.format(**mapping))
        else:
            os.system('cd {o} ; {svaba} run -t {o}{n}.sv.bam -k {bed} -a {n}.filter -G {r} -p {threads}'.format(**mapping))


@click.command()
@click.option('--inbam', '-i', help='input bam')
@click.option('--outpath','-o', default='./', help='dir for outputs')
@click.option('--bedfile','-b', help='bed file of filter region')
@click.option('--refernece','-r', help='reference genome', default='~/database/gatk_bundle/b37/human_g1k_v37.fasta')
@click.option('--name', '-n', help='prefix of output file')
@click.option('--split', '-s', help='path of split reads extract script', default='~/softerwares/lumpy-sv/scripts/extractSplitReads_BwaMem')
@click.option('--svaba', '-v', help='path of svaba programe', default='~/softerwares/svaba/bin/svaba')
@click.option('--threads', '-p', help='number of threads, default is 1', default='1')
def sv_analysis(inbam, outpath, bedfile, refernece, name, split, svaba, threads):
    bam = sv_tools(inbam, split, name, svaba)
    bam.extract_reads(outpath)
    try:
      bam.svaba(outpath, refernece, threads, bedfile)
    except:
      bam.svaba(outpath, refernece, threads)

if __name__ == '__main__':
    sv_analysis()
