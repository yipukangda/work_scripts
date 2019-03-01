~/softerwares/GATK4x/gatk-4.0.3.0/gatk BaseRecalibrator \
       -I /mnt/data_sata_2t/downloads/na12878_fq/gatk4_test/NIST7035_TAAGGCGA_L002.sorted.markdup.bam \
       --known-sites ~/database/gatk_bundle/GRCh37/ftp.broadinstitute.org/bundle/b37/dbsnp_138.b37.vcf \
       --known-sites ~/database/gatk_bundle/GRCh37/ftp.broadinstitute.org/bundle/b37/Mills_and_1000G_gold_standard.indels.b37.vcf \
       -O /mnt/data_sata_2t/downloads/na12878_fq/gatk4_test/NIST7035.gatk4.recal_data.table \
       -R ~/database/gatk_bundle/b37/human_g1k_v37.fasta 

~/softerwares/GATK4x/gatk-4.0.3.0/gatk ApplyBQSR \
       -bqsr /mnt/data_sata_2t/downloads/na12878_fq/gatk4_test/NIST7035.gatk4.recal_data.table \
       -I /mnt/data_sata_2t/downloads/na12878_fq/gatk4_test/NIST7035_TAAGGCGA_L002.sorted.markdup.bam \
       -O /mnt/data_sata_2t/downloads/na12878_fq/gatk4_test/NIST7035.gatk4.sorted.markdup.bqsr.bam

~/softerwares/GATK4x/gatk-4.0.3.0/gatk HaplotypeCaller \
       -I /mnt/data_sata_2t/downloads/na12878_fq/gatk4_test/NIST7035.gatk4.sorted.markdup.bqsr.bam \
       -O /mnt/data_sata_2t/downloads/na12878_fq/gatk4_test/NIST7035.gatk4.vcf \
       -R ~/database/gatk_bundle/b37/human_g1k_v37.fasta
