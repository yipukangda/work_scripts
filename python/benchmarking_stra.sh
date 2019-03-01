docker run -it \
-v ~/softerwares/benchmarking-tools:/bench \
-v ~/database:/ref \
-v /mnt/data_sata_2t/vsftpd/wxq/ftp/files:/wxq \
-v /mnt/data_sata_2t/downloads/na12878_fq:/data \
pkrusche/hap.py /opt/hap.py/bin/hap.py \
/data/benchmarking_vcf/NA12878.vcf.gz \
/wxq/0320/HY18034390.reads1_converted_Output_Mutation_Report.vcf \
-o /wxq/0320/HY18034390.nextgene \
-r /ref/gatk_bundle/hg19/ucsc.hg19.fasta \
--stratification /bench/resources/stratification-bed-files/ga4gh_other.tsv \
-f /data/benchmarking_vcf/ConfidentRegions.bed.gz \
-V \
--threads 8 \
--roc QUAL --roc-filter LowQual \
-T /wxq/hy_test_0312/BED02.bed 
