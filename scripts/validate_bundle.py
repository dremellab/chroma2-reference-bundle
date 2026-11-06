#!/usr/bin/env python3
"""Validate gzip payload checksums, FASTA sequences and GTF coordinate bounds."""
import argparse
import csv
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path


def inspect_fasta(path):
    sizes = {}
    current = None
    with gzip.open(path, 'rb') as handle:
        for line in iter(lambda: handle.readline(1024 * 1024), b''):
            if line.startswith(b'>'):
                current = line[1:].split()[0].decode('ascii')
                if current in sizes:
                    raise ValueError(f'Duplicate FASTA ID: {current}')
                sizes[current] = 0
            elif line.strip():
                if current is None:
                    raise ValueError('Sequence before FASTA header')
                sizes[current] += len(line.strip())
    return sizes


def inspect_gtf(path, sizes):
    rows = 0
    issues = Counter()
    examples = {}
    families = Counter()
    with gzip.open(path, 'rt') as handle:
        for number, line in enumerate(handle, 1):
            if not line.strip() or line.startswith('#'):
                continue
            rows += 1
            fields = line.rstrip('\n').split('\t')
            errors = []
            if len(fields) != 9:
                errors.append('not_nine_columns')
            else:
                chrom, _, _, start, end, _, strand, frame, attrs = fields
                try:
                    start, end = int(start), int(end)
                    if start < 1 or end < start:
                        errors.append('invalid_interval')
                    if chrom not in sizes:
                        errors.append('unknown_contig')
                    elif end > sizes[chrom]:
                        errors.append('outside_contig')
                except ValueError:
                    errors.append('noninteger_coordinates')
                if strand not in ('+', '-', '.'):
                    errors.append('invalid_strand')
                if frame not in ('0', '1', '2', '.'):
                    errors.append('invalid_frame')
                if 'gene_id "' not in attrs:
                    issues['missing_gene_id'] += 1
                if 'transcript_id "' not in attrs:
                    issues['missing_transcript_id'] += 1
                for attr in attrs.split(';'):
                    attr = attr.strip()
                    if attr.startswith('repeat_family '):
                        families[attr.split('"')[1]] += 1
            for error in errors:
                issues[error] += 1
                examples.setdefault(error, {'line': number, 'text': line.strip()[:300]})
    fatal = sum(v for k, v in issues.items() if k not in ('missing_gene_id', 'missing_transcript_id'))
    return {'rows': rows, 'issues': dict(issues), 'examples': examples, 'repeat_families': dict(families), 'fatal_errors': fatal}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    with (args.root / 'manifest.tsv').open() as handle:
        manifest = list(csv.DictReader(handle, delimiter='\t'))
    report = {'files': {}, 'fatal_errors': 0}
    genomes = {}
    for row in manifest:
        path = args.root / row['path']
        print('Checking hashes:', row['path'], flush=True)
        packed, unpacked = hashlib.sha256(), hashlib.sha256()
        with path.open('rb') as handle:
            for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b''):
                packed.update(chunk)
        with gzip.open(path, 'rb') as handle:
            for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b''):
                unpacked.update(chunk)
        if packed.hexdigest() != row['sha256_gzip'] or unpacked.hexdigest() != row['sha256_original']:
            raise ValueError(f'Checksum mismatch: {path}')
        if row['kind'] == 'fasta':
            genomes[row['assembly']] = inspect_fasta(path)
            report['files'][row['path']] = {'contig_lengths': genomes[row['assembly']], 'checksums': 'passed'}
    for row in manifest:
        if row['kind'] != 'fasta':
            print('Checking coordinates:', row['path'], flush=True)
            result = inspect_gtf(args.root / row['path'], genomes[row['assembly']])
            result['checksums'] = 'passed'
            report['files'][row['path']] = result
            report['fatal_errors'] += result['fatal_errors']
    output = json.dumps(report, indent=2) + '\n'
    if args.output:
        args.output.write_text(output)
    else:
        print(output)
    raise SystemExit(bool(report['fatal_errors']))


if __name__ == '__main__':
    main()
