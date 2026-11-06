#!/usr/bin/env python3
"""
Filter GTF file to exclude tRNA features.

Reads a GTF file and removes all lines where the feature type (column 3)
contains 'tRNA'. Outputs filtered GTF to file or stdout.
"""

import sys


def read_gtf_exclude_trna(input_file, output_file=None):
    """
    Read GTF file and exclude all tRNA features.

    Args:
        input_file: Path to input GTF file
        output_file: Path to output GTF file (optional, prints to stdout if None)
    """
    excluded_count = 0
    included_count = 0

    # Open output file if specified
    out_fh = open(output_file, 'w') if output_file else sys.stdout

    try:
        with open(input_file, 'r') as infile:
            for line in infile:
                # Skip comment lines and header lines
                if line.startswith('#'):
                    if output_file:
                        out_fh.write(line)
                    continue

                # Split the line by tabs
                fields = line.rstrip('\n').split('\t')

                # GTF must have at least 3 fields
                if len(fields) < 3:
                    continue

                # Column 3 (index 2) is the feature type
                feature_type = fields[2]

                # Column 9 (index 8) is the attributes
                attributes = fields[8] if len(fields) > 8 else ""

                # Exclude tRNA and related features:
                # 1. Direct tRNA features (feature_type = "tRNA")
                # 2. tRNA sub-features (gene_type "Mt_tRNA" or transcript_type "Mt_tRNA")
                if (feature_type == 'tRNA' or
                    'gene_type "Mt_tRNA"' in attributes or
                    'transcript_type "Mt_tRNA"' in attributes):
                    excluded_count += 1
                    continue

                # Write non-tRNA features to output
                out_fh.write(line)
                included_count += 1

        # Print statistics to stderr
        print(f"\n{'='*50}", file=sys.stderr)
        print(f"GTF Filtering Summary:", file=sys.stderr)
        print(f"Features excluded (tRNA): {excluded_count}", file=sys.stderr)
        print(f"Features included: {included_count}", file=sys.stderr)
        print(f"Total features: {excluded_count + included_count}", file=sys.stderr)
        print(f"{'='*50}", file=sys.stderr)

    finally:
        if output_file and out_fh != sys.stdout:
            out_fh.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python filter_trna.py <input.gtf> [output.gtf]")
        print("\nIf output file is not specified, writes to stdout")
        sys.exit(1)

    input_gtf = sys.argv[1]
    output_gtf = sys.argv[2] if len(sys.argv) > 2 else None

    read_gtf_exclude_trna(input_gtf, output_gtf)
