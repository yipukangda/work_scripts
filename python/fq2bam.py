"""
Created on Sat Nov 25 10:52:03 2017

@author: jgs
"""
import os
import re
import click

#function for generate bam contain marked reads
def cyp_p_des(sample, file_path, out_path, reference):
    
    if not file_path.endswith('/'):
        file_path = file_path + r'/'
    if not out_path.endswith('/'):
        out_path = out_path + r'/'
    if not os.path.isdir(out_path):
        os.makedirs(out_path)
    mapping = {'n':sample, 'f':file_path, 'o':out_path, 'r':reference}
    #trim and OC
    os.system('trim_galore --illumina --trim-n --paired -o {o} \
              {f}{n}*.gz'\
              .format(**mapping))
    #Generate a SAM file containing aligned reads
    os.system('ls {f}{n}* && bwa mem -M -t 15 -K 10000000 \
              -R "@RG\\tID:{n}\\tSM:{n}\\tLB:lib1\\tPL:illumina" \
              {r} {o}{n}*gz \
              1> {o}{n}.sam'\
              .format(**mapping))
    #Run the following Picard command to sort the SAM file and convert it to BAM:
    os.system('picard SortSam \
              INPUT={o}{n}.sam \
              OUTPUT={o}{n}.sorted.bam \
              SORT_ORDER=coordinate'\
              .format(**mapping))
    os.system('rm {o}{n}.sam'.format(**mapping))
    #Run the following Picard command to mark duplicates:
    os.system('picard MarkDuplicates  \
              INPUT={o}{n}.sorted.bam \
              OUTPUT={o}{n}.sorted.markdup.bam \
              METRICS_FILE={o}{n}_metrics.txt \
              && samtools index {o}{n}.sorted.markdup.bam'\
              .format(**mapping))
    os.system('rm {o}{n}.sorted.bam'.format(**mapping))
    #Run the following Picard command to index the BAM file:
    os.system('picard BuildBamIndex \
              INPUT={o}{n}.sorted.markdup.bam && \
              samtools index {o}{n}.sorted.markdup.bam'\
              .format(**mapping))
    
    


@click.command()
@click.option('--filelist','-l', help='a list of input sample names')
@click.option('--inpath','-i', default='./')
@click.option('--outpath','-o', default='./results')
@click.option('--refernece','-r', default='/home/jgs/database/gatk_bundle/b37/human_g1k_v37.fasta', help='reference genome fasta, default is human b37')
@click.option('--name', '-n', help='sample name for a single sample')
def analysis_cyp_gene(filelist, inpath, outpath, refernece, name):
    if filelist:
        f = open(filelist,'r')
        l = f.read().strip().split('\n')
        for i in l:
            cyp_p_des(i, inpath, outpath, refernece)
        f.close()
    else:
        cyp_p_des(name, inpath, outpath, refernece)


if __name__ == '__main__':
    analysis_cyp_gene()

