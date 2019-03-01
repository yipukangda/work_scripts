for i in "TP" "FP" "FN" "N:"
  do
  for j in "SNP" "INDEL"
    do
    zcat /home/wxq/ftp/files/HY18034390_bed02.vcf.gz | grep "chr.*$i.*$j" > /home/wxq/ftp/files/HY18034390_bed02.$i.$j.vcf
    done
  done
