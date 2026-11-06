wget https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M38/gencode.vM38.tRNAs.gtf.gz
zcat gencode.vM38.tRNAs.gtf.gz > mm39.tRNAs.gtf
head mm39.tRNAs.gtf
cut -f1 mm39.tRNAs.gtf |sort|uniq -c
awk 'BEGIN{FS=OFS="\t"} FNR==NR{if($0!~/^#/){keep[$1]=1} next} /^#/{print; next} ($1 in keep)' mm39.gtf mm39.tRNAs.gtf > mm39.tRNAs.mm39chroms.gtf
head mm39.tRNAs.mm39chroms.gtf
grep -v "^#" mm39.tRNAs.mm39chroms.gtf > tmp
awk 'BEGIN{OFS="\t"; t[1]="gene"; t[2]="transcript"; t[3]="exon"} /^#/ {print; next} {for(i=1;i<=3;i++){ $3=t[i]; print }}' tmp > tmp2
awk 'BEGIN{FS=OFS="\t"} /^#/{print; next} {attr=$9; for(i=10;i<=NF;i++) attr=attr" "$i; gsub(/[[:space:]]*;[[:space:]]*/, "; ", attr); sub(/[[:space:]]+$/, "", attr); print $1,$2,$3,$4,$5,$6,$7,$8,attr}' tmp2 > tmp2.fixed.gtf
mv tmp2.fixed.gtf mm39.tRNAs.mm39chroms.gtf
