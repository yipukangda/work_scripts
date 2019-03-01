"""
Created on Sat Nov 25 10:52:03 2017

@author: jgs
"""
import os
import re
import click

#function for generate bam contain marked reads
def cyp_p_des(sample, file_path, out_path, reference, marker_bed):
#    #trim and OC
#    os.system('trim_galore --illumina --trim-n --paired -o /home/jgs/Downloads/cyp21a2/sec_bat/ \
#              /home/jgs/Downloads/cyp21a2/sec_bat/%s \
#              /home/jgs/Downloads/cyp21a2/sec_bat/%s'%(file1,file2))
#    file1 = file1.split('.')[0] + '_val_1.fq.gz'
#    file2 = file2.split('.')[0] + '_val_2.fq.gz'
    #Generate a SAM file containing aligned reads
    if not file_path.endswith('/'):
        file_path = file_path + r'/'
    if not out_path.endswith('/'):
        out_path = out_path + r'/'
    mapping = {'n':sample, 'f':file_path, 'o':out_path, 'r':reference, 'm':marker_bed}
    os.system('ls {f}{n}* && /home/jgs/softerwares/bwa/bwa mem -M -t 8  \
              -R "@RG\\tID:{n}\\tSM:sv_test\\tLB:lib1\\tPL:illumina" \
              {r} {f}{n}* \
              1> {o}{n}_cyp21a2p_excluded.sam'\
              .format(**mapping))
    #Run the following Picard command to sort the SAM file and convert it to BAM:
    os.system('java -jar /home/jgs/softerwares/picard/build/libs/picard.jar SortSam \
              INPUT={o}{n}_cyp21a2p_excluded.sam \
              OUTPUT={o}{n}_cyp21a2p_excluded.sorted.bam \
              SORT_ORDER=coordinate'\
              .format(**mapping))
    os.system('rm {o}{n}_cyp21a2p_excluded.sam'.format(**mapping))
    #Run the following Picard command to mark duplicates:
    os.system('java -jar /home/jgs/softerwares/picard/build/libs/picard.jar MarkDuplicates  \
              INPUT={o}{n}_cyp21a2p_excluded.sorted.bam \
              OUTPUT={o}{n}_cyp21a2p_excluded.sorted.markdup.bam \
              METRICS_FILE={o}{n}_metrics.txt'\
              .format(**mapping))
    os.system('rm {o}{n}_cyp21a2p_excluded.sorted.bam'.format(**mapping))
    #Run the following Picard command to index the BAM file:
    os.system('java -jar /home/jgs/softerwares/picard/build/libs/picard.jar BuildBamIndex \
              INPUT={o}{n}_cyp21a2p_excluded.sorted.markdup.bam && \
              samtools index {o}{n}_cyp21a2p_excluded.sorted.markdup.bam'\
              .format(**mapping))
    
    #Generate read id list file by marker bed file
    os.system('samtools mpileup -f /home/jgs/database/gatk_bundle/b37/human_g1k_v37.fasta \
              --positions {m} -q 5 --output-QNAME \
              {o}{n}_cyp21a2p_excluded.sorted.markdup.bam \
              -o {o}{n}_pileup.cyp.txt'\
              .format(**mapping))
    
    
    with open('{o}{n}_pileup.cyp.txt'.format(**mapping)) as p:
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
    #            print(ri[r.start()],'|',r.group())
                f.write(ri[r.start()] + '\n')
        f.close()
        
    os.system('java -jar /home/jgs/softerwares/picard/build/libs/picard.jar FilterSamReads \
              I={o}{n}_cyp21a2p_excluded.sorted.markdup.bam \
              O={o}{n}_extract_bam.bam \
              READ_LIST_FILE={o}{n}_read_id.list FILTER=includeReadList'\
              .format(**mapping))
    os.system('java -jar /home/jgs/softerwares/picard/build/libs/picard.jar BuildBamIndex \
              INPUT={o}{n}_extract_bam.bam && \
              samtools index {o}{n}_extract_bam.bam'\
              .format(**mapping))
    # Generate multicov bed file of raw bam and extracted bam
    os.system('bedtools multicov -bams {o}{n}_extract_bam.bam {o}{n}_cyp21a2p_excluded.sorted.markdup.bam \
              -bed {m} > {o}{n}.bedcov.bed && \
              sed -i \'1i chr\tstart\tstop\textract\traw\' {o}{n}.bedcov.bed'\
              .format(**mapping))
    


@click.command()
@click.option('--filelist','-l', help='a list of input sample names')
@click.option('--inpath','-i', default='./')
@click.option('--outpath','-o', default='./')
@click.option('--bedfile','-b',default='/home/jgs/database/cyp21a2_ref/cyp_marker.bed', help='bed file of diff markers of real/pseudo genes')
@click.option('--refernece','-r', default='/home/jgs/database/cyp21a2_ref/human_g1k_v37_cyp21a2_psudo_excluded.fasta', help='use pseudogene masked reference')
@click.option('--name', '-n', help='sample name for a single sample')
def analysis_cyp_gene(filelist, inpath, outpath, refernece, bedfile, name):
    if filelist:
        f = open(filelist,'r')
        l = f.read().strip().split('\n')
        for i in l:
            cyp_p_des(i, inpath, outpath, refernece, bedfile)
        f.close()
    else:
        cyp_p_des(name, inpath, outpath, refernece, bedfile)


if __name__ == '__main__':
    analysis_cyp_gene()
