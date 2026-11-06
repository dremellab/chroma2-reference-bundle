# CHROMA2 reference bundle

Human GRCh38 with custom rDNA chromosome (`hg38`) and mouse GRCm39 (`mm39`) reference inputs used by CHROMA2. This bundle preserves the supplied FASTA/GTF bytes after decompression. It excludes hg38_basic, hs1, viruses, additives and alignment indexes.

## Release status

**Original-data prerelease with known annotation issues.** All payload checksums pass, but coordinate validation detects 122,277 repeat records on contigs absent from the supplied FASTAs and four chrR exon records extending one base beyond sequence bounds. LTR files also contain only plus-strand records. See [known issues](docs/known-issues.md) and [the validation report](docs/validation.json) before using this bundle. The original bytes are preserved; this is not a clean, comprehensive ERV mapping bundle.

## Download

Install Git and [Git LFS](https://git-lfs.com/), then run:

```bash
git lfs install
git clone https://github.com/dremellab/chroma2-reference-bundle.git
cd chroma2-reference-bundle
git checkout v1.0.0
git lfs pull
sha256sum -c SHA256SUMS
```

GitHub file previews may show LFS pointers. Use the commands above to retrieve the actual data. To decompress without removing the downloaded archives:

```bash
find human mouse -name '*.gz' -exec gzip -dk {} +
```

Build aligner indexes from the decompressed FASTA. Do not substitute a standard hg38 download for the custom human FASTA in this bundle.

## Contents

| Directory | FASTA | Main gene GTF |
| --- | --- | --- |
| `human/hg38_rDNA/` | `hg38.fa.gz` | `hg38-rDNA_v1.0_enriched.canonical_chromosomes_plus_chrR.gtf.gz` |
| `mouse/mm39/` | `mm39.fa.gz` | `mm39.no_tRNA.gtf.gz` |

Each directory also contains separate tRNA and chrR/rRNA annotations. Its `repeats/` directory contains six original RepeatMasker GTFs: LINE_L1, LINE_L2, LTR, SINE_Alu, SINE_MIR and other_repeat_elements. Category names are retained exactly as provided, including the mouse SINE_Alu filename; inspect attributes for biological family assignments. The human Pol III-specific GTFs are outside this release's scope.

`manifest.tsv` records original filenames, byte sizes and SHA-256 checksums for both compressed and decompressed files. `SHA256SUMS` verifies all compressed reference payloads. `docs/validation.json` records structural checks and repeat family counts.

## Known repeat coverage limitation

Both supplied LTR GTFs contain only `+` strand records (human: 376,332; mouse: 552,644). The preserved preparation scripts attempt to parse parenthesized RepeatMasker repeat coordinates as integers, which can skip reverse-strand records. These original annotations must not be treated as complete, strand-balanced repeat catalogs. They are preserved for reproducibility; a corrected repeat annotation should be generated and released separately before claiming comprehensive ERV coverage.

## Annotation compatibility

The repeat GTFs preserve `repeat_name` and `repeat_family`; they do not supply standard gene/transcript IDs. They are interval annotations and may need a documented conversion for gene-oriented counting software. Gene-level GTF records also legitimately lack transcript IDs. No synthetic IDs or merged annotations have been introduced.

Read [mapping notes](docs/mapping-notes.md) before handing these files to an analysis provider. Source provenance and known gaps are in [provenance](docs/provenance.md). A reference release identifies these exact bytes; it does not establish that every historical CHROMA2 analysis used them.

## Validate locally

Python 3, with no third-party packages:

```bash
python3 scripts/validate_bundle.py --output validation.local.json
```

The original snapshot is expected to exit nonzero because of the documented coordinate/contig errors. This reads every compressed payload, checks compressed and original hashes, derives chromosome lengths from FASTA sequences, and checks GTF coordinates, columns, strands and frames. It reports absent gene/transcript IDs separately from structural errors. It does not assert biological annotation completeness or absence of overlapping features.

## Attribution

These are redistributed reference data with upstream provenance described in `docs/provenance.md`. No blanket license is asserted over third-party data; preserve source attribution and consult upstream terms. This repository contains no sample reads or sample-level results.
