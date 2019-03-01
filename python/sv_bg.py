"""
Created on Wed Dec 20 10:49:35 2017

@author: jgs
"""

import os 
import click

def pipeline(sample:str, file_path, out_path, bed_file, ly:bool):
    if not file_path.endswith('/'):
        file_path = file_path + r'/'
    if not out_path.endswith('/'):
        out_path = out_path + r'/'
    mapping = {'n':sample, 'f':file_path, 'b':bed_file, 'o':out_path}
    # Run bwa and samblast to generate sam, disc sam and split sam
    os.system('/home/jgs/softerwares/bwa/bwa mem -M -t 4 \
              -R "@RG\\tID:{n}\\tSM:sv_test\\tLB:lib1\\tPL:illumina" \
              /home/jgs/database/gatk_bundle/b37/human_g1k_v37.fasta {f}{n}* | \
              /home/jgs/softerwares/samblaster/samblaster -M \
              -e --maxSplitCount 30 \
              --maxUnmappedBases 75 \
              --minIndelSize 25 --minNonOverlap 5 \
              -d {o}{n}.disc.sam -s {o}{n}.split.sam > {o}{n}.sam'\
              .format(**mapping))
    
    #Run the following Picard command to sort the SAM file and convert it to BAM:
    os.system('java -jar /home/jgs/softerwares/picard/build/libs/picard.jar SortSam \
              INPUT={o}{n}.sam \
              OUTPUT={o}{n}.sorted.bam \
              SORT_ORDER=coordinate'\
              .format(**mapping))
    os.system('rm %s%s.sam'%(out_path, sample))
    
    #Run the following Picard command to mark duplicates:
    os.system('java -jar /home/jgs/softerwares/picard/build/libs/picard.jar MarkDuplicates \
              INPUT={o}{n}.sorted.bam \
              OUTPUT={o}{n}.sorted.markdup.bam \
              METRICS_FILE={o}{n}_metrics.txt'\
              .format(**mapping))
    os.system('rm %s%s.sorted.bam'%(out_path, sample))
    #Run the following Picard command to index the BAM file:
    os.system('samtools index {o}{n}.sorted.markdup.bam'\
              .format(**mapping))
    
    #Sort and Index split and disc file:
    os.system('samtools view -h -b {o}{n}.split.sam > {o}{n}.split.unsorted.bam && \
              samtools sort -o {o}{n}.split.bam {o}{n}.split.unsorted.bam && \
              samtools index {o}{n}.split.bam && \
              rm {o}{n}.split.unsorted.bam {o}{n}.split.sam && \
              samtools view -h -b {o}{n}.disc.sam > {o}{n}.disc.unsorted.bam && \
              samtools sort -o {o}{n}.disc.bam {o}{n}.disc.unsorted.bam && \
              samtools index {o}{n}.disc.bam && \
              rm {o}{n}.disc.unsorted.bam {o}{n}.disc.sam'\
              .format(**mapping))
    
    #Run bedtools for counting split & disc reads, MQ>20
    os.system('bedtools multicov -bams {o}{n}.split.bam {o}{n}.disc.bam {o}{n}.sorted.markdup.bam -bed {b} -q 20 > {o}{n}.combat.bedcov.bed && \
              bedtools multicov -bams {o}{n}.split.bam -bed {b} -q 20 > {o}{n}.split.bedcov.bed && \
              bedtools multicov -bams {o}{n}.disc.bam -bed {b} -q 20 > {o}{n}.disc.bedcov.bed && \
              bedtools multicov -bams {o}{n}.sorted.markdup.bam -bed {b} -q 20 > {o}{n}.bedcov.bed'\
              .format(**mapping))
    
    #Run lumpy express if lumpy is true
    if ly:
        os.system('~/softerwares/lumpy-sv/bin/lumpyexpress \
                  -B {o}{n}.sorted.markdup.bam \
                  -S {o}{n}.split.bam \
                  -D {o}{n}.disc.bam \
                  -o {o}{n}.lumpy.vcf \
                  -m 10'\
                  .format(**mapping))

    
@click.command()
@click.option('--filelist','-l')
@click.option('--inpath','-i')
@click.option('--outpath','-o')
@click.option('--bedfile','-b')
@click.option('--lumpy/--nolumpy','-s/-n', default=True)
def breakpoint_analysis(filelist, inpath, outpath, bedfile, lumpy):
    os.system('mkdir -p %s'%(outpath))
    with open(filelist, 'r+') as fl:
        for f in fl.readlines():
            f = f.strip()
            pipeline(f, inpath, outpath, bedfile, lumpy)
            
if __name__ == '__main__':
    breakpoint_analysis()
            

