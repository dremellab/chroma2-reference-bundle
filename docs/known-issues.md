# Validation findings for the original snapshot

This prerelease preserves source bytes and is not a fully compatible or complete mapping annotation bundle. Compressed and decompressed payload hashes passed. Structural validation found 122,281 coordinate/contig errors: 122,277 repeat records on absent contigs and four chrR exon records extending one base past FASTA sequence ends. Missing gene/transcript IDs are reported separately and are not included in that total.

| Annotation | Absent-contig records | Out-of-bounds records |
| --- | ---: | ---: |
| `human/hg38_rDNA/hg38-rDNA_v1.0_enriched.canonical_chromosomes_plus_chrR.gtf.gz` | 0 | 1 |
| `human/hg38_rDNA/hg38-rDNA_v1.0_enriched.chrR_only.gtf.gz` | 0 | 1 |
| `human/hg38_rDNA/repeats/hg38.repeatMasker.LINE_L1.gtf.gz` | 20189 | 0 |
| `human/hg38_rDNA/repeats/hg38.repeatMasker.LINE_L2.gtf.gz` | 6210 | 0 |
| `human/hg38_rDNA/repeats/hg38.repeatMasker.LTR.gtf.gz` | 14719 | 0 |
| `human/hg38_rDNA/repeats/hg38.repeatMasker.SINE_Alu.gtf.gz` | 29211 | 0 |
| `human/hg38_rDNA/repeats/hg38.repeatMasker.SINE_MIR.gtf.gz` | 7728 | 0 |
| `human/hg38_rDNA/repeats/hg38.repeatMasker.other_repeat_elements.gtf.gz` | 39077 | 0 |
| `mouse/mm39/mm39.no_tRNA.gtf.gz` | 0 | 1 |
| `mouse/mm39/mm39.chrR.gtf.gz` | 0 | 1 |
| `mouse/mm39/repeats/mm39.repeatMasker.LINE_L1.gtf.gz` | 928 | 0 |
| `mouse/mm39/repeats/mm39.repeatMasker.LINE_L2.gtf.gz` | 14 | 0 |
| `mouse/mm39/repeats/mm39.repeatMasker.LTR.gtf.gz` | 1062 | 0 |
| `mouse/mm39/repeats/mm39.repeatMasker.SINE_Alu.gtf.gz` | 465 | 0 |
| `mouse/mm39/repeats/mm39.repeatMasker.SINE_MIR.gtf.gz` | 25 | 0 |
| `mouse/mm39/repeats/mm39.repeatMasker.other_repeat_elements.gtf.gz` | 2649 | 0 |

Human chrR is 44,838 bases; the IGS exon ends at 44,839 in both the main and dedicated chrR GTF. Mouse chrR is 45,306 bases; the IGS exon ends at 45,307 in both GTFs. These are preserved original records, not silently clipped.

Repeat annotations include alternate/random contigs absent from these canonical-plus-chrR FASTAs. A mapping-specific derivative should explicitly filter absent contigs, record removed features, and address the chrR boundary records. Such a derivative changes the annotations and should have its own checksums and version.

Both LTR files have exclusively plus-strand records: human 376,332 and mouse 552,644. The preserved splitting scripts can discard reverse-strand records while parsing parenthesized repeat coordinates. Comprehensive repeat analysis requires regeneration from raw RepeatMasker outputs with a corrected parser, including both orientations. Filtering existing files cannot recover missing records.

The supplied repeat GTFs also lack gene_id/transcript_id and use category-specific feature types. Configure counting tools explicitly or produce a documented derivative.

The validator intentionally exits nonzero on the supplied snapshot. Its report documents existing problems; a passing checksum check does not imply passing coordinate validation. No validation finding has been suppressed.
