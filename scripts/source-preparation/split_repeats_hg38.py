#!/usr/bin/env python3
import sys
from collections import defaultdict

# Categories and their conditions
def categorize(family):
    if family == "SINE/Alu":
        return "SINE/Alu"
    elif family == "LINE/L1":
        return "LINE/L1"
    elif family == "SINE/MIR":
        return "SINE/MIR"
    elif family == "LINE/L2":
        return "LINE/L2"
    elif family.startswith("LTR"):
        return "LTR"
    else:
        return "other_repeat_elements"

# Initialize file handles for BED and GTF
bed_files = {}
gtf_files = {}
categories = ["SINE/Alu", "LINE/L1", "SINE/MIR", "LINE/L2", "LTR", "other_repeat_elements"]

for cat in categories:
    safe_cat = cat.replace("/", "_")
    bed_files[cat] = open(f"hg38.repeatMasker.{safe_cat}.bed", "w")
    gtf_files[cat] = open(f"hg38.repeatMasker.{safe_cat}.gtf", "w")

# Parse RepeatMasker output
input_file = "hg38.fa.out"
stats = defaultdict(int)

with open(input_file, "r") as f:
    for line in f:
        line = line.rstrip()
        # Skip header lines (first 3 lines)
        if line.startswith("SW") or line.startswith("score") or line.strip() == "":
            continue

        fields = line.split()
        if len(fields) < 14:
            continue

        try:
            sw_score = int(fields[0])
            perc_div = float(fields[1])
            perc_del = float(fields[2])
            perc_ins = float(fields[3])
            chrom = fields[4]
            start = int(fields[5]) - 1  # Convert to 0-based
            end = int(fields[6])        # End is exclusive in BED
            strand = fields[8]
            repeat_name = fields[9]
            repeat_family = fields[10]
            repeat_start = int(fields[11]) if fields[11] != "(" else 0
            repeat_end = int(fields[12]) if fields[12] != "(" else 0
            repeat_id = fields[14] if len(fields) > 14 else "."

            cat = categorize(repeat_family)
            stats[cat] += 1

            # Write BED file (0-based, half-open)
            bed_line = f"{chrom}\t{start}\t{end}\t{repeat_name}_{repeat_family}\t{sw_score}\t{strand}\n"
            bed_files[cat].write(bed_line)

            # Write GTF file (1-based, inclusive)
            # GTF attributes: name, family, score, divergence
            attributes = f'repeat_name "{repeat_name}"; repeat_family "{repeat_family}"; sw_score "{sw_score}"; perc_div "{perc_div}"; perc_del "{perc_del}"; perc_ins "{perc_ins}"'
            gtf_line = f"{chrom}\tRepeatMasker\t{cat}\t{start+1}\t{end}\t{sw_score}\t{strand}\t.\t{attributes}\n"
            gtf_files[cat].write(gtf_line)

        except (ValueError, IndexError) as e:
            print(f"Warning: Could not parse line: {line}", file=sys.stderr)
            continue

# Close all files
for cat in categories:
    bed_files[cat].close()
    gtf_files[cat].close()

# Print statistics
print("Split RepeatMasker output into 6 categories:")
print("-" * 50)
total = 0
for cat in categories:
    count = stats[cat]
    total += count
    print(f"{cat:20s}: {count:10,d} repeats")
print("-" * 50)
print(f"{'Total':20s}: {total:10,d} repeats")
print("\nOutput files:")
print("BED files:")
for cat in categories:
    safe_cat = cat.replace("/", "_")
    print(f"  hg38.repeatMasker.{safe_cat}.bed")
print("\nGTF files:")
for cat in categories:
    safe_cat = cat.replace("/", "_")
    print(f"  hg38.repeatMasker.{safe_cat}.gtf")
