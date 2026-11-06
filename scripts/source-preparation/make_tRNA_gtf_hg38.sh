wget https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_49/gencode.v49.tRNAs.gtf.gz
zcat gencode.v49.tRNAs.gtf.gz > hg38.tRNAs.gtf
head hg38.tRNAs.gtf
cut -f1 hg38.tRNAs.gtf |sort|uniq -c
awk 'BEGIN{FS=OFS="\t"} FNR==NR{if($0!~/^#/){keep[$1]=1} next} /^#/{print; next} ($1 in keep)' hg38.gtf hg38.tRNAs.gtf > hg38.tRNAs.hg38chroms.gtf
head hg38.tRNAs.hg38chroms.gtf
grep -v "^#" hg38.tRNAs.hg38chroms.gtf > tmp
awk 'BEGIN{OFS="\t"; t[1]="gene"; t[2]="transcript"; t[3]="exon"} /^#/ {print; next} {for(i=1;i<=3;i++){ $3=t[i]; print }}' tmp > tmp2
awk 'BEGIN{FS=OFS="\t"} /^#/{print; next} {attr=$9; for(i=10;i<=NF;i++) attr=attr" "$i; gsub(/[[:space:]]*;[[:space:]]*/, "; ", attr); sub(/[[:space:]]+$/, "", attr); print $1,$2,$3,$4,$5,$6,$7,$8,attr}' tmp2 > tmp2.fixed.gtf
mv tmp2.fixed.gtf hg38.tRNAs.hg38chroms.gtf
