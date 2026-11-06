# Source provenance

## Snapshot

Packaged on 2026-11-06 from the lab's existing `workflows/reference_data/fasta_gtf/` reference collection. Original basenames and decompressed bytes are preserved. Compression uses `pigz -n -6 -p 2`: gzip timestamps and source filenames are omitted. SHA-256 values in manifest.tsv identify the exact source content. No reference sequences, feature records, attributes or coordinates were edited during packaging.

The current CHROMA2 config selects the human enriched canonical-plus-chrR GTF and mouse no_tRNA GTF. It also selects the separate tRNA, chrR and six RepeatMasker layers supplied here. Selection is based on current pipeline configuration, not provenance inferred from a particular sample run.

## Human hg38 with rDNA

Local construction documentation identifies the host as GRCh38 with a custom chrR ribosomal DNA sequence, derived from modified GenBank KY962518.1, and the enriched main annotation as RefSeq plus custom rDNA annotation. These descriptions are historical local documentation, not independently reconstructed upstream downloads. Exact upstream assembly patch/release and the full transformation chain have not been established for this snapshot. The decompressed FASTA and annotations, rather than the build name alone, define this release.

The source main GTF begins with `##gff-version 3` but uses GTF-style quoted attributes; this original header is retained. The separate chrR GTF overlaps the chrR annotation in the main GTF and is intended as a dedicated annotation layer.

## Mouse mm39

The main GTF header identifies GENCODE M38 / Ensembl 115, GRCm39, dated 2025-07-09. The selected file is the lab's `mm39.no_tRNA.gtf` derivative. Separate tRNA and chrR GTFs are provided. The local `make_tRNA_gtf_mm39.sh` downloads GENCODE M38 tRNAs, filters chromosome names against mm39.gtf, expands each record into gene/transcript/exon rows and normalizes attribute spacing. The exact original FASTA download and full chrR derivation history have not been established from the available metadata.

## RepeatMasker annotations

Six existing GTFs per species are distributed unchanged. The records identify RepeatMasker as their source and retain repeat_name/repeat_family attributes and available alignment scores/divergence attributes. The local construction guide and human/mouse splitting scripts describe a direct split of RepeatMasker `.out` records into six GTF categories (not a BED-to-GTF conversion). It infers the human source as a UCSC hg38 RepeatMasker track from a raw `.out` file dated 2014-01-15, but does not establish download provenance. The precise engine version, repeat-library release and mouse source history have not been independently established. `other_repeat_elements` is a catch-all category including simple repeats, low-complexity regions, satellites and other classes; it is not limited to transposable elements. No claim of current or exhaustive repeat-library coverage is made.

## Upstream reference information

- Human assembly: https://www.ncbi.nlm.nih.gov/grc/human/
- Custom human rDNA source accession: https://www.ncbi.nlm.nih.gov/nuccore/KY962518.1
- Mouse annotation release: https://www.gencodegenes.org/mouse/release_M38.html
- RepeatMasker: https://www.repeatmasker.org/

These links identify upstream projects/accessions; they are not substitutes for the exact files and checksums in this repository. No single new data license is assigned to the upstream reference collection. Retain attribution and review upstream redistribution terms when reusing or repackaging.

## Preserved preparation scripts

Selected existing preparation scripts are included under `scripts/source-preparation/` for provenance. They were not rerun to create this release and contain historical paths/commands. The RepeatMasker parsers can skip records on parsing errors; their presence does not demonstrate that the supplied six files exhaust the raw input.

## Observed repeat coverage limitation

A full scan of each supplied LTR GTF found human 376,332 records and mouse 552,644 records, all on the plus strand. Both source splitting scripts parse RepeatMasker repeat_start/repeat_end fields with int(), while checking only for a literal opening parenthesis rather than parenthesized values. Reverse-strand RepeatMasker records can therefore be discarded by the exception handler. This is a significant coverage limitation. The original data remain unchanged; this release does not repair or imply complete repeat/ERV coverage.
