#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 10:52:03 2017

@author: jgs
"""
import os
import re


#function for generate bam contain marked reads
def cyp_p_des(file1,file2,name):
#    #trim and OC
#    os.system('trim_galore --illumina --trim-n --paired -o /home/jgs/Downloads/cyp21a2/sec_bat/ \
#              /home/jgs/Downloads/cyp21a2/sec_bat/%s \
#              /home/jgs/Downloads/cyp21a2/sec_bat/%s'%(file1,file2))
#    file1 = file1.split('.')[0] + '_val_1.fq.gz'
#    file2 = file2.split('.')[0] + '_val_2.fq.gz'
    #Generate a SAM file containing aligned reads
    os.system('/home/jgs/softerwares/bwa/bwa mem -t 4 -M /home/jgs/database/cyp21a2_ref/human_g1k_v37_cyp21a2_psudo_excluded.fasta \
              /home/jgs/Downloads/cyp21a2/sec_bat/%s \
              /home/jgs/Downloads/cyp21a2/sec_bat/%s \
              1> /home/jgs/Downloads/cyp21a2/sec_bat/%s_cyp21a2p_excluded.sam'%(file1,file2,name))
    #Run the following Picard command to sort the SAM file and convert it to BAM:
    os.system('java -jar /home/jgs/softerwares/picard/build/libs/picard.jar SortSam \
              INPUT=/home/jgs/Downloads/cyp21a2/sec_bat/%s_cyp21a2p_excluded.sam \
              OUTPUT=/home/jgs/Downloads/cyp21a2/sec_bat/%s_cyp21a2p_excluded.sorted.bam \
              SORT_ORDER=coordinate'%(name,name))
    os.system('rm /home/jgs/Downloads/cyp21a2/sec_bat/%s_cyp21a2p_excluded.sam'%(name))
    #Run the following Picard command to mark duplicates:
    os.system('java -jar /home/jgs/softerwares/picard/build/libs/picard.jar MarkDuplicates  \
              INPUT=/home/jgs/Downloads/cyp21a2/sec_bat/%s_cyp21a2p_excluded.sorted.bam \
              OUTPUT=/home/jgs/Downloads/cyp21a2/sec_bat/%s_cyp21a2p_excluded.sorted.markdup.bam \
              METRICS_FILE=/home/jgs/Downloads/cyp21a2/sec_bat/%s_metrics.txt'%(name,name,name))
    #Run the following Picard command to index the BAM file:
    os.system('java -jar /home/jgs/softerwares/picard/build/libs/picard.jar BuildBamIndex \
              INPUT=/home/jgs/Downloads/cyp21a2/sec_bat/%s_cyp21a2p_excluded.sorted.markdup.bam'%(name))
    
    #Generate read id list file by marker bed file
    os.system('samtools mpileup -f /home/jgs/database/gatk_bundle/b37/human_g1k_v37.fasta \
              --positions /home/jgs/database/cyp21a2_ref/cyp_marker.bed -q 5 --output-QNAME \
              /home/jgs/Downloads/cyp21a2/sec_bat/%s_cyp21a2p_excluded.sorted.markdup.bam \
              -o /home/jgs/Downloads/%s_pileup.cyp.txt'%(name,name))
    
    
    with open('/home/jgs/Downloads/%s_pileup.cyp.txt'%(name)) as p:
        f = open('/home/jgs/Downloads/cyp21a2/sec_bat/%s_read_id.list'%(name),'w')
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
              I=/home/jgs/Downloads/cyp21a2/sec_bat/%s_cyp21a2p_excluded.sorted.markdup.bam \
              O=/home/jgs/Downloads/cyp21a2/sec_bat/%s_extract_bam.bam \
              READ_LIST_FILE=/home/jgs/Downloads/cyp21a2/sec_bat/%s_read_id.list FILTER=includeReadList'%(name,name,name))
    os.system('java -jar /home/jgs/softerwares/picard/build/libs/picard.jar BuildBamIndex \
              INPUT=/home/jgs/Downloads/cyp21a2/sec_bat/%s_extract_bam.bam'%(name))

#if __name__ == '__main__':
#    f = open('/home/jgs/Downloads/cyp21a2/sec_bat/file_list','r')
#    l = f.read().strip().split('\n')
#    for i in l:
#        os.system('echo %s'%(i[2]))
#        i = i.split('\t')
#        cyp_p_des(i[0], i[1], i[2])
