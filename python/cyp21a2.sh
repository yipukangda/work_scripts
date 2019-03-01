#Generate a SAM file containing aligned reads
~/softerwares/bwa/bwa mem -M human_g1k_v37_cyp21a2_psudo_excluded.fasta ~/Downloads/cyp21a2/S208_09A_CHG007616-LAN16031313-PNG16030031_L008_R1_val_1.fq.gz ~/Downloads/cyp21a2/S208_09A_CHG007616-LAN16031313-PNG16030031_L008_R2_val_2.fq.gz 1> ~/Downloads/cyp21a2/cyp21a2p_excluded.sam
#Run the following Picard command to sort the SAM file and convert it to BAM:
java -jar ~/softerwares/picard/build/libs/picard.jar SortSam INPUT=/home/jgs/Downloads/cyp21a2/cyp21a2p_excluded.sam OUTPUT=/home/jgs/Downloads/cyp21a2/cyp21a2p_excluded.sorted.bam SORT_ORDER=coordinate
#Run the following Picard command to mark duplicates:
java -jar ~/softerwares/picard/build/libs/picard.jar MarkDuplicates  INPUT=/home/jgs/Downloads/cyp21a2/cyp21a2p_excluded.sorted.bam OUTPUT=/home/jgs/Downloads/cyp21a2/cyp21a2p_excluded.sorted.markdup.bam METRICS_FILE=/home/jgs/Downloads/cyp21a2/metrics.txt
#Run the following Picard command to index the BAM file:
java -jar ~/softerwares/picard/build/libs/picard.jar BuildBamIndex INPUT=/home/jgs/Downloads/cyp21a2/cyp21a2p_excluded.sorted.markdup.bam

#Generate read id list file by marker bed file
samtools mpileup -f ~/database/gatk_bundle/b37/human_g1k_v37.fasta --positions ~/database/cyp21a2_ref/cyp_marker.bed -q 5 --output-QNAME ~/Downloads/aln.recal.bam -o ~/Downloads/pileup.cyp.txt

with open('pileup.cyp.txt') as p:
     l = p.read().strip().split('\n')
     for i in l:
         i = i.split('\t')
         m = i[5]
         ri = i[7]
         for r in re.finditer('(\.|,)',re.sub('(\^[\w\W]{1})|\$','',m)):
         print(ri[r.start()],'|',r.group())

#Extact read form bam according read id list
java -jar ~/softerwares/picard/build/libs/picard.jar FilterSamReads I=/home/jgs/Downloads/aln.recal.bam O=/home/jgs/Downloads/extract_bam.bam READ_LIST_FILE=/home/jgs/Downloads/read_id.list FILTER=includeReadList
java -jar ~/softerwares/picard/build/libs/picard.jar BuildBamIndex INPUT=/home/jgs/Downloads/extract_bam.bam
