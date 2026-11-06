# Mapping and annotation notes

Use the FASTA and annotations from the same species directory. Human hg38 is a custom reference containing chrR; mouse mm39 is GRCm39. Chromosome names must match exactly, including the `chr` prefix.

The gene, tRNA, rRNA and six repeat annotations are separate layers, not disjoint feature sets. Adding their counts can double-count overlapping intervals. Do not concatenate them into a gene-counting GTF without defining feature identifiers and overlap handling.

The supplied LTR files contain only plus-strand records, a known limitation of this historical annotation preparation. Do not interpret the absence of a repeat annotation as evidence that the corresponding repeat is absent. A corrected repeat bundle requires regeneration from the raw RepeatMasker output and a separate version.

For ERV analysis, inspect `repeat_family` in the LTR GTF. LTR includes multiple families and is not an ERV-only category. The validation report tabulates the observed family labels. The category filenames alone do not specify a complete ERV analysis strategy.

The RepeatMasker GTFs use repeat classes as feature types (for example `LTR`), not conventional `exon` records, and lack gene_id/transcript_id attributes. Tools with default exon/gene_id settings require explicit configuration or a separately versioned conversion. Preserve repeat_name/repeat_family and define whether counts represent individual loci or aggregated families.

Agree with the provider on aligner/version, paired-end settings, multimapping policy, MAPQ filters, duplicate handling, strandedness and count assignment. Repetitive loci are especially sensitive to multimapping policy. dsRIP-seq and ATAC-seq need assay-appropriate processing; ATAC-specific Tn5 offsets should not be applied automatically to dsRIP-seq.

This bundle excludes viruses and spike-ins. If an original ATAC run mapped to a composite host-plus-virus/additive FASTA, exact mapping reproduction also requires those components and the original settings. This release freezes current reference inputs, not a verified reconstruction of an identified historical run.
