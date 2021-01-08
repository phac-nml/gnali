# Filtering #

Note that by default, gNALI filters for high-confidence loss-of-function variants. There is currently no way to disable this.

## Additional Filters ##

The below filters are available through the `-a`/`--additional_filters` parameter.

For example, if we were using gnomADv2.1.1 and wanted to filter for variants with an alternate allele count greater than 3, we would find the following annotation below:

| Annotation | Value Type | Description |
|------------|------------|-------------|
| AC | Integer | Alternate allele count for samples |

... and add the expression "AC>3" to our command, like so:

```bash
gnali
    --input my_gnali_stuff/data/genes.txt
    --predefined_filters homozygous-controls
    --additional_filters "AC>3"
    --vcf
    --output my_results/
```

### gnomADv2.1.1 Filters ###
| Annotation | Value Type | Description |
|------------|------------|-------------|
| AC | Integer | Alternate allele count for samples |
| AN | Integer | Total number of alleles in samples |
| AF | Float | Alternate allele frequency in samples |
| rf_tp_probability | Float | Random forest prediction probability for a site being a true variant |
| FS | Float | Phred-scaled p-value of Fisher's exact test for strand bias |
| InbreedingCoeff | Float | Inbreeding coefficient as estimated from the genotype likelihoods per-sample when compared against the Hardy-Weinberg expectation |
| MQ | Float | Root mean square of the mapping quality of reads across all samples |
| MQRankSum | Float | Z-score from Wilcoxon rank sum test of alternate vs. reference read mapping qualities |
| QD | Float | Variant call confidence normalized by depth of sample reads supporting a variant |
| ReadPosRankSum | Float | Z-score from Wilcoxon rank sum test of alternate vs. reference read position bias |
| SOR | Float | Strand bias estimated by the symmetric odds ratio test |
| VQSR_POSITIVE_TRAIN_SITE | Flag | Variant was used to build the positive training set of high-quality variants for VQSR |
| VQSR_NEGATIVE_TRAIN_SITE | Flag | Variant was used to build the negative training set of low-quality variants for VQSR |
| BaseQRankSum | Float | Z-score from Wilcoxon rank sum test of alternate vs. reference base qualities |
| ClippingRankSum | Float | Z-score from Wilcoxon rank sum test of alternate vs. reference number of hard clipped bases |
| DP | Integer | Depth of informative coverage for each sample; reads with MQ=255 or with bad mates are filtered |
| VQSLOD | Float | Log-odds ratio of being a true variant versus being a false positive under the trained VQSR Gaussian mixture model |
| VQSR_culprit | String | Worst-performing annotation in the VQSR Gaussian mixture model |
| segdup | Flag | Variant falls within a segmental duplication region |
| lcr | Flag | Variant falls within a low complexity region |
| decoy | Flag | Variant falls within a reference decoy region |
| nonpar | Flag | Variant (on sex chromosome) falls outside a pseudoautosomal region |
| rf_positive_label | Flag | Variant was labelled as a positive example for training of random forest model |
| rf_negative_label | Flag | Variant was labelled as a negative example for training of random forest model |
| rf_label | String | Random forest training label |
| rf_train | Flag | Variant was used in training random forest model |
| transmitted_singleton | Flag | Variant was a callset-wide doubleton that was transmitted within a family (i.e.
| variant_type | String | Variant type (snv, indel, multi-snv, multi-indel, or mixed) |
| allele_type | String | Allele type (snv, indel, multi-snv, multi-indel, or mixed) |
| n_alt_alleles | Integer | Total number of alternate alleles observed at variant locus |
| was_mixed | Flag | Variant type was mixed |
| has_star | Flag | Variant locus coincides with a spanning deletion (represented by a star) observed elsewhere in the callset |
| pab_max | Float | Maximum p-value over callset for binomial test of observed allele balance for a heterozygous genotype
| gq_hist_alt_bin_freq | String | Histogram for GQ in heterozygous individuals; bin edges are: 0|5|10|15|20|25|30|35|40|45|50|55|60|65|70|75|80|85|90|95|100 |
| gq_hist_all_bin_freq | String | Histogram for GQ; bin edges are: 0|5|10|15|20|25|30|35|40|45|50|55|60|65|70|75|80|85|90|95|100 |
| dp_hist_alt_bin_freq | String | Histogram for DP in heterozygous individuals; bin edges are: 0|5|10|15|20|25|30|35|40|45|50|55|60|65|70|75|80|85|90|95|100 |
| dp_hist_alt_n_larger | Integer | Count of DP values falling above highest histogram bin edge |
| dp_hist_all_bin_freq | String | Histogram for DP; bin edges are: 0|5|10|15|20|25|30|35|40|45|50|55|60|65|70|75|80|85|90|95|100 |
| dp_hist_all_n_larger | Integer | Count of DP values falling above highest histogram bin edge |
| ab_hist_alt_bin_freq | String | Histogram for AB in heterozygous individuals; bin edges are: 0.00|0.05|0.10|0.15|0.20|0.25|0.30|0.35|0.40|0.45|0.50|0.55|0.60|0.65|0.70|0.75|0.80|0.85|0.90|0.95|1.00 |
| AC_nfe_seu | Integer | Alternate allele count for samples of Southern European ancestry |
| AN_nfe_seu | Integer | Total number of alleles in samples of Southern European ancestry |
| AF_nfe_seu | Float | Alternate allele frequency in samples of Southern European ancestry |
| nhomalt_nfe_seu | Integer | Count of homozygous individuals in samples of Southern European ancestry |
| controls_AC_afr_male | Integer | Alternate allele count for male samples of African-American/African ancestry in the controls subset |
| controls_AN_afr_male | Integer | Total number of alleles in male samples of African-American/African ancestry in the controls subset |
| controls_AF_afr_male | Float | Alternate allele frequency in male samples of African-American/African ancestry in the controls subset |
| controls_nhomalt_afr_male | Integer | Count of homozygous individuals in male samples of African-American/African ancestry in the controls subset |
| non_neuro_AC_eas_kor | Integer | Alternate allele count for samples of Korean ancestry in the non_neuro subset |
| non_neuro_AN_eas_kor | Integer | Total number of alleles in samples of Korean ancestry in the non_neuro subset |
| non_neuro_AF_eas_kor | Float | Alternate allele frequency in samples of Korean ancestry in the non_neuro subset |
| non_neuro_nhomalt_eas_kor | Integer | Count of homozygous individuals in samples of Korean ancestry in the non_neuro subset |
| non_topmed_AC_amr | Integer | Alternate allele count for samples of Latino ancestry in the non_topmed subset |
| non_topmed_AN_amr | Integer | Total number of alleles in samples of Latino ancestry in the non_topmed subset |
| non_topmed_AF_amr | Float | Alternate allele frequency in samples of Latino ancestry in the non_topmed subset |
| non_topmed_nhomalt_amr | Integer | Count of homozygous individuals in samples of Latino ancestry in the non_topmed subset |
| non_cancer_AC_asj_female | Integer | Alternate allele count for female samples of Ashkenazi Jewish ancestry in the non_cancer subset |
| non_cancer_AN_asj_female | Integer | Total number of alleles in female samples of Ashkenazi Jewish ancestry in the non_cancer subset |
| non_cancer_AF_asj_female | Float | Alternate allele frequency in female samples of Ashkenazi Jewish ancestry in the non_cancer subset |
| non_cancer_nhomalt_asj_female | Integer | Count of homozygous individuals in female samples of Ashkenazi Jewish ancestry in the non_cancer subset |
| AC_raw | Integer | Alternate allele count for samples
| AN_raw | Integer | Total number of alleles in samples
| AF_raw | Float | Alternate allele frequency in samples
| nhomalt_raw | Integer | Count of homozygous individuals in samples
| AC_fin_female | Integer | Alternate allele count for female samples of Finnish ancestry |
| AN_fin_female | Integer | Total number of alleles in female samples of Finnish ancestry |
| AF_fin_female | Float | Alternate allele frequency in female samples of Finnish ancestry |
| nhomalt_fin_female | Integer | Count of homozygous individuals in female samples of Finnish ancestry |
| non_cancer_AC_oth_female | Integer | Alternate allele count for female samples of Other ancestry in the non_cancer subset |
| non_cancer_AN_oth_female | Integer | Total number of alleles in female samples of Other ancestry in the non_cancer subset |
| non_cancer_AF_oth_female | Float | Alternate allele frequency in female samples of Other ancestry in the non_cancer subset |
| non_cancer_nhomalt_oth_female | Integer | Count of homozygous individuals in female samples of Other ancestry in the non_cancer subset |
| AC_nfe_bgr | Integer | Alternate allele count for samples of Bulgarian (Eastern European) ancestry |
| AN_nfe_bgr | Integer | Total number of alleles in samples of Bulgarian (Eastern European) ancestry |
| AF_nfe_bgr | Float | Alternate allele frequency in samples of Bulgarian (Eastern European) ancestry |
| nhomalt_nfe_bgr | Integer | Count of homozygous individuals in samples of Bulgarian (Eastern European) ancestry |
| non_neuro_AC_asj_female | Integer | Alternate allele count for female samples of Ashkenazi Jewish ancestry in the non_neuro subset |
| non_neuro_AN_asj_female | Integer | Total number of alleles in female samples of Ashkenazi Jewish ancestry in the non_neuro subset |
| non_neuro_AF_asj_female | Float | Alternate allele frequency in female samples of Ashkenazi Jewish ancestry in the non_neuro subset |
| non_neuro_nhomalt_asj_female | Integer | Count of homozygous individuals in female samples of Ashkenazi Jewish ancestry in the non_neuro subset |
| AC_sas_male | Integer | Alternate allele count for male samples of South Asian ancestry |
| AN_sas_male | Integer | Total number of alleles in male samples of South Asian ancestry |
| AF_sas_male | Float | Alternate allele frequency in male samples of South Asian ancestry |
| nhomalt_sas_male | Integer | Count of homozygous individuals in male samples of South Asian ancestry |
| non_neuro_AC_afr_male | Integer | Alternate allele count for male samples of African-American/African ancestry in the non_neuro subset |
| non_neuro_AN_afr_male | Integer | Total number of alleles in male samples of African-American/African ancestry in the non_neuro subset |
| non_neuro_AF_afr_male | Float | Alternate allele frequency in male samples of African-American/African ancestry in the non_neuro subset |
| non_neuro_nhomalt_afr_male | Integer | Count of homozygous individuals in male samples of African-American/African ancestry in the non_neuro subset |
| AC_afr_male | Integer | Alternate allele count for male samples of African-American/African ancestry |
| AN_afr_male | Integer | Total number of alleles in male samples of African-American/African ancestry |
| AF_afr_male | Float | Alternate allele frequency in male samples of African-American/African ancestry |
| nhomalt_afr_male | Integer | Count of homozygous individuals in male samples of African-American/African ancestry |
| AC_afr | Integer | Alternate allele count for samples of African-American/African ancestry |
| AN_afr | Integer | Total number of alleles in samples of African-American/African ancestry |
| AF_afr | Float | Alternate allele frequency in samples of African-American/African ancestry |
| nhomalt_afr | Integer | Count of homozygous individuals in samples of African-American/African ancestry |
| controls_AC_nfe_swe | Integer | Alternate allele count for samples of Swedish ancestry in the controls subset |
| controls_AN_nfe_swe | Integer | Total number of alleles in samples of Swedish ancestry in the controls subset |
| controls_AF_nfe_swe | Float | Alternate allele frequency in samples of Swedish ancestry in the controls subset |
| controls_nhomalt_nfe_swe | Integer | Count of homozygous individuals in samples of Swedish ancestry in the controls subset |
| non_neuro_AC_afr_female | Integer | Alternate allele count for female samples of African-American/African ancestry in the non_neuro subset |
| non_neuro_AN_afr_female | Integer | Total number of alleles in female samples of African-American/African ancestry in the non_neuro subset |
| non_neuro_AF_afr_female | Float | Alternate allele frequency in female samples of African-American/African ancestry in the non_neuro subset |
| non_neuro_nhomalt_afr_female | Integer | Count of homozygous individuals in female samples of African-American/African ancestry in the non_neuro subset |
| non_topmed_AC_amr_female | Integer | Alternate allele count for female samples of Latino ancestry in the non_topmed subset |
| non_topmed_AN_amr_female | Integer | Total number of alleles in female samples of Latino ancestry in the non_topmed subset |
| non_topmed_AF_amr_female | Float | Alternate allele frequency in female samples of Latino ancestry in the non_topmed subset |
| non_topmed_nhomalt_amr_female | Integer | Count of homozygous individuals in female samples of Latino ancestry in the non_topmed subset |
| non_cancer_AC_female | Integer | Alternate allele count for female samples in the non_cancer subset |
| non_cancer_AN_female | Integer | Total number of alleles in female samples in the non_cancer subset |
| non_cancer_AF_female | Float | Alternate allele frequency in female samples in the non_cancer subset |
| non_cancer_nhomalt_female | Integer | Count of homozygous individuals in female samples in the non_cancer subset |
| non_cancer_AC_nfe_onf | Integer | Alternate allele count for samples of Other Non-Finnish European ancestry in the non_cancer subset |
| non_cancer_AN_nfe_onf | Integer | Total number of alleles in samples of Other Non-Finnish European ancestry in the non_cancer subset |
| non_cancer_AF_nfe_onf | Float | Alternate allele frequency in samples of Other Non-Finnish European ancestry in the non_cancer subset |
| non_cancer_nhomalt_nfe_onf | Integer | Count of homozygous individuals in samples of Other Non-Finnish European ancestry in the non_cancer subset |
| non_cancer_AC_male | Integer | Alternate allele count for male samples in the non_cancer subset |
| non_cancer_AN_male | Integer | Total number of alleles in male samples in the non_cancer subset |
| non_cancer_AF_male | Float | Alternate allele frequency in male samples in the non_cancer subset |
| non_cancer_nhomalt_male | Integer | Count of homozygous individuals in male samples in the non_cancer subset |
| non_topmed_AC_oth_female | Integer | Alternate allele count for female samples of Other ancestry in the non_topmed subset |
| non_topmed_AN_oth_female | Integer | Total number of alleles in female samples of Other ancestry in the non_topmed subset |
| non_topmed_AF_oth_female | Float | Alternate allele frequency in female samples of Other ancestry in the non_topmed subset |
| non_topmed_nhomalt_oth_female | Integer | Count of homozygous individuals in female samples of Other ancestry in the non_topmed subset |
| AC_eas_female | Integer | Alternate allele count for female samples of East Asian ancestry |
| AN_eas_female | Integer | Total number of alleles in female samples of East Asian ancestry |
| AF_eas_female | Float | Alternate allele frequency in female samples of East Asian ancestry |
| nhomalt_eas_female | Integer | Count of homozygous individuals in female samples of East Asian ancestry |
| non_cancer_AC_sas_female | Integer | Alternate allele count for female samples of South Asian ancestry in the non_cancer subset |
| non_cancer_AN_sas_female | Integer | Total number of alleles in female samples of South Asian ancestry in the non_cancer subset |
| non_cancer_AF_sas_female | Float | Alternate allele frequency in female samples of South Asian ancestry in the non_cancer subset |
| non_cancer_nhomalt_sas_female | Integer | Count of homozygous individuals in female samples of South Asian ancestry in the non_cancer subset |
| AC_afr_female | Integer | Alternate allele count for female samples of African-American/African ancestry |
| AN_afr_female | Integer | Total number of alleles in female samples of African-American/African ancestry |
| AF_afr_female | Float | Alternate allele frequency in female samples of African-American/African ancestry |
| nhomalt_afr_female | Integer | Count of homozygous individuals in female samples of African-American/African ancestry |
| AC_sas | Integer | Alternate allele count for samples of South Asian ancestry |
| AN_sas | Integer | Total number of alleles in samples of South Asian ancestry |
| AF_sas | Float | Alternate allele frequency in samples of South Asian ancestry |
| nhomalt_sas | Integer | Count of homozygous individuals in samples of South Asian ancestry |
| non_neuro_AC_female | Integer | Alternate allele count for female samples in the non_neuro subset |
| non_neuro_AN_female | Integer | Total number of alleles in female samples in the non_neuro subset |
| non_neuro_AF_female | Float | Alternate allele frequency in female samples in the non_neuro subset |
| non_neuro_nhomalt_female | Integer | Count of homozygous individuals in female samples in the non_neuro subset |
| controls_AC_afr | Integer | Alternate allele count for samples of African-American/African ancestry in the controls subset |
| controls_AN_afr | Integer | Total number of alleles in samples of African-American/African ancestry in the controls subset |
| controls_AF_afr | Float | Alternate allele frequency in samples of African-American/African ancestry in the controls subset |
| controls_nhomalt_afr | Integer | Count of homozygous individuals in samples of African-American/African ancestry in the controls subset |
| non_neuro_AC_eas_jpn | Integer | Alternate allele count for samples of Japanese ancestry in the non_neuro subset |
| non_neuro_AN_eas_jpn | Integer | Total number of alleles in samples of Japanese ancestry in the non_neuro subset |
| non_neuro_AF_eas_jpn | Float | Alternate allele frequency in samples of Japanese ancestry in the non_neuro subset |
| non_neuro_nhomalt_eas_jpn | Integer | Count of homozygous individuals in samples of Japanese ancestry in the non_neuro subset |
| AC_nfe_onf | Integer | Alternate allele count for samples of Other Non-Finnish European ancestry |
| AN_nfe_onf | Integer | Total number of alleles in samples of Other Non-Finnish European ancestry |
| AF_nfe_onf | Float | Alternate allele frequency in samples of Other Non-Finnish European ancestry |
| nhomalt_nfe_onf | Integer | Count of homozygous individuals in samples of Other Non-Finnish European ancestry |
| non_cancer_AC_amr_male | Integer | Alternate allele count for male samples of Latino ancestry in the non_cancer subset |
| non_cancer_AN_amr_male | Integer | Total number of alleles in male samples of Latino ancestry in the non_cancer subset |
| non_cancer_AF_amr_male | Float | Alternate allele frequency in male samples of Latino ancestry in the non_cancer subset |
| non_cancer_nhomalt_amr_male | Integer | Count of homozygous individuals in male samples of Latino ancestry in the non_cancer subset |
| controls_AC_fin_male | Integer | Alternate allele count for male samples of Finnish ancestry in the controls subset |
| controls_AN_fin_male | Integer | Total number of alleles in male samples of Finnish ancestry in the controls subset |
| controls_AF_fin_male | Float | Alternate allele frequency in male samples of Finnish ancestry in the controls subset |
| controls_nhomalt_fin_male | Integer | Count of homozygous individuals in male samples of Finnish ancestry in the controls subset |
| non_neuro_AC_nfe_nwe | Integer | Alternate allele count for samples of North-Western European ancestry in the non_neuro subset |
| non_neuro_AN_nfe_nwe | Integer | Total number of alleles in samples of North-Western European ancestry in the non_neuro subset |
| non_neuro_AF_nfe_nwe | Float | Alternate allele frequency in samples of North-Western European ancestry in the non_neuro subset |
| non_neuro_nhomalt_nfe_nwe | Integer | Count of homozygous individuals in samples of North-Western European ancestry in the non_neuro subset |
| AC_fin_male | Integer | Alternate allele count for male samples of Finnish ancestry |
| AN_fin_male | Integer | Total number of alleles in male samples of Finnish ancestry |
| AF_fin_male | Float | Alternate allele frequency in male samples of Finnish ancestry |
| nhomalt_fin_male | Integer | Count of homozygous individuals in male samples of Finnish ancestry |
| AC_nfe_female | Integer | Alternate allele count for female samples of Non-Finnish European ancestry |
| AN_nfe_female | Integer | Total number of alleles in female samples of Non-Finnish European ancestry |
| AF_nfe_female | Float | Alternate allele frequency in female samples of Non-Finnish European ancestry |
| nhomalt_nfe_female | Integer | Count of homozygous individuals in female samples of Non-Finnish European ancestry |
| AC_amr | Integer | Alternate allele count for samples of Latino ancestry |
| AN_amr | Integer | Total number of alleles in samples of Latino ancestry |
| AF_amr | Float | Alternate allele frequency in samples of Latino ancestry |
| nhomalt_amr | Integer | Count of homozygous individuals in samples of Latino ancestry |
| non_topmed_AC_nfe_male | Integer | Alternate allele count for male samples of Non-Finnish European ancestry in the non_topmed subset |
| non_topmed_AN_nfe_male | Integer | Total number of alleles in male samples of Non-Finnish European ancestry in the non_topmed subset |
| non_topmed_AF_nfe_male | Float | Alternate allele frequency in male samples of Non-Finnish European ancestry in the non_topmed subset |
| non_topmed_nhomalt_nfe_male | Integer | Count of homozygous individuals in male samples of Non-Finnish European ancestry in the non_topmed subset |
| non_neuro_AC_sas | Integer | Alternate allele count for samples of South Asian ancestry in the non_neuro subset |
| non_neuro_AN_sas | Integer | Total number of alleles in samples of South Asian ancestry in the non_neuro subset |
| non_neuro_AF_sas | Float | Alternate allele frequency in samples of South Asian ancestry in the non_neuro subset |
| non_neuro_nhomalt_sas | Integer | Count of homozygous individuals in samples of South Asian ancestry in the non_neuro subset |
| non_cancer_AC_fin_male | Integer | Alternate allele count for male samples of Finnish ancestry in the non_cancer subset |
| non_cancer_AN_fin_male | Integer | Total number of alleles in male samples of Finnish ancestry in the non_cancer subset |
| non_cancer_AF_fin_male | Float | Alternate allele frequency in male samples of Finnish ancestry in the non_cancer subset |
| non_cancer_nhomalt_fin_male | Integer | Count of homozygous individuals in male samples of Finnish ancestry in the non_cancer subset |
| non_cancer_AC_nfe_seu | Integer | Alternate allele count for samples of Southern European ancestry in the non_cancer subset |
| non_cancer_AN_nfe_seu | Integer | Total number of alleles in samples of Southern European ancestry in the non_cancer subset |
| non_cancer_AF_nfe_seu | Float | Alternate allele frequency in samples of Southern European ancestry in the non_cancer subset |
| non_cancer_nhomalt_nfe_seu | Integer | Count of homozygous individuals in samples of Southern European ancestry in the non_cancer subset |
| AC_eas | Integer | Alternate allele count for samples of East Asian ancestry |
| AN_eas | Integer | Total number of alleles in samples of East Asian ancestry |
| AF_eas | Float | Alternate allele frequency in samples of East Asian ancestry |
| nhomalt_eas | Integer | Count of homozygous individuals in samples of East Asian ancestry |
| nhomalt | Integer | Count of homozygous individuals in samples |
| non_neuro_AC_nfe_female | Integer | Alternate allele count for female samples of Non-Finnish European ancestry in the non_neuro subset |
| non_neuro_AN_nfe_female | Integer | Total number of alleles in female samples of Non-Finnish European ancestry in the non_neuro subset |
| non_neuro_AF_nfe_female | Float | Alternate allele frequency in female samples of Non-Finnish European ancestry in the non_neuro subset |
| non_neuro_nhomalt_nfe_female | Integer | Count of homozygous individuals in female samples of Non-Finnish European ancestry in the non_neuro subset |
| non_neuro_AC_afr | Integer | Alternate allele count for samples of African-American/African ancestry in the non_neuro subset |
| non_neuro_AN_afr | Integer | Total number of alleles in samples of African-American/African ancestry in the non_neuro subset |
| non_neuro_AF_afr | Float | Alternate allele frequency in samples of African-American/African ancestry in the non_neuro subset |
| non_neuro_nhomalt_afr | Integer | Count of homozygous individuals in samples of African-American/African ancestry in the non_neuro subset |
| controls_AC_raw | Integer | Alternate allele count for samples in the controls subset
| controls_AN_raw | Integer | Total number of alleles in samples in the controls subset
| controls_AF_raw | Float | Alternate allele frequency in samples in the controls subset
| controls_nhomalt_raw | Integer | Count of homozygous individuals in samples in the controls subset
| non_cancer_AC_eas | Integer | Alternate allele count for samples of East Asian ancestry in the non_cancer subset |
| non_cancer_AN_eas | Integer | Total number of alleles in samples of East Asian ancestry in the non_cancer subset |
| non_cancer_AF_eas | Float | Alternate allele frequency in samples of East Asian ancestry in the non_cancer subset |
| non_cancer_nhomalt_eas | Integer | Count of homozygous individuals in samples of East Asian ancestry in the non_cancer subset |
| non_cancer_AC_amr_female | Integer | Alternate allele count for female samples of Latino ancestry in the non_cancer subset |
| non_cancer_AN_amr_female | Integer | Total number of alleles in female samples of Latino ancestry in the non_cancer subset |
| non_cancer_AF_amr_female | Float | Alternate allele frequency in female samples of Latino ancestry in the non_cancer subset |
| non_cancer_nhomalt_amr_female | Integer | Count of homozygous individuals in female samples of Latino ancestry in the non_cancer subset |
| non_neuro_AC_nfe_swe | Integer | Alternate allele count for samples of Swedish ancestry in the non_neuro subset |
| non_neuro_AN_nfe_swe | Integer | Total number of alleles in samples of Swedish ancestry in the non_neuro subset |
| non_neuro_AF_nfe_swe | Float | Alternate allele frequency in samples of Swedish ancestry in the non_neuro subset |
| non_neuro_nhomalt_nfe_swe | Integer | Count of homozygous individuals in samples of Swedish ancestry in the non_neuro subset |
| controls_AC_male | Integer | Alternate allele count for male samples in the controls subset |
| controls_AN_male | Integer | Total number of alleles in male samples in the controls subset |
| controls_AF_male | Float | Alternate allele frequency in male samples in the controls subset |
| controls_nhomalt_male | Integer | Count of homozygous individuals in male samples in the controls subset |
| non_topmed_AC_male | Integer | Alternate allele count for male samples in the non_topmed subset |
| non_topmed_AN_male | Integer | Total number of alleles in male samples in the non_topmed subset |
| non_topmed_AF_male | Float | Alternate allele frequency in male samples in the non_topmed subset |
| non_topmed_nhomalt_male | Integer | Count of homozygous individuals in male samples in the non_topmed subset |
| controls_AC_eas_jpn | Integer | Alternate allele count for samples of Japanese ancestry in the controls subset |
| controls_AN_eas_jpn | Integer | Total number of alleles in samples of Japanese ancestry in the controls subset |
| controls_AF_eas_jpn | Float | Alternate allele frequency in samples of Japanese ancestry in the controls subset |
| controls_nhomalt_eas_jpn | Integer | Count of homozygous individuals in samples of Japanese ancestry in the controls subset |
| controls_AC_nfe_female | Integer | Alternate allele count for female samples of Non-Finnish European ancestry in the controls subset |
| controls_AN_nfe_female | Integer | Total number of alleles in female samples of Non-Finnish European ancestry in the controls subset |
| controls_AF_nfe_female | Float | Alternate allele frequency in female samples of Non-Finnish European ancestry in the controls subset |
| controls_nhomalt_nfe_female | Integer | Count of homozygous individuals in female samples of Non-Finnish European ancestry in the controls subset |
| non_neuro_AC_amr | Integer | Alternate allele count for samples of Latino ancestry in the non_neuro subset |
| non_neuro_AN_amr | Integer | Total number of alleles in samples of Latino ancestry in the non_neuro subset |
| non_neuro_AF_amr | Float | Alternate allele frequency in samples of Latino ancestry in the non_neuro subset |
| non_neuro_nhomalt_amr | Integer | Count of homozygous individuals in samples of Latino ancestry in the non_neuro subset |
| non_neuro_AC_eas_female | Integer | Alternate allele count for female samples of East Asian ancestry in the non_neuro subset |
| non_neuro_AN_eas_female | Integer | Total number of alleles in female samples of East Asian ancestry in the non_neuro subset |
| non_neuro_AF_eas_female | Float | Alternate allele frequency in female samples of East Asian ancestry in the non_neuro subset |
| non_neuro_nhomalt_eas_female | Integer | Count of homozygous individuals in female samples of East Asian ancestry in the non_neuro subset |
| AC_asj_male | Integer | Alternate allele count for male samples of Ashkenazi Jewish ancestry |
| AN_asj_male | Integer | Total number of alleles in male samples of Ashkenazi Jewish ancestry |
| AF_asj_male | Float | Alternate allele frequency in male samples of Ashkenazi Jewish ancestry |
| nhomalt_asj_male | Integer | Count of homozygous individuals in male samples of Ashkenazi Jewish ancestry |
| controls_AC_nfe_male | Integer | Alternate allele count for male samples of Non-Finnish European ancestry in the controls subset |
| controls_AN_nfe_male | Integer | Total number of alleles in male samples of Non-Finnish European ancestry in the controls subset |
| controls_AF_nfe_male | Float | Alternate allele frequency in male samples of Non-Finnish European ancestry in the controls subset |
| controls_nhomalt_nfe_male | Integer | Count of homozygous individuals in male samples of Non-Finnish European ancestry in the controls subset |
| non_neuro_AC_fin | Integer | Alternate allele count for samples of Finnish ancestry in the non_neuro subset |
| non_neuro_AN_fin | Integer | Total number of alleles in samples of Finnish ancestry in the non_neuro subset |
| non_neuro_AF_fin | Float | Alternate allele frequency in samples of Finnish ancestry in the non_neuro subset |
| non_neuro_nhomalt_fin | Integer | Count of homozygous individuals in samples of Finnish ancestry in the non_neuro subset |
| non_topmed_AC_sas | Integer | Alternate allele count for samples of South Asian ancestry in the non_topmed subset |
| non_topmed_AN_sas | Integer | Total number of alleles in samples of South Asian ancestry in the non_topmed subset |
| non_topmed_AF_sas | Float | Alternate allele frequency in samples of South Asian ancestry in the non_topmed subset |
| non_topmed_nhomalt_sas | Integer | Count of homozygous individuals in samples of South Asian ancestry in the non_topmed subset |
| non_cancer_AC_nfe_female | Integer | Alternate allele count for female samples of Non-Finnish European ancestry in the non_cancer subset |
| non_cancer_AN_nfe_female | Integer | Total number of alleles in female samples of Non-Finnish European ancestry in the non_cancer subset |
| non_cancer_AF_nfe_female | Float | Alternate allele frequency in female samples of Non-Finnish European ancestry in the non_cancer subset |
| non_cancer_nhomalt_nfe_female | Integer | Count of homozygous individuals in female samples of Non-Finnish European ancestry in the non_cancer subset |
| AC_oth_female | Integer | Alternate allele count for female samples of Other ancestry |
| AN_oth_female | Integer | Total number of alleles in female samples of Other ancestry |
| AF_oth_female | Float | Alternate allele frequency in female samples of Other ancestry |
| nhomalt_oth_female | Integer | Count of homozygous individuals in female samples of Other ancestry |
| non_cancer_AC_asj | Integer | Alternate allele count for samples of Ashkenazi Jewish ancestry in the non_cancer subset |
| non_cancer_AN_asj | Integer | Total number of alleles in samples of Ashkenazi Jewish ancestry in the non_cancer subset |
| non_cancer_AF_asj | Float | Alternate allele frequency in samples of Ashkenazi Jewish ancestry in the non_cancer subset |
| non_cancer_nhomalt_asj | Integer | Count of homozygous individuals in samples of Ashkenazi Jewish ancestry in the non_cancer subset |
| AC_nfe_swe | Integer | Alternate allele count for samples of Swedish ancestry |
| AN_nfe_swe | Integer | Total number of alleles in samples of Swedish ancestry |
| AF_nfe_swe | Float | Alternate allele frequency in samples of Swedish ancestry |
| nhomalt_nfe_swe | Integer | Count of homozygous individuals in samples of Swedish ancestry |
| controls_AC_nfe | Integer | Alternate allele count for samples of Non-Finnish European ancestry in the controls subset |
| controls_AN_nfe | Integer | Total number of alleles in samples of Non-Finnish European ancestry in the controls subset |
| controls_AF_nfe | Float | Alternate allele frequency in samples of Non-Finnish European ancestry in the controls subset |
| controls_nhomalt_nfe | Integer | Count of homozygous individuals in samples of Non-Finnish European ancestry in the controls subset |
| controls_AC_oth_female | Integer | Alternate allele count for female samples of Other ancestry in the controls subset |
| controls_AN_oth_female | Integer | Total number of alleles in female samples of Other ancestry in the controls subset |
| controls_AF_oth_female | Float | Alternate allele frequency in female samples of Other ancestry in the controls subset |
| controls_nhomalt_oth_female | Integer | Count of homozygous individuals in female samples of Other ancestry in the controls subset |
| controls_AC_asj | Integer | Alternate allele count for samples of Ashkenazi Jewish ancestry in the controls subset |
| controls_AN_asj | Integer | Total number of alleles in samples of Ashkenazi Jewish ancestry in the controls subset |
| controls_AF_asj | Float | Alternate allele frequency in samples of Ashkenazi Jewish ancestry in the controls subset |
| controls_nhomalt_asj | Integer | Count of homozygous individuals in samples of Ashkenazi Jewish ancestry in the controls subset |
| non_neuro_AC_amr_male | Integer | Alternate allele count for male samples of Latino ancestry in the non_neuro subset |
| non_neuro_AN_amr_male | Integer | Total number of alleles in male samples of Latino ancestry in the non_neuro subset |
| non_neuro_AF_amr_male | Float | Alternate allele frequency in male samples of Latino ancestry in the non_neuro subset |
| non_neuro_nhomalt_amr_male | Integer | Count of homozygous individuals in male samples of Latino ancestry in the non_neuro subset |
| controls_AC_nfe_nwe | Integer | Alternate allele count for samples of North-Western European ancestry in the controls subset |
| controls_AN_nfe_nwe | Integer | Total number of alleles in samples of North-Western European ancestry in the controls subset |
| controls_AF_nfe_nwe | Float | Alternate allele frequency in samples of North-Western European ancestry in the controls subset |
| controls_nhomalt_nfe_nwe | Integer | Count of homozygous individuals in samples of North-Western European ancestry in the controls subset |
| AC_nfe_nwe | Integer | Alternate allele count for samples of North-Western European ancestry |
| AN_nfe_nwe | Integer | Total number of alleles in samples of North-Western European ancestry |
| AF_nfe_nwe | Float | Alternate allele frequency in samples of North-Western European ancestry |
| nhomalt_nfe_nwe | Integer | Count of homozygous individuals in samples of North-Western European ancestry |
| controls_AC_nfe_seu | Integer | Alternate allele count for samples of Southern European ancestry in the controls subset |
| controls_AN_nfe_seu | Integer | Total number of alleles in samples of Southern European ancestry in the controls subset |
| controls_AF_nfe_seu | Float | Alternate allele frequency in samples of Southern European ancestry in the controls subset |
| controls_nhomalt_nfe_seu | Integer | Count of homozygous individuals in samples of Southern European ancestry in the controls subset |
| controls_AC_sas_female | Integer | Alternate allele count for female samples of South Asian ancestry in the controls subset |
| controls_AN_sas_female | Integer | Total number of alleles in female samples of South Asian ancestry in the controls subset |
| controls_AF_sas_female | Float | Alternate allele frequency in female samples of South Asian ancestry in the controls subset |
| controls_nhomalt_sas_female | Integer | Count of homozygous individuals in female samples of South Asian ancestry in the controls subset |
| non_neuro_AC_amr_female | Integer | Alternate allele count for female samples of Latino ancestry in the non_neuro subset |
| non_neuro_AN_amr_female | Integer | Total number of alleles in female samples of Latino ancestry in the non_neuro subset |
| non_neuro_AF_amr_female | Float | Alternate allele frequency in female samples of Latino ancestry in the non_neuro subset |
| non_neuro_nhomalt_amr_female | Integer | Count of homozygous individuals in female samples of Latino ancestry in the non_neuro subset |
| non_cancer_AC_eas_jpn | Integer | Alternate allele count for samples of Japanese ancestry in the non_cancer subset |
| non_cancer_AN_eas_jpn | Integer | Total number of alleles in samples of Japanese ancestry in the non_cancer subset |
| non_cancer_AF_eas_jpn | Float | Alternate allele frequency in samples of Japanese ancestry in the non_cancer subset |
| non_cancer_nhomalt_eas_jpn | Integer | Count of homozygous individuals in samples of Japanese ancestry in the non_cancer subset |
| non_neuro_AC_nfe_onf | Integer | Alternate allele count for samples of Other Non-Finnish European ancestry in the non_neuro subset |
| non_neuro_AN_nfe_onf | Integer | Total number of alleles in samples of Other Non-Finnish European ancestry in the non_neuro subset |
| non_neuro_AF_nfe_onf | Float | Alternate allele frequency in samples of Other Non-Finnish European ancestry in the non_neuro subset |
| non_neuro_nhomalt_nfe_onf | Integer | Count of homozygous individuals in samples of Other Non-Finnish European ancestry in the non_neuro subset |
| non_topmed_AC_eas_male | Integer | Alternate allele count for male samples of East Asian ancestry in the non_topmed subset |
| non_topmed_AN_eas_male | Integer | Total number of alleles in male samples of East Asian ancestry in the non_topmed subset |
| non_topmed_AF_eas_male | Float | Alternate allele frequency in male samples of East Asian ancestry in the non_topmed subset |
| non_topmed_nhomalt_eas_male | Integer | Count of homozygous individuals in male samples of East Asian ancestry in the non_topmed subset |
| AC_eas_jpn | Integer | Alternate allele count for samples of Japanese ancestry |
| AN_eas_jpn | Integer | Total number of alleles in samples of Japanese ancestry |
| AF_eas_jpn | Float | Alternate allele frequency in samples of Japanese ancestry |
| nhomalt_eas_jpn | Integer | Count of homozygous individuals in samples of Japanese ancestry |
| non_cancer_AC_afr_male | Integer | Alternate allele count for male samples of African-American/African ancestry in the non_cancer subset |
| non_cancer_AN_afr_male | Integer | Total number of alleles in male samples of African-American/African ancestry in the non_cancer subset |
| non_cancer_AF_afr_male | Float | Alternate allele frequency in male samples of African-American/African ancestry in the non_cancer subset |
| non_cancer_nhomalt_afr_male | Integer | Count of homozygous individuals in male samples of African-American/African ancestry in the non_cancer subset |
| non_cancer_AC_afr | Integer | Alternate allele count for samples of African-American/African ancestry in the non_cancer subset |
| non_cancer_AN_afr | Integer | Total number of alleles in samples of African-American/African ancestry in the non_cancer subset |
| non_cancer_AF_afr | Float | Alternate allele frequency in samples of African-American/African ancestry in the non_cancer subset |
| non_cancer_nhomalt_afr | Integer | Count of homozygous individuals in samples of African-American/African ancestry in the non_cancer subset |
| controls_AC_amr_female | Integer | Alternate allele count for female samples of Latino ancestry in the controls subset |
| controls_AN_amr_female | Integer | Total number of alleles in female samples of Latino ancestry in the controls subset |
| controls_AF_amr_female | Float | Alternate allele frequency in female samples of Latino ancestry in the controls subset |
| controls_nhomalt_amr_female | Integer | Count of homozygous individuals in female samples of Latino ancestry in the controls subset |
| non_neuro_AC_fin_male | Integer | Alternate allele count for male samples of Finnish ancestry in the non_neuro subset |
| non_neuro_AN_fin_male | Integer | Total number of alleles in male samples of Finnish ancestry in the non_neuro subset |
| non_neuro_AF_fin_male | Float | Alternate allele frequency in male samples of Finnish ancestry in the non_neuro subset |
| non_neuro_nhomalt_fin_male | Integer | Count of homozygous individuals in male samples of Finnish ancestry in the non_neuro subset |
| AC_female | Integer | Alternate allele count for female samples |
| AN_female | Integer | Total number of alleles in female samples |
| AF_female | Float | Alternate allele frequency in female samples |
| nhomalt_female | Integer | Count of homozygous individuals in female samples |
| non_neuro_AC_nfe_bgr | Integer | Alternate allele count for samples of Bulgarian (Eastern European) ancestry in the non_neuro subset |
| non_neuro_AN_nfe_bgr | Integer | Total number of alleles in samples of Bulgarian (Eastern European) ancestry in the non_neuro subset |
| non_neuro_AF_nfe_bgr | Float | Alternate allele frequency in samples of Bulgarian (Eastern European) ancestry in the non_neuro subset |
| non_neuro_nhomalt_nfe_bgr | Integer | Count of homozygous individuals in samples of Bulgarian (Eastern European) ancestry in the non_neuro subset |
| non_neuro_AC_oth_male | Integer | Alternate allele count for male samples of Other ancestry in the non_neuro subset |
| non_neuro_AN_oth_male | Integer | Total number of alleles in male samples of Other ancestry in the non_neuro subset |
| non_neuro_AF_oth_male | Float | Alternate allele frequency in male samples of Other ancestry in the non_neuro subset |
| non_neuro_nhomalt_oth_male | Integer | Count of homozygous individuals in male samples of Other ancestry in the non_neuro subset |
| non_topmed_AC_nfe_est | Integer | Alternate allele count for samples of Estonian ancestry in the non_topmed subset |
| non_topmed_AN_nfe_est | Integer | Total number of alleles in samples of Estonian ancestry in the non_topmed subset |
| non_topmed_AF_nfe_est | Float | Alternate allele frequency in samples of Estonian ancestry in the non_topmed subset |
| non_topmed_nhomalt_nfe_est | Integer | Count of homozygous individuals in samples of Estonian ancestry in the non_topmed subset |
| non_topmed_AC_nfe_nwe | Integer | Alternate allele count for samples of North-Western European ancestry in the non_topmed subset |
| non_topmed_AN_nfe_nwe | Integer | Total number of alleles in samples of North-Western European ancestry in the non_topmed subset |
| non_topmed_AF_nfe_nwe | Float | Alternate allele frequency in samples of North-Western European ancestry in the non_topmed subset |
| non_topmed_nhomalt_nfe_nwe | Integer | Count of homozygous individuals in samples of North-Western European ancestry in the non_topmed subset |
| non_topmed_AC_amr_male | Integer | Alternate allele count for male samples of Latino ancestry in the non_topmed subset |
| non_topmed_AN_amr_male | Integer | Total number of alleles in male samples of Latino ancestry in the non_topmed subset |
| non_topmed_AF_amr_male | Float | Alternate allele frequency in male samples of Latino ancestry in the non_topmed subset |
| non_topmed_nhomalt_amr_male | Integer | Count of homozygous individuals in male samples of Latino ancestry in the non_topmed subset |
| non_cancer_AC_amr | Integer | Alternate allele count for samples of Latino ancestry in the non_cancer subset |
| non_cancer_AN_amr | Integer | Total number of alleles in samples of Latino ancestry in the non_cancer subset |
| non_cancer_AF_amr | Float | Alternate allele frequency in samples of Latino ancestry in the non_cancer subset |
| non_cancer_nhomalt_amr | Integer | Count of homozygous individuals in samples of Latino ancestry in the non_cancer subset |
| non_topmed_AC_nfe_swe | Integer | Alternate allele count for samples of Swedish ancestry in the non_topmed subset |
| non_topmed_AN_nfe_swe | Integer | Total number of alleles in samples of Swedish ancestry in the non_topmed subset |
| non_topmed_AF_nfe_swe | Float | Alternate allele frequency in samples of Swedish ancestry in the non_topmed subset |
| non_topmed_nhomalt_nfe_swe | Integer | Count of homozygous individuals in samples of Swedish ancestry in the non_topmed subset |
| non_topmed_AC_nfe_onf | Integer | Alternate allele count for samples of Other Non-Finnish European ancestry in the non_topmed subset |
| non_topmed_AN_nfe_onf | Integer | Total number of alleles in samples of Other Non-Finnish European ancestry in the non_topmed subset |
| non_topmed_AF_nfe_onf | Float | Alternate allele frequency in samples of Other Non-Finnish European ancestry in the non_topmed subset |
| non_topmed_nhomalt_nfe_onf | Integer | Count of homozygous individuals in samples of Other Non-Finnish European ancestry in the non_topmed subset |
| controls_AC_eas_kor | Integer | Alternate allele count for samples of Korean ancestry in the controls subset |
| controls_AN_eas_kor | Integer | Total number of alleles in samples of Korean ancestry in the controls subset |
| controls_AF_eas_kor | Float | Alternate allele frequency in samples of Korean ancestry in the controls subset |
| controls_nhomalt_eas_kor | Integer | Count of homozygous individuals in samples of Korean ancestry in the controls subset |
| non_topmed_AC_eas_oea | Integer | Alternate allele count for samples of Other East Asian ancestry in the non_topmed subset |
| non_topmed_AN_eas_oea | Integer | Total number of alleles in samples of Other East Asian ancestry in the non_topmed subset |
| non_topmed_AF_eas_oea | Float | Alternate allele frequency in samples of Other East Asian ancestry in the non_topmed subset |
| non_topmed_nhomalt_eas_oea | Integer | Count of homozygous individuals in samples of Other East Asian ancestry in the non_topmed subset |
| controls_AC_eas_male | Integer | Alternate allele count for male samples of East Asian ancestry in the controls subset |
| controls_AN_eas_male | Integer | Total number of alleles in male samples of East Asian ancestry in the controls subset |
| controls_AF_eas_male | Float | Alternate allele frequency in male samples of East Asian ancestry in the controls subset |
| controls_nhomalt_eas_male | Integer | Count of homozygous individuals in male samples of East Asian ancestry in the controls subset |
| controls_AC_oth_male | Integer | Alternate allele count for male samples of Other ancestry in the controls subset |
| controls_AN_oth_male | Integer | Total number of alleles in male samples of Other ancestry in the controls subset |
| controls_AF_oth_male | Float | Alternate allele frequency in male samples of Other ancestry in the controls subset |
| controls_nhomalt_oth_male | Integer | Count of homozygous individuals in male samples of Other ancestry in the controls subset |
| non_topmed_AC | Integer | Alternate allele count for samples in the non_topmed subset |
| non_topmed_AN | Integer | Total number of alleles in samples in the non_topmed subset |
| non_topmed_AF | Float | Alternate allele frequency in samples in the non_topmed subset |
| non_topmed_nhomalt | Integer | Count of homozygous individuals in samples in the non_topmed subset |
| controls_AC_fin | Integer | Alternate allele count for samples of Finnish ancestry in the controls subset |
| controls_AN_fin | Integer | Total number of alleles in samples of Finnish ancestry in the controls subset |
| controls_AF_fin | Float | Alternate allele frequency in samples of Finnish ancestry in the controls subset |
| controls_nhomalt_fin | Integer | Count of homozygous individuals in samples of Finnish ancestry in the controls subset |
| AC_eas_kor | Integer | Alternate allele count for samples of Korean ancestry |
| AN_eas_kor | Integer | Total number of alleles in samples of Korean ancestry |
| AF_eas_kor | Float | Alternate allele frequency in samples of Korean ancestry |
| nhomalt_eas_kor | Integer | Count of homozygous individuals in samples of Korean ancestry |
| non_neuro_AC_nfe | Integer | Alternate allele count for samples of Non-Finnish European ancestry in the non_neuro subset |
| non_neuro_AN_nfe | Integer | Total number of alleles in samples of Non-Finnish European ancestry in the non_neuro subset |
| non_neuro_AF_nfe | Float | Alternate allele frequency in samples of Non-Finnish European ancestry in the non_neuro subset |
| non_neuro_nhomalt_nfe | Integer | Count of homozygous individuals in samples of Non-Finnish European ancestry in the non_neuro subset |
| non_neuro_AC_fin_female | Integer | Alternate allele count for female samples of Finnish ancestry in the non_neuro subset |
| non_neuro_AN_fin_female | Integer | Total number of alleles in female samples of Finnish ancestry in the non_neuro subset |
| non_neuro_AF_fin_female | Float | Alternate allele frequency in female samples of Finnish ancestry in the non_neuro subset |
| non_neuro_nhomalt_fin_female | Integer | Count of homozygous individuals in female samples of Finnish ancestry in the non_neuro subset |
| non_cancer_AC_nfe_male | Integer | Alternate allele count for male samples of Non-Finnish European ancestry in the non_cancer subset |
| non_cancer_AN_nfe_male | Integer | Total number of alleles in male samples of Non-Finnish European ancestry in the non_cancer subset |
| non_cancer_AF_nfe_male | Float | Alternate allele frequency in male samples of Non-Finnish European ancestry in the non_cancer subset |
| non_cancer_nhomalt_nfe_male | Integer | Count of homozygous individuals in male samples of Non-Finnish European ancestry in the non_cancer subset |
| controls_AC_eas_oea | Integer | Alternate allele count for samples of Other East Asian ancestry in the controls subset |
| controls_AN_eas_oea | Integer | Total number of alleles in samples of Other East Asian ancestry in the controls subset |
| controls_AF_eas_oea | Float | Alternate allele frequency in samples of Other East Asian ancestry in the controls subset |
| controls_nhomalt_eas_oea | Integer | Count of homozygous individuals in samples of Other East Asian ancestry in the controls subset |
| non_topmed_AC_nfe_seu | Integer | Alternate allele count for samples of Southern European ancestry in the non_topmed subset |
| non_topmed_AN_nfe_seu | Integer | Total number of alleles in samples of Southern European ancestry in the non_topmed subset |
| non_topmed_AF_nfe_seu | Float | Alternate allele frequency in samples of Southern European ancestry in the non_topmed subset |
| non_topmed_nhomalt_nfe_seu | Integer | Count of homozygous individuals in samples of Southern European ancestry in the non_topmed subset |
| controls_AC_eas_female | Integer | Alternate allele count for female samples of East Asian ancestry in the controls subset |
| controls_AN_eas_female | Integer | Total number of alleles in female samples of East Asian ancestry in the controls subset |
| controls_AF_eas_female | Float | Alternate allele frequency in female samples of East Asian ancestry in the controls subset |
| controls_nhomalt_eas_female | Integer | Count of homozygous individuals in female samples of East Asian ancestry in the controls subset |
| non_topmed_AC_asj | Integer | Alternate allele count for samples of Ashkenazi Jewish ancestry in the non_topmed subset |
| non_topmed_AN_asj | Integer | Total number of alleles in samples of Ashkenazi Jewish ancestry in the non_topmed subset |
| non_topmed_AF_asj | Float | Alternate allele frequency in samples of Ashkenazi Jewish ancestry in the non_topmed subset |
| non_topmed_nhomalt_asj | Integer | Count of homozygous individuals in samples of Ashkenazi Jewish ancestry in the non_topmed subset |
| controls_AC_nfe_onf | Integer | Alternate allele count for samples of Other Non-Finnish European ancestry in the controls subset |
| controls_AN_nfe_onf | Integer | Total number of alleles in samples of Other Non-Finnish European ancestry in the controls subset |
| controls_AF_nfe_onf | Float | Alternate allele frequency in samples of Other Non-Finnish European ancestry in the controls subset |
| controls_nhomalt_nfe_onf | Integer | Count of homozygous individuals in samples of Other Non-Finnish European ancestry in the controls subset |
| non_neuro_AC | Integer | Alternate allele count for samples in the non_neuro subset |
| non_neuro_AN | Integer | Total number of alleles in samples in the non_neuro subset |
| non_neuro_AF | Float | Alternate allele frequency in samples in the non_neuro subset |
| non_neuro_nhomalt | Integer | Count of homozygous individuals in samples in the non_neuro subset |
| AC_eas_oea | Integer | Alternate allele count for samples of Other East Asian ancestry |
| AN_eas_oea | Integer | Total number of alleles in samples of Other East Asian ancestry |
| AF_eas_oea | Float | Alternate allele frequency in samples of Other East Asian ancestry |
| nhomalt_eas_oea | Integer | Count of homozygous individuals in samples of Other East Asian ancestry |
| non_topmed_AC_nfe | Integer | Alternate allele count for samples of Non-Finnish European ancestry in the non_topmed subset |
| non_topmed_AN_nfe | Integer | Total number of alleles in samples of Non-Finnish European ancestry in the non_topmed subset |
| non_topmed_AF_nfe | Float | Alternate allele frequency in samples of Non-Finnish European ancestry in the non_topmed subset |
| non_topmed_nhomalt_nfe | Integer | Count of homozygous individuals in samples of Non-Finnish European ancestry in the non_topmed subset |
| non_cancer_AC_oth | Integer | Alternate allele count for samples of Other ancestry in the non_cancer subset |
| non_cancer_AN_oth | Integer | Total number of alleles in samples of Other ancestry in the non_cancer subset |
| non_cancer_AF_oth | Float | Alternate allele frequency in samples of Other ancestry in the non_cancer subset |
| non_cancer_nhomalt_oth | Integer | Count of homozygous individuals in samples of Other ancestry in the non_cancer subset |
| non_topmed_AC_raw | Integer | Alternate allele count for samples in the non_topmed subset
| non_topmed_AN_raw | Integer | Total number of alleles in samples in the non_topmed subset
| non_topmed_AF_raw | Float | Alternate allele frequency in samples in the non_topmed subset
| non_topmed_nhomalt_raw | Integer | Count of homozygous individuals in samples in the non_topmed subset
| non_neuro_AC_nfe_est | Integer | Alternate allele count for samples of Estonian ancestry in the non_neuro subset |
| non_neuro_AN_nfe_est | Integer | Total number of alleles in samples of Estonian ancestry in the non_neuro subset |
| non_neuro_AF_nfe_est | Float | Alternate allele frequency in samples of Estonian ancestry in the non_neuro subset |
| non_neuro_nhomalt_nfe_est | Integer | Count of homozygous individuals in samples of Estonian ancestry in the non_neuro subset |
| non_topmed_AC_oth_male | Integer | Alternate allele count for male samples of Other ancestry in the non_topmed subset |
| non_topmed_AN_oth_male | Integer | Total number of alleles in male samples of Other ancestry in the non_topmed subset |
| non_topmed_AF_oth_male | Float | Alternate allele frequency in male samples of Other ancestry in the non_topmed subset |
| non_topmed_nhomalt_oth_male | Integer | Count of homozygous individuals in male samples of Other ancestry in the non_topmed subset |
| non_cancer_AC_oth_male | Integer | Alternate allele count for male samples of Other ancestry in the non_cancer subset |
| non_cancer_AN_oth_male | Integer | Total number of alleles in male samples of Other ancestry in the non_cancer subset |
| non_cancer_AF_oth_male | Float | Alternate allele frequency in male samples of Other ancestry in the non_cancer subset |
| non_cancer_nhomalt_oth_male | Integer | Count of homozygous individuals in male samples of Other ancestry in the non_cancer subset |
| AC_nfe_est | Integer | Alternate allele count for samples of Estonian ancestry |
| AN_nfe_est | Integer | Total number of alleles in samples of Estonian ancestry |
| AF_nfe_est | Float | Alternate allele frequency in samples of Estonian ancestry |
| nhomalt_nfe_est | Integer | Count of homozygous individuals in samples of Estonian ancestry |
| non_cancer_AC_afr_female | Integer | Alternate allele count for female samples of African-American/African ancestry in the non_cancer subset |
| non_cancer_AN_afr_female | Integer | Total number of alleles in female samples of African-American/African ancestry in the non_cancer subset |
| non_cancer_AF_afr_female | Float | Alternate allele frequency in female samples of African-American/African ancestry in the non_cancer subset |
| non_cancer_nhomalt_afr_female | Integer | Count of homozygous individuals in female samples of African-American/African ancestry in the non_cancer subset |
| non_topmed_AC_afr_male | Integer | Alternate allele count for male samples of African-American/African ancestry in the non_topmed subset |
| non_topmed_AN_afr_male | Integer | Total number of alleles in male samples of African-American/African ancestry in the non_topmed subset |
| non_topmed_AF_afr_male | Float | Alternate allele frequency in male samples of African-American/African ancestry in the non_topmed subset |
| non_topmed_nhomalt_afr_male | Integer | Count of homozygous individuals in male samples of African-American/African ancestry in the non_topmed subset |
| AC_eas_male | Integer | Alternate allele count for male samples of East Asian ancestry |
| AN_eas_male | Integer | Total number of alleles in male samples of East Asian ancestry |
| AF_eas_male | Float | Alternate allele frequency in male samples of East Asian ancestry |
| nhomalt_eas_male | Integer | Count of homozygous individuals in male samples of East Asian ancestry |
| controls_AC_eas | Integer | Alternate allele count for samples of East Asian ancestry in the controls subset |
| controls_AN_eas | Integer | Total number of alleles in samples of East Asian ancestry in the controls subset |
| controls_AF_eas | Float | Alternate allele frequency in samples of East Asian ancestry in the controls subset |
| controls_nhomalt_eas | Integer | Count of homozygous individuals in samples of East Asian ancestry in the controls subset |
| non_neuro_AC_eas_male | Integer | Alternate allele count for male samples of East Asian ancestry in the non_neuro subset |
| non_neuro_AN_eas_male | Integer | Total number of alleles in male samples of East Asian ancestry in the non_neuro subset |
| non_neuro_AF_eas_male | Float | Alternate allele frequency in male samples of East Asian ancestry in the non_neuro subset |
| non_neuro_nhomalt_eas_male | Integer | Count of homozygous individuals in male samples of East Asian ancestry in the non_neuro subset |
| non_cancer_AC_nfe_nwe | Integer | Alternate allele count for samples of North-Western European ancestry in the non_cancer subset |
| non_cancer_AN_nfe_nwe | Integer | Total number of alleles in samples of North-Western European ancestry in the non_cancer subset |
| non_cancer_AF_nfe_nwe | Float | Alternate allele frequency in samples of North-Western European ancestry in the non_cancer subset |
| non_cancer_nhomalt_nfe_nwe | Integer | Count of homozygous individuals in samples of North-Western European ancestry in the non_cancer subset |
| controls_AC_sas | Integer | Alternate allele count for samples of South Asian ancestry in the controls subset |
| controls_AN_sas | Integer | Total number of alleles in samples of South Asian ancestry in the controls subset |
| controls_AF_sas | Float | Alternate allele frequency in samples of South Asian ancestry in the controls subset |
| controls_nhomalt_sas | Integer | Count of homozygous individuals in samples of South Asian ancestry in the controls subset |
| non_neuro_AC_sas_male | Integer | Alternate allele count for male samples of South Asian ancestry in the non_neuro subset |
| non_neuro_AN_sas_male | Integer | Total number of alleles in male samples of South Asian ancestry in the non_neuro subset |
| non_neuro_AF_sas_male | Float | Alternate allele frequency in male samples of South Asian ancestry in the non_neuro subset |
| non_neuro_nhomalt_sas_male | Integer | Count of homozygous individuals in male samples of South Asian ancestry in the non_neuro subset |
| non_neuro_AC_asj_male | Integer | Alternate allele count for male samples of Ashkenazi Jewish ancestry in the non_neuro subset |
| non_neuro_AN_asj_male | Integer | Total number of alleles in male samples of Ashkenazi Jewish ancestry in the non_neuro subset |
| non_neuro_AF_asj_male | Float | Alternate allele frequency in male samples of Ashkenazi Jewish ancestry in the non_neuro subset |
| non_neuro_nhomalt_asj_male | Integer | Count of homozygous individuals in male samples of Ashkenazi Jewish ancestry in the non_neuro subset |
| non_cancer_AC_nfe_bgr | Integer | Alternate allele count for samples of Bulgarian (Eastern European) ancestry in the non_cancer subset |
| non_cancer_AN_nfe_bgr | Integer | Total number of alleles in samples of Bulgarian (Eastern European) ancestry in the non_cancer subset |
| non_cancer_AF_nfe_bgr | Float | Alternate allele frequency in samples of Bulgarian (Eastern European) ancestry in the non_cancer subset |
| non_cancer_nhomalt_nfe_bgr | Integer | Count of homozygous individuals in samples of Bulgarian (Eastern European) ancestry in the non_cancer subset |
| controls_AC_oth | Integer | Alternate allele count for samples of Other ancestry in the controls subset |
| controls_AN_oth | Integer | Total number of alleles in samples of Other ancestry in the controls subset |
| controls_AF_oth | Float | Alternate allele frequency in samples of Other ancestry in the controls subset |
| controls_nhomalt_oth | Integer | Count of homozygous individuals in samples of Other ancestry in the controls subset |
| non_cancer_AC_eas_female | Integer | Alternate allele count for female samples of East Asian ancestry in the non_cancer subset |
| non_cancer_AN_eas_female | Integer | Total number of alleles in female samples of East Asian ancestry in the non_cancer subset |
| non_cancer_AF_eas_female | Float | Alternate allele frequency in female samples of East Asian ancestry in the non_cancer subset |
| non_cancer_nhomalt_eas_female | Integer | Count of homozygous individuals in female samples of East Asian ancestry in the non_cancer subset |
| AC_nfe | Integer | Alternate allele count for samples of Non-Finnish European ancestry |
| AN_nfe | Integer | Total number of alleles in samples of Non-Finnish European ancestry |
| AF_nfe | Float | Alternate allele frequency in samples of Non-Finnish European ancestry |
| nhomalt_nfe | Integer | Count of homozygous individuals in samples of Non-Finnish European ancestry |
| non_topmed_AC_female | Integer | Alternate allele count for female samples in the non_topmed subset |
| non_topmed_AN_female | Integer | Total number of alleles in female samples in the non_topmed subset |
| non_topmed_AF_female | Float | Alternate allele frequency in female samples in the non_topmed subset |
| non_topmed_nhomalt_female | Integer | Count of homozygous individuals in female samples in the non_topmed subset |
| non_neuro_AC_asj | Integer | Alternate allele count for samples of Ashkenazi Jewish ancestry in the non_neuro subset |
| non_neuro_AN_asj | Integer | Total number of alleles in samples of Ashkenazi Jewish ancestry in the non_neuro subset |
| non_neuro_AF_asj | Float | Alternate allele frequency in samples of Ashkenazi Jewish ancestry in the non_neuro subset |
| non_neuro_nhomalt_asj | Integer | Count of homozygous individuals in samples of Ashkenazi Jewish ancestry in the non_neuro subset |
| non_topmed_AC_eas_female | Integer | Alternate allele count for female samples of East Asian ancestry in the non_topmed subset |
| non_topmed_AN_eas_female | Integer | Total number of alleles in female samples of East Asian ancestry in the non_topmed subset |
| non_topmed_AF_eas_female | Float | Alternate allele frequency in female samples of East Asian ancestry in the non_topmed subset |
| non_topmed_nhomalt_eas_female | Integer | Count of homozygous individuals in female samples of East Asian ancestry in the non_topmed subset |
| non_neuro_AC_raw | Integer | Alternate allele count for samples in the non_neuro subset
| non_neuro_AN_raw | Integer | Total number of alleles in samples in the non_neuro subset
| non_neuro_AF_raw | Float | Alternate allele frequency in samples in the non_neuro subset
| non_neuro_nhomalt_raw | Integer | Count of homozygous individuals in samples in the non_neuro subset
| non_topmed_AC_eas | Integer | Alternate allele count for samples of East Asian ancestry in the non_topmed subset |
| non_topmed_AN_eas | Integer | Total number of alleles in samples of East Asian ancestry in the non_topmed subset |
| non_topmed_AF_eas | Float | Alternate allele frequency in samples of East Asian ancestry in the non_topmed subset |
| non_topmed_nhomalt_eas | Integer | Count of homozygous individuals in samples of East Asian ancestry in the non_topmed subset |
| non_topmed_AC_fin_male | Integer | Alternate allele count for male samples of Finnish ancestry in the non_topmed subset |
| non_topmed_AN_fin_male | Integer | Total number of alleles in male samples of Finnish ancestry in the non_topmed subset |
| non_topmed_AF_fin_male | Float | Alternate allele frequency in male samples of Finnish ancestry in the non_topmed subset |
| non_topmed_nhomalt_fin_male | Integer | Count of homozygous individuals in male samples of Finnish ancestry in the non_topmed subset |
| non_cancer_AC_asj_male | Integer | Alternate allele count for male samples of Ashkenazi Jewish ancestry in the non_cancer subset |
| non_cancer_AN_asj_male | Integer | Total number of alleles in male samples of Ashkenazi Jewish ancestry in the non_cancer subset |
| non_cancer_AF_asj_male | Float | Alternate allele frequency in male samples of Ashkenazi Jewish ancestry in the non_cancer subset |
| non_cancer_nhomalt_asj_male | Integer | Count of homozygous individuals in male samples of Ashkenazi Jewish ancestry in the non_cancer subset |
| AC_fin | Integer | Alternate allele count for samples of Finnish ancestry |
| AN_fin | Integer | Total number of alleles in samples of Finnish ancestry |
| AF_fin | Float | Alternate allele frequency in samples of Finnish ancestry |
| nhomalt_fin | Integer | Count of homozygous individuals in samples of Finnish ancestry |
| AC_nfe_male | Integer | Alternate allele count for male samples of Non-Finnish European ancestry |
| AN_nfe_male | Integer | Total number of alleles in male samples of Non-Finnish European ancestry |
| AF_nfe_male | Float | Alternate allele frequency in male samples of Non-Finnish European ancestry |
| nhomalt_nfe_male | Integer | Count of homozygous individuals in male samples of Non-Finnish European ancestry |
| non_topmed_AC_eas_kor | Integer | Alternate allele count for samples of Korean ancestry in the non_topmed subset |
| non_topmed_AN_eas_kor | Integer | Total number of alleles in samples of Korean ancestry in the non_topmed subset |
| non_topmed_AF_eas_kor | Float | Alternate allele frequency in samples of Korean ancestry in the non_topmed subset |
| non_topmed_nhomalt_eas_kor | Integer | Count of homozygous individuals in samples of Korean ancestry in the non_topmed subset |
| controls_AC_amr_male | Integer | Alternate allele count for male samples of Latino ancestry in the controls subset |
| controls_AN_amr_male | Integer | Total number of alleles in male samples of Latino ancestry in the controls subset |
| controls_AF_amr_male | Float | Alternate allele frequency in male samples of Latino ancestry in the controls subset |
| controls_nhomalt_amr_male | Integer | Count of homozygous individuals in male samples of Latino ancestry in the controls subset |
| non_neuro_AC_eas_oea | Integer | Alternate allele count for samples of Other East Asian ancestry in the non_neuro subset |
| non_neuro_AN_eas_oea | Integer | Total number of alleles in samples of Other East Asian ancestry in the non_neuro subset |
| non_neuro_AF_eas_oea | Float | Alternate allele frequency in samples of Other East Asian ancestry in the non_neuro subset |
| non_neuro_nhomalt_eas_oea | Integer | Count of homozygous individuals in samples of Other East Asian ancestry in the non_neuro subset |
| AC_sas_female | Integer | Alternate allele count for female samples of South Asian ancestry |
| AN_sas_female | Integer | Total number of alleles in female samples of South Asian ancestry |
| AF_sas_female | Float | Alternate allele frequency in female samples of South Asian ancestry |
| nhomalt_sas_female | Integer | Count of homozygous individuals in female samples of South Asian ancestry |
| controls_AC_afr_female | Integer | Alternate allele count for female samples of African-American/African ancestry in the controls subset |
| controls_AN_afr_female | Integer | Total number of alleles in female samples of African-American/African ancestry in the controls subset |
| controls_AF_afr_female | Float | Alternate allele frequency in female samples of African-American/African ancestry in the controls subset |
| controls_nhomalt_afr_female | Integer | Count of homozygous individuals in female samples of African-American/African ancestry in the controls subset |
| controls_AC_amr | Integer | Alternate allele count for samples of Latino ancestry in the controls subset |
| controls_AN_amr | Integer | Total number of alleles in samples of Latino ancestry in the controls subset |
| controls_AF_amr | Float | Alternate allele frequency in samples of Latino ancestry in the controls subset |
| controls_nhomalt_amr | Integer | Count of homozygous individuals in samples of Latino ancestry in the controls subset |
| non_topmed_AC_eas_jpn | Integer | Alternate allele count for samples of Japanese ancestry in the non_topmed subset |
| non_topmed_AN_eas_jpn | Integer | Total number of alleles in samples of Japanese ancestry in the non_topmed subset |
| non_topmed_AF_eas_jpn | Float | Alternate allele frequency in samples of Japanese ancestry in the non_topmed subset |
| non_topmed_nhomalt_eas_jpn | Integer | Count of homozygous individuals in samples of Japanese ancestry in the non_topmed subset |
| AC_asj_female | Integer | Alternate allele count for female samples of Ashkenazi Jewish ancestry |
| AN_asj_female | Integer | Total number of alleles in female samples of Ashkenazi Jewish ancestry |
| AF_asj_female | Float | Alternate allele frequency in female samples of Ashkenazi Jewish ancestry |
| nhomalt_asj_female | Integer | Count of homozygous individuals in female samples of Ashkenazi Jewish ancestry |
| non_topmed_AC_nfe_bgr | Integer | Alternate allele count for samples of Bulgarian (Eastern European) ancestry in the non_topmed subset |
| non_topmed_AN_nfe_bgr | Integer | Total number of alleles in samples of Bulgarian (Eastern European) ancestry in the non_topmed subset |
| non_topmed_AF_nfe_bgr | Float | Alternate allele frequency in samples of Bulgarian (Eastern European) ancestry in the non_topmed subset |
| non_topmed_nhomalt_nfe_bgr | Integer | Count of homozygous individuals in samples of Bulgarian (Eastern European) ancestry in the non_topmed subset |
| non_cancer_AC_nfe_est | Integer | Alternate allele count for samples of Estonian ancestry in the non_cancer subset |
| non_cancer_AN_nfe_est | Integer | Total number of alleles in samples of Estonian ancestry in the non_cancer subset |
| non_cancer_AF_nfe_est | Float | Alternate allele frequency in samples of Estonian ancestry in the non_cancer subset |
| non_cancer_nhomalt_nfe_est | Integer | Count of homozygous individuals in samples of Estonian ancestry in the non_cancer subset |
| non_neuro_AC_eas | Integer | Alternate allele count for samples of East Asian ancestry in the non_neuro subset |
| non_neuro_AN_eas | Integer | Total number of alleles in samples of East Asian ancestry in the non_neuro subset |
| non_neuro_AF_eas | Float | Alternate allele frequency in samples of East Asian ancestry in the non_neuro subset |
| non_neuro_nhomalt_eas | Integer | Count of homozygous individuals in samples of East Asian ancestry in the non_neuro subset |
| non_cancer_AC_nfe | Integer | Alternate allele count for samples of Non-Finnish European ancestry in the non_cancer subset |
| non_cancer_AN_nfe | Integer | Total number of alleles in samples of Non-Finnish European ancestry in the non_cancer subset |
| non_cancer_AF_nfe | Float | Alternate allele frequency in samples of Non-Finnish European ancestry in the non_cancer subset |
| non_cancer_nhomalt_nfe | Integer | Count of homozygous individuals in samples of Non-Finnish European ancestry in the non_cancer subset |
| non_neuro_AC_male | Integer | Alternate allele count for male samples in the non_neuro subset |
| non_neuro_AN_male | Integer | Total number of alleles in male samples in the non_neuro subset |
| non_neuro_AF_male | Float | Alternate allele frequency in male samples in the non_neuro subset |
| non_neuro_nhomalt_male | Integer | Count of homozygous individuals in male samples in the non_neuro subset |
| non_neuro_AC_sas_female | Integer | Alternate allele count for female samples of South Asian ancestry in the non_neuro subset |
| non_neuro_AN_sas_female | Integer | Total number of alleles in female samples of South Asian ancestry in the non_neuro subset |
| non_neuro_AF_sas_female | Float | Alternate allele frequency in female samples of South Asian ancestry in the non_neuro subset |
| non_neuro_nhomalt_sas_female | Integer | Count of homozygous individuals in female samples of South Asian ancestry in the non_neuro subset |
| AC_asj | Integer | Alternate allele count for samples of Ashkenazi Jewish ancestry |
| AN_asj | Integer | Total number of alleles in samples of Ashkenazi Jewish ancestry |
| AF_asj | Float | Alternate allele frequency in samples of Ashkenazi Jewish ancestry |
| nhomalt_asj | Integer | Count of homozygous individuals in samples of Ashkenazi Jewish ancestry |
| controls_AC_nfe_est | Integer | Alternate allele count for samples of Estonian ancestry in the controls subset |
| controls_AN_nfe_est | Integer | Total number of alleles in samples of Estonian ancestry in the controls subset |
| controls_AF_nfe_est | Float | Alternate allele frequency in samples of Estonian ancestry in the controls subset |
| controls_nhomalt_nfe_est | Integer | Count of homozygous individuals in samples of Estonian ancestry in the controls subset |
| non_topmed_AC_asj_female | Integer | Alternate allele count for female samples of Ashkenazi Jewish ancestry in the non_topmed subset |
| non_topmed_AN_asj_female | Integer | Total number of alleles in female samples of Ashkenazi Jewish ancestry in the non_topmed subset |
| non_topmed_AF_asj_female | Float | Alternate allele frequency in female samples of Ashkenazi Jewish ancestry in the non_topmed subset |
| non_topmed_nhomalt_asj_female | Integer | Count of homozygous individuals in female samples of Ashkenazi Jewish ancestry in the non_topmed subset |
| non_cancer_AC_nfe_swe | Integer | Alternate allele count for samples of Swedish ancestry in the non_cancer subset |
| non_cancer_AN_nfe_swe | Integer | Total number of alleles in samples of Swedish ancestry in the non_cancer subset |
| non_cancer_AF_nfe_swe | Float | Alternate allele frequency in samples of Swedish ancestry in the non_cancer subset |
| non_cancer_nhomalt_nfe_swe | Integer | Count of homozygous individuals in samples of Swedish ancestry in the non_cancer subset |
| non_cancer_AC | Integer | Alternate allele count for samples in the non_cancer subset |
| non_cancer_AN | Integer | Total number of alleles in samples in the non_cancer subset |
| non_cancer_AF | Float | Alternate allele frequency in samples in the non_cancer subset |
| non_cancer_nhomalt | Integer | Count of homozygous individuals in samples in the non_cancer subset |
| non_topmed_AC_oth | Integer | Alternate allele count for samples of Other ancestry in the non_topmed subset |
| non_topmed_AN_oth | Integer | Total number of alleles in samples of Other ancestry in the non_topmed subset |
| non_topmed_AF_oth | Float | Alternate allele frequency in samples of Other ancestry in the non_topmed subset |
| non_topmed_nhomalt_oth | Integer | Count of homozygous individuals in samples of Other ancestry in the non_topmed subset |
| non_topmed_AC_fin_female | Integer | Alternate allele count for female samples of Finnish ancestry in the non_topmed subset |
| non_topmed_AN_fin_female | Integer | Total number of alleles in female samples of Finnish ancestry in the non_topmed subset |
| non_topmed_AF_fin_female | Float | Alternate allele frequency in female samples of Finnish ancestry in the non_topmed subset |
| non_topmed_nhomalt_fin_female | Integer | Count of homozygous individuals in female samples of Finnish ancestry in the non_topmed subset |
| non_cancer_AC_fin_female | Integer | Alternate allele count for female samples of Finnish ancestry in the non_cancer subset |
| non_cancer_AN_fin_female | Integer | Total number of alleles in female samples of Finnish ancestry in the non_cancer subset |
| non_cancer_AF_fin_female | Float | Alternate allele frequency in female samples of Finnish ancestry in the non_cancer subset |
| non_cancer_nhomalt_fin_female | Integer | Count of homozygous individuals in female samples of Finnish ancestry in the non_cancer subset |
| AC_oth | Integer | Alternate allele count for samples of Other ancestry |
| AN_oth | Integer | Total number of alleles in samples of Other ancestry |
| AF_oth | Float | Alternate allele frequency in samples of Other ancestry |
| nhomalt_oth | Integer | Count of homozygous individuals in samples of Other ancestry |
| non_neuro_AC_nfe_male | Integer | Alternate allele count for male samples of Non-Finnish European ancestry in the non_neuro subset |
| non_neuro_AN_nfe_male | Integer | Total number of alleles in male samples of Non-Finnish European ancestry in the non_neuro subset |
| non_neuro_AF_nfe_male | Float | Alternate allele frequency in male samples of Non-Finnish European ancestry in the non_neuro subset |
| non_neuro_nhomalt_nfe_male | Integer | Count of homozygous individuals in male samples of Non-Finnish European ancestry in the non_neuro subset |
| controls_AC_female | Integer | Alternate allele count for female samples in the controls subset |
| controls_AN_female | Integer | Total number of alleles in female samples in the controls subset |
| controls_AF_female | Float | Alternate allele frequency in female samples in the controls subset |
| controls_nhomalt_female | Integer | Count of homozygous individuals in female samples in the controls subset |
| non_cancer_AC_fin | Integer | Alternate allele count for samples of Finnish ancestry in the non_cancer subset |
| non_cancer_AN_fin | Integer | Total number of alleles in samples of Finnish ancestry in the non_cancer subset |
| non_cancer_AF_fin | Float | Alternate allele frequency in samples of Finnish ancestry in the non_cancer subset |
| non_cancer_nhomalt_fin | Integer | Count of homozygous individuals in samples of Finnish ancestry in the non_cancer subset |
| non_topmed_AC_fin | Integer | Alternate allele count for samples of Finnish ancestry in the non_topmed subset |
| non_topmed_AN_fin | Integer | Total number of alleles in samples of Finnish ancestry in the non_topmed subset |
| non_topmed_AF_fin | Float | Alternate allele frequency in samples of Finnish ancestry in the non_topmed subset |
| non_topmed_nhomalt_fin | Integer | Count of homozygous individuals in samples of Finnish ancestry in the non_topmed subset |
| non_cancer_AC_eas_oea | Integer | Alternate allele count for samples of Other East Asian ancestry in the non_cancer subset |
| non_cancer_AN_eas_oea | Integer | Total number of alleles in samples of Other East Asian ancestry in the non_cancer subset |
| non_cancer_AF_eas_oea | Float | Alternate allele frequency in samples of Other East Asian ancestry in the non_cancer subset |
| non_cancer_nhomalt_eas_oea | Integer | Count of homozygous individuals in samples of Other East Asian ancestry in the non_cancer subset |
| non_topmed_AC_nfe_female | Integer | Alternate allele count for female samples of Non-Finnish European ancestry in the non_topmed subset |
| non_topmed_AN_nfe_female | Integer | Total number of alleles in female samples of Non-Finnish European ancestry in the non_topmed subset |
| non_topmed_AF_nfe_female | Float | Alternate allele frequency in female samples of Non-Finnish European ancestry in the non_topmed subset |
| non_topmed_nhomalt_nfe_female | Integer | Count of homozygous individuals in female samples of Non-Finnish European ancestry in the non_topmed subset |
| non_cancer_AC_sas_male | Integer | Alternate allele count for male samples of South Asian ancestry in the non_cancer subset |
| non_cancer_AN_sas_male | Integer | Total number of alleles in male samples of South Asian ancestry in the non_cancer subset |
| non_cancer_AF_sas_male | Float | Alternate allele frequency in male samples of South Asian ancestry in the non_cancer subset |
| non_cancer_nhomalt_sas_male | Integer | Count of homozygous individuals in male samples of South Asian ancestry in the non_cancer subset |
| controls_AC_asj_male | Integer | Alternate allele count for male samples of Ashkenazi Jewish ancestry in the controls subset |
| controls_AN_asj_male | Integer | Total number of alleles in male samples of Ashkenazi Jewish ancestry in the controls subset |
| controls_AF_asj_male | Float | Alternate allele frequency in male samples of Ashkenazi Jewish ancestry in the controls subset |
| controls_nhomalt_asj_male | Integer | Count of homozygous individuals in male samples of Ashkenazi Jewish ancestry in the controls subset |
| non_cancer_AC_raw | Integer | Alternate allele count for samples in the non_cancer subset
| non_cancer_AN_raw | Integer | Total number of alleles in samples in the non_cancer subset
| non_cancer_AF_raw | Float | Alternate allele frequency in samples in the non_cancer subset
| non_cancer_nhomalt_raw | Integer | Count of homozygous individuals in samples in the non_cancer subset
| non_cancer_AC_eas_male | Integer | Alternate allele count for male samples of East Asian ancestry in the non_cancer subset |
| non_cancer_AN_eas_male | Integer | Total number of alleles in male samples of East Asian ancestry in the non_cancer subset |
| non_cancer_AF_eas_male | Float | Alternate allele frequency in male samples of East Asian ancestry in the non_cancer subset |
| non_cancer_nhomalt_eas_male | Integer | Count of homozygous individuals in male samples of East Asian ancestry in the non_cancer subset |
| non_topmed_AC_asj_male | Integer | Alternate allele count for male samples of Ashkenazi Jewish ancestry in the non_topmed subset |
| non_topmed_AN_asj_male | Integer | Total number of alleles in male samples of Ashkenazi Jewish ancestry in the non_topmed subset |
| non_topmed_AF_asj_male | Float | Alternate allele frequency in male samples of Ashkenazi Jewish ancestry in the non_topmed subset |
| non_topmed_nhomalt_asj_male | Integer | Count of homozygous individuals in male samples of Ashkenazi Jewish ancestry in the non_topmed subset |
| non_neuro_AC_oth | Integer | Alternate allele count for samples of Other ancestry in the non_neuro subset |
| non_neuro_AN_oth | Integer | Total number of alleles in samples of Other ancestry in the non_neuro subset |
| non_neuro_AF_oth | Float | Alternate allele frequency in samples of Other ancestry in the non_neuro subset |
| non_neuro_nhomalt_oth | Integer | Count of homozygous individuals in samples of Other ancestry in the non_neuro subset |
| AC_male | Integer | Alternate allele count for male samples |
| AN_male | Integer | Total number of alleles in male samples |
| AF_male | Float | Alternate allele frequency in male samples |
| nhomalt_male | Integer | Count of homozygous individuals in male samples |
| controls_AC_fin_female | Integer | Alternate allele count for female samples of Finnish ancestry in the controls subset |
| controls_AN_fin_female | Integer | Total number of alleles in female samples of Finnish ancestry in the controls subset |
| controls_AF_fin_female | Float | Alternate allele frequency in female samples of Finnish ancestry in the controls subset |
| controls_nhomalt_fin_female | Integer | Count of homozygous individuals in female samples of Finnish ancestry in the controls subset |
| controls_AC_nfe_bgr | Integer | Alternate allele count for samples of Bulgarian (Eastern European) ancestry in the controls subset |
| controls_AN_nfe_bgr | Integer | Total number of alleles in samples of Bulgarian (Eastern European) ancestry in the controls subset |
| controls_AF_nfe_bgr | Float | Alternate allele frequency in samples of Bulgarian (Eastern European) ancestry in the controls subset |
| controls_nhomalt_nfe_bgr | Integer | Count of homozygous individuals in samples of Bulgarian (Eastern European) ancestry in the controls subset |
| controls_AC_asj_female | Integer | Alternate allele count for female samples of Ashkenazi Jewish ancestry in the controls subset |
| controls_AN_asj_female | Integer | Total number of alleles in female samples of Ashkenazi Jewish ancestry in the controls subset |
| controls_AF_asj_female | Float | Alternate allele frequency in female samples of Ashkenazi Jewish ancestry in the controls subset |
| controls_nhomalt_asj_female | Integer | Count of homozygous individuals in female samples of Ashkenazi Jewish ancestry in the controls subset |
| AC_amr_male | Integer | Alternate allele count for male samples of Latino ancestry |
| AN_amr_male | Integer | Total number of alleles in male samples of Latino ancestry |
| AF_amr_male | Float | Alternate allele frequency in male samples of Latino ancestry |
| nhomalt_amr_male | Integer | Count of homozygous individuals in male samples of Latino ancestry |
| AC_amr_female | Integer | Alternate allele count for female samples of Latino ancestry |
| AN_amr_female | Integer | Total number of alleles in female samples of Latino ancestry |
| AF_amr_female | Float | Alternate allele frequency in female samples of Latino ancestry |
| nhomalt_amr_female | Integer | Count of homozygous individuals in female samples of Latino ancestry |
| non_topmed_AC_sas_male | Integer | Alternate allele count for male samples of South Asian ancestry in the non_topmed subset |
| non_topmed_AN_sas_male | Integer | Total number of alleles in male samples of South Asian ancestry in the non_topmed subset |
| non_topmed_AF_sas_male | Float | Alternate allele frequency in male samples of South Asian ancestry in the non_topmed subset |
| non_topmed_nhomalt_sas_male | Integer | Count of homozygous individuals in male samples of South Asian ancestry in the non_topmed subset |
| AC_oth_male | Integer | Alternate allele count for male samples of Other ancestry |
| AN_oth_male | Integer | Total number of alleles in male samples of Other ancestry |
| AF_oth_male | Float | Alternate allele frequency in male samples of Other ancestry |
| nhomalt_oth_male | Integer | Count of homozygous individuals in male samples of Other ancestry |
| non_cancer_AC_sas | Integer | Alternate allele count for samples of South Asian ancestry in the non_cancer subset |
| non_cancer_AN_sas | Integer | Total number of alleles in samples of South Asian ancestry in the non_cancer subset |
| non_cancer_AF_sas | Float | Alternate allele frequency in samples of South Asian ancestry in the non_cancer subset |
| non_cancer_nhomalt_sas | Integer | Count of homozygous individuals in samples of South Asian ancestry in the non_cancer subset |
| non_neuro_AC_nfe_seu | Integer | Alternate allele count for samples of Southern European ancestry in the non_neuro subset |
| non_neuro_AN_nfe_seu | Integer | Total number of alleles in samples of Southern European ancestry in the non_neuro subset |
| non_neuro_AF_nfe_seu | Float | Alternate allele frequency in samples of Southern European ancestry in the non_neuro subset |
| non_neuro_nhomalt_nfe_seu | Integer | Count of homozygous individuals in samples of Southern European ancestry in the non_neuro subset |
| non_cancer_AC_eas_kor | Integer | Alternate allele count for samples of Korean ancestry in the non_cancer subset |
| non_cancer_AN_eas_kor | Integer | Total number of alleles in samples of Korean ancestry in the non_cancer subset |
| non_cancer_AF_eas_kor | Float | Alternate allele frequency in samples of Korean ancestry in the non_cancer subset |
| non_cancer_nhomalt_eas_kor | Integer | Count of homozygous individuals in samples of Korean ancestry in the non_cancer subset |
| non_topmed_AC_afr_female | Integer | Alternate allele count for female samples of African-American/African ancestry in the non_topmed subset |
| non_topmed_AN_afr_female | Integer | Total number of alleles in female samples of African-American/African ancestry in the non_topmed subset |
| non_topmed_AF_afr_female | Float | Alternate allele frequency in female samples of African-American/African ancestry in the non_topmed subset |
| non_topmed_nhomalt_afr_female | Integer | Count of homozygous individuals in female samples of African-American/African ancestry in the non_topmed subset |
| controls_AC_sas_male | Integer | Alternate allele count for male samples of South Asian ancestry in the controls subset |
| controls_AN_sas_male | Integer | Total number of alleles in male samples of South Asian ancestry in the controls subset |
| controls_AF_sas_male | Float | Alternate allele frequency in male samples of South Asian ancestry in the controls subset |
| controls_nhomalt_sas_male | Integer | Count of homozygous individuals in male samples of South Asian ancestry in the controls subset |
| non_topmed_AC_sas_female | Integer | Alternate allele count for female samples of South Asian ancestry in the non_topmed subset |
| non_topmed_AN_sas_female | Integer | Total number of alleles in female samples of South Asian ancestry in the non_topmed subset |
| non_topmed_AF_sas_female | Float | Alternate allele frequency in female samples of South Asian ancestry in the non_topmed subset |
| non_topmed_nhomalt_sas_female | Integer | Count of homozygous individuals in female samples of South Asian ancestry in the non_topmed subset |
| non_topmed_AC_afr | Integer | Alternate allele count for samples of African-American/African ancestry in the non_topmed subset |
| non_topmed_AN_afr | Integer | Total number of alleles in samples of African-American/African ancestry in the non_topmed subset |
| non_topmed_AF_afr | Float | Alternate allele frequency in samples of African-American/African ancestry in the non_topmed subset |
| non_topmed_nhomalt_afr | Integer | Count of homozygous individuals in samples of African-American/African ancestry in the non_topmed subset |
| controls_AC | Integer | Alternate allele count for samples in the controls subset |
| controls_AN | Integer | Total number of alleles in samples in the controls subset |
| controls_AF | Float | Alternate allele frequency in samples in the controls subset |
| controls_nhomalt | Integer | Count of homozygous individuals in samples in the controls subset |
| non_neuro_AC_oth_female | Integer | Alternate allele count for female samples of Other ancestry in the non_neuro subset |
| non_neuro_AN_oth_female | Integer | Total number of alleles in female samples of Other ancestry in the non_neuro subset |
| non_neuro_AF_oth_female | Float | Alternate allele frequency in female samples of Other ancestry in the non_neuro subset |
| non_neuro_nhomalt_oth_female | Integer | Count of homozygous individuals in female samples of Other ancestry in the non_neuro subset |
| non_topmed_faf95_amr | Float | Filtering allele frequency (using Poisson 95% CI) for samples of Latino ancestry in the non_topmed subset |
| non_topmed_faf99_amr | Float | Filtering allele frequency (using Poisson 99% CI) for samples of Latino ancestry in the non_topmed subset |
| faf95_afr | Float | Filtering allele frequency (using Poisson 95% CI) for samples of African-American/African ancestry |
| faf99_afr | Float | Filtering allele frequency (using Poisson 99% CI) for samples of African-American/African ancestry |
| faf95_sas | Float | Filtering allele frequency (using Poisson 95% CI) for samples of South Asian ancestry |
| faf99_sas | Float | Filtering allele frequency (using Poisson 99% CI) for samples of South Asian ancestry |
| controls_faf95_afr | Float | Filtering allele frequency (using Poisson 95% CI) for samples of African-American/African ancestry in the controls subset |
| controls_faf99_afr | Float | Filtering allele frequency (using Poisson 99% CI) for samples of African-American/African ancestry in the controls subset |
| faf95_amr | Float | Filtering allele frequency (using Poisson 95% CI) for samples of Latino ancestry |
| faf99_amr | Float | Filtering allele frequency (using Poisson 99% CI) for samples of Latino ancestry |
| non_neuro_faf95_sas | Float | Filtering allele frequency (using Poisson 95% CI) for samples of South Asian ancestry in the non_neuro subset |
| non_neuro_faf99_sas | Float | Filtering allele frequency (using Poisson 99% CI) for samples of South Asian ancestry in the non_neuro subset |
| faf95_eas | Float | Filtering allele frequency (using Poisson 95% CI) for samples of East Asian ancestry |
| faf99_eas | Float | Filtering allele frequency (using Poisson 99% CI) for samples of East Asian ancestry |
| faf95 | Float | Filtering allele frequency (using Poisson 95% CI) for samples |
| faf99 | Float | Filtering allele frequency (using Poisson 99% CI) for samples |
| non_neuro_faf95_afr | Float | Filtering allele frequency (using Poisson 95% CI) for samples of African-American/African ancestry in the non_neuro subset |
| non_neuro_faf99_afr | Float | Filtering allele frequency (using Poisson 99% CI) for samples of African-American/African ancestry in the non_neuro subset |
| non_cancer_faf95_eas | Float | Filtering allele frequency (using Poisson 95% CI) for samples of East Asian ancestry in the non_cancer subset |
| non_cancer_faf99_eas | Float | Filtering allele frequency (using Poisson 99% CI) for samples of East Asian ancestry in the non_cancer subset |
| non_neuro_faf95_amr | Float | Filtering allele frequency (using Poisson 95% CI) for samples of Latino ancestry in the non_neuro subset |
| non_neuro_faf99_amr | Float | Filtering allele frequency (using Poisson 99% CI) for samples of Latino ancestry in the non_neuro subset |
| non_topmed_faf95_sas | Float | Filtering allele frequency (using Poisson 95% CI) for samples of South Asian ancestry in the non_topmed subset |
| non_topmed_faf99_sas | Float | Filtering allele frequency (using Poisson 99% CI) for samples of South Asian ancestry in the non_topmed subset |
| controls_faf95_nfe | Float | Filtering allele frequency (using Poisson 95% CI) for samples of Non-Finnish European ancestry in the controls subset |
| controls_faf99_nfe | Float | Filtering allele frequency (using Poisson 99% CI) for samples of Non-Finnish European ancestry in the controls subset |
| non_cancer_faf95_afr | Float | Filtering allele frequency (using Poisson 95% CI) for samples of African-American/African ancestry in the non_cancer subset |
| non_cancer_faf99_afr | Float | Filtering allele frequency (using Poisson 99% CI) for samples of African-American/African ancestry in the non_cancer subset |
| non_cancer_faf95_amr | Float | Filtering allele frequency (using Poisson 95% CI) for samples of Latino ancestry in the non_cancer subset |
| non_cancer_faf99_amr | Float | Filtering allele frequency (using Poisson 99% CI) for samples of Latino ancestry in the non_cancer subset |
| non_topmed_faf95 | Float | Filtering allele frequency (using Poisson 95% CI) for samples in the non_topmed subset |
| non_topmed_faf99 | Float | Filtering allele frequency (using Poisson 99% CI) for samples in the non_topmed subset |
| non_neuro_faf95_nfe | Float | Filtering allele frequency (using Poisson 95% CI) for samples of Non-Finnish European ancestry in the non_neuro subset |
| non_neuro_faf99_nfe | Float | Filtering allele frequency (using Poisson 99% CI) for samples of Non-Finnish European ancestry in the non_neuro subset |
| non_neuro_faf95 | Float | Filtering allele frequency (using Poisson 95% CI) for samples in the non_neuro subset |
| non_neuro_faf99 | Float | Filtering allele frequency (using Poisson 99% CI) for samples in the non_neuro subset |
| non_topmed_faf95_nfe | Float | Filtering allele frequency (using Poisson 95% CI) for samples of Non-Finnish European ancestry in the non_topmed subset |
| non_topmed_faf99_nfe | Float | Filtering allele frequency (using Poisson 99% CI) for samples of Non-Finnish European ancestry in the non_topmed subset |
| controls_faf95_eas | Float | Filtering allele frequency (using Poisson 95% CI) for samples of East Asian ancestry in the controls subset |
| controls_faf99_eas | Float | Filtering allele frequency (using Poisson 99% CI) for samples of East Asian ancestry in the controls subset |
| controls_faf95_sas | Float | Filtering allele frequency (using Poisson 95% CI) for samples of South Asian ancestry in the controls subset |
| controls_faf99_sas | Float | Filtering allele frequency (using Poisson 99% CI) for samples of South Asian ancestry in the controls subset |
| faf95_nfe | Float | Filtering allele frequency (using Poisson 95% CI) for samples of Non-Finnish European ancestry |
| faf99_nfe | Float | Filtering allele frequency (using Poisson 99% CI) for samples of Non-Finnish European ancestry |
| non_topmed_faf95_eas | Float | Filtering allele frequency (using Poisson 95% CI) for samples of East Asian ancestry in the non_topmed subset |
| non_topmed_faf99_eas | Float | Filtering allele frequency (using Poisson 99% CI) for samples of East Asian ancestry in the non_topmed subset |
| controls_faf95_amr | Float | Filtering allele frequency (using Poisson 95% CI) for samples of Latino ancestry in the controls subset |
| controls_faf99_amr | Float | Filtering allele frequency (using Poisson 99% CI) for samples of Latino ancestry in the controls subset |
| non_neuro_faf95_eas | Float | Filtering allele frequency (using Poisson 95% CI) for samples of East Asian ancestry in the non_neuro subset |
| non_neuro_faf99_eas | Float | Filtering allele frequency (using Poisson 99% CI) for samples of East Asian ancestry in the non_neuro subset |
| non_cancer_faf95_nfe | Float | Filtering allele frequency (using Poisson 95% CI) for samples of Non-Finnish European ancestry in the non_cancer subset |
| non_cancer_faf99_nfe | Float | Filtering allele frequency (using Poisson 99% CI) for samples of Non-Finnish European ancestry in the non_cancer subset |
| non_cancer_faf95 | Float | Filtering allele frequency (using Poisson 95% CI) for samples in the non_cancer subset |
| non_cancer_faf99 | Float | Filtering allele frequency (using Poisson 99% CI) for samples in the non_cancer subset |
| non_cancer_faf95_sas | Float | Filtering allele frequency (using Poisson 95% CI) for samples of South Asian ancestry in the non_cancer subset |
| non_cancer_faf99_sas | Float | Filtering allele frequency (using Poisson 99% CI) for samples of South Asian ancestry in the non_cancer subset |
| non_topmed_faf95_afr | Float | Filtering allele frequency (using Poisson 95% CI) for samples of African-American/African ancestry in the non_topmed subset |
| non_topmed_faf99_afr | Float | Filtering allele frequency (using Poisson 99% CI) for samples of African-American/African ancestry in the non_topmed subset |
| controls_faf95 | Float | Filtering allele frequency (using Poisson 95% CI) for samples in the controls subset |
| controls_faf99 | Float | Filtering allele frequency (using Poisson 99% CI) for samples in the controls subset |
| popmax | String | Population with maximum AF |
| AC_popmax | Integer | Allele count in the population with the maximum AF |
| AN_popmax | Integer | Total number of alleles in the population with the maximum AF |
| AF_popmax | Float | Maximum allele frequency across populations (excluding samples of Ashkenazi
| nhomalt_popmax | Integer | Count of homozygous individuals in the population with the maximum allele frequency |
| age_hist_het_bin_freq | String | Histogram of ages of heterozygous individuals; bin edges are: 30.0|35.0|40.0|45.0|50.0|55.0|60.0|65.0|70.0|75.0|80.0; total number of individuals of any genotype bin: 2547|3423|4546|8487|10355|12693|11933|10534|8882|5991|4136|1935 |
| age_hist_het_n_smaller | Integer | Count of age values falling below lowest histogram bin edge for heterozygous individuals |
| age_hist_het_n_larger | Integer | Count of age values falling above highest histogram bin edge for heterozygous individuals |
| age_hist_hom_bin_freq | String | Histogram of ages of homozygous alternate individuals; bin edges are: 30.0|35.0|40.0|45.0|50.0|55.0|60.0|65.0|70.0|75.0|80.0; total number of individuals of any genotype bin: 2547|3423|4546|8487|10355|12693|11933|10534|8882|5991|4136|1935 |
| age_hist_hom_n_smaller | Integer | Count of age values falling below lowest histogram bin edge for homozygous alternate individuals |
| age_hist_hom_n_larger | Integer | Count of age values falling above highest histogram bin edge for homozygous alternate individuals |
| non_topmed_popmax | String | Population with maximum AF in the non_topmed subset |
| non_topmed_AC_popmax | Integer | Allele count in the population with the maximum AF in the non_topmed subset |
| non_topmed_AN_popmax | Integer | Total number of alleles in the population with the maximum AF in the non_topmed subset |
| non_topmed_AF_popmax | Float | Maximum allele frequency across populations (excluding samples of Ashkenazi
| non_topmed_nhomalt_popmax | Integer | Count of homozygous individuals in the population with the maximum allele frequency in the non_topmed subset |
| non_neuro_popmax | String | Population with maximum AF in the non_neuro subset |
| non_neuro_AC_popmax | Integer | Allele count in the population with the maximum AF in the non_neuro subset |
| non_neuro_AN_popmax | Integer | Total number of alleles in the population with the maximum AF in the non_neuro subset |
| non_neuro_AF_popmax | Float | Maximum allele frequency across populations (excluding samples of Ashkenazi
| non_neuro_nhomalt_popmax | Integer | Count of homozygous individuals in the population with the maximum allele frequency in the non_neuro subset |
| non_cancer_popmax | String | Population with maximum AF in the non_cancer subset |
| non_cancer_AC_popmax | Integer | Allele count in the population with the maximum AF in the non_cancer subset |
| non_cancer_AN_popmax | Integer | Total number of alleles in the population with the maximum AF in the non_cancer subset |
| non_cancer_AF_popmax | Float | Maximum allele frequency across populations (excluding samples of Ashkenazi
| non_cancer_nhomalt_popmax | Integer | Count of homozygous individuals in the population with the maximum allele frequency in the non_cancer subset |
| controls_popmax | String | Population with maximum AF in the controls subset |
| controls_AC_popmax | Integer | Allele count in the population with the maximum AF in the controls subset |
| controls_AN_popmax | Integer | Total number of alleles in the population with the maximum AF in the controls subset |
| controls_AF_popmax | Float | Maximum allele frequency across populations (excluding samples of Ashkenazi
| controls_nhomalt_popmax | Integer | Count of homozygous individuals in the population with the maximum allele frequency in the controls subset |


### gnomADv3 Filters ###

| Annotation | Value Type | Description |
|------------|------------|-------------|
| AC | Integer | Alternate allele count for samples |
| AN | Integer | Total number of alleles in samples |
| AF | Float | Alternate allele frequency in samples |
| non_par | Flag | Variant (on sex chromosome) falls outside a pseudoautosomal region |
| lcr | Flag | Variant falls within a low complexity region |
| variant_type | String | Variant type (snv, indel, multi-snv, multi-indel, or mixed) |
| n_alt_alleles | Integer | Total number of alternate alleles observed at variant locus |
| ReadPosRankSum | Float | Z-score from Wilcoxon rank sum test of alternate vs. reference read position bias |
| MQRankSum | Float | Z-score from Wilcoxon rank sum test of alternate vs. reference read mapping qualities |
| RAW_MQ | Float | (No description from gnomAD) |
| DP | Integer | Depth of informative coverage for each sample; reads with MQ=255 or with bad mates are filtered |
| MQ_DP | Integer | (No description from gnomAD) |
| VarDP | Integer | (No description from gnomAD) |
| MQ | Float | Root mean square of the mapping quality of reads across all samples |
| QD | Float | Variant call confidence normalized by depth of sample reads supporting a variant |
| FS | Float | Phred-scaled p-value of Fisher's exact test for strand bias |
| SB | Integer | (No description from gnomAD) |
| InbreedingCoeff | Float | Inbreeding coefficient as estimated from the genotype likelihoods per-sample when compared against the Hardy-Weinberg expectation |
| AS_VQSLOD | Float | Log-odds ratio of being a true variant versus being a false positive under the trained allele-specific VQSR Gaussian mixture model |
| NEGATIVE_TRAIN_SITE | Flag | Variant was used to build the negative training set of low-quality variants for VQSR |
| POSITIVE_TRAIN_SITE | Flag | Variant was used to build the positive training set of high-quality variants for VQSR |
| culprit | String | Worst-performing annotation in the VQSR Gaussian mixture model |
| SOR | Float | Strand bias estimated by the symmetric odds ratio test |
| AC_asj_female | Integer | Alternate allele count for female samples of Ashkenazi Jewish ancestry |
| AN_asj_female | Integer | Total number of alleles in female samples of Ashkenazi Jewish ancestry |
| AF_asj_female | Float | Alternate allele frequency in female samples of Ashkenazi Jewish ancestry |
| nhomalt_asj_female | Integer | Count of homozygous individuals in female samples of Ashkenazi Jewish ancestry |
| AC_eas_female | Integer | Alternate allele count for female samples of East Asian ancestry |
| AN_eas_female | Integer | Total number of alleles in female samples of East Asian ancestry |
| AF_eas_female | Float | Alternate allele frequency in female samples of East Asian ancestry |
| nhomalt_eas_female | Integer | Count of homozygous individuals in female samples of East Asian ancestry |
| AC_afr_male | Integer | Alternate allele count for male samples of African-American/African ancestry |
| AN_afr_male | Integer | Total number of alleles in male samples of African-American/African ancestry |
| AF_afr_male | Float | Alternate allele frequency in male samples of African-American/African ancestry |
| nhomalt_afr_male | Integer | Count of homozygous individuals in male samples of African-American/African ancestry |
| AC_female | Integer | Alternate allele count for female samples |
| AN_female | Integer | Total number of alleles in female samples |
| AF_female | Float | Alternate allele frequency in female samples |
| nhomalt_female | Integer | Count of homozygous individuals in female samples |
| AC_fin_male | Integer | Alternate allele count for male samples of Finnish ancestry |
| AN_fin_male | Integer | Total number of alleles in male samples of Finnish ancestry |
| AF_fin_male | Float | Alternate allele frequency in male samples of Finnish ancestry |
| nhomalt_fin_male | Integer | Count of homozygous individuals in male samples of Finnish ancestry |
| AC_oth_female | Integer | Alternate allele count for female samples of Other ancestry |
| AN_oth_female | Integer | Total number of alleles in female samples of Other ancestry |
| AF_oth_female | Float | Alternate allele frequency in female samples of Other ancestry |
| nhomalt_oth_female | Integer | Count of homozygous individuals in female samples of Other ancestry |
| AC_ami | Integer | Alternate allele count for samples of Amish ancestry |
| AN_ami | Integer | Total number of alleles in samples of Amish ancestry |
| AF_ami | Float | Alternate allele frequency in samples of Amish ancestry |
| nhomalt_ami | Integer | Count of homozygous individuals in samples of Amish ancestry |
| AC_oth | Integer | Alternate allele count for samples of Other ancestry |
| AN_oth | Integer | Total number of alleles in samples of Other ancestry |
| AF_oth | Float | Alternate allele frequency in samples of Other ancestry |
| nhomalt_oth | Integer | Count of homozygous individuals in samples of Other ancestry |
| AC_male | Integer | Alternate allele count for male samples |
| AN_male | Integer | Total number of alleles in male samples |
| AF_male | Float | Alternate allele frequency in male samples |
| nhomalt_male | Integer | Count of homozygous individuals in male samples |
| AC_ami_female | Integer | Alternate allele count for female samples of Amish ancestry |
| AN_ami_female | Integer | Total number of alleles in female samples of Amish ancestry |
| AF_ami_female | Float | Alternate allele frequency in female samples of Amish ancestry |
| nhomalt_ami_female | Integer | Count of homozygous individuals in female samples of Amish ancestry |
| AC_afr | Integer | Alternate allele count for samples of African-American/African ancestry |
| AN_afr | Integer | Total number of alleles in samples of African-American/African ancestry |
| AF_afr | Float | Alternate allele frequency in samples of African-American/African ancestry |
| nhomalt_afr | Integer | Count of homozygous individuals in samples of African-American/African ancestry |
| AC_eas_male | Integer | Alternate allele count for male samples of East Asian ancestry |
| AN_eas_male | Integer | Total number of alleles in male samples of East Asian ancestry |
| AF_eas_male | Float | Alternate allele frequency in male samples of East Asian ancestry |
| nhomalt_eas_male | Integer | Count of homozygous individuals in male samples of East Asian ancestry |
| AC_sas | Integer | Alternate allele count for samples of South Asian ancestry |
| AN_sas | Integer | Total number of alleles in samples of South Asian ancestry |
| AF_sas | Float | Alternate allele frequency in samples of South Asian ancestry |
| nhomalt_sas | Integer | Count of homozygous individuals in samples of South Asian ancestry |
| AC_nfe_female | Integer | Alternate allele count for female samples of Non-Finnish European ancestry |
| AN_nfe_female | Integer | Total number of alleles in female samples of Non-Finnish European ancestry |
| AF_nfe_female | Float | Alternate allele frequency in female samples of Non-Finnish European ancestry |
| nhomalt_nfe_female | Integer | Count of homozygous individuals in female samples of Non-Finnish European ancestry |
| AC_asj_male | Integer | Alternate allele count for male samples of Ashkenazi Jewish ancestry |
| AN_asj_male | Integer | Total number of alleles in male samples of Ashkenazi Jewish ancestry |
| AF_asj_male | Float | Alternate allele frequency in male samples of Ashkenazi Jewish ancestry |
| nhomalt_asj_male | Integer | Count of homozygous individuals in male samples of Ashkenazi Jewish ancestry |
| AC_raw | Integer | Alternate allele count for samples
| AN_raw | Integer | Total number of alleles in samples
| AF_raw | Float | Alternate allele frequency in samples
| nhomalt_raw | Integer | Count of homozygous individuals in samples
| AC_oth_male | Integer | Alternate allele count for male samples of Other ancestry |
| AN_oth_male | Integer | Total number of alleles in male samples of Other ancestry |
| AF_oth_male | Float | Alternate allele frequency in male samples of Other ancestry |
| nhomalt_oth_male | Integer | Count of homozygous individuals in male samples of Other ancestry |
| AC_nfe_male | Integer | Alternate allele count for male samples of Non-Finnish European ancestry |
| AN_nfe_male | Integer | Total number of alleles in male samples of Non-Finnish European ancestry |
| AF_nfe_male | Float | Alternate allele frequency in male samples of Non-Finnish European ancestry |
| nhomalt_nfe_male | Integer | Count of homozygous individuals in male samples of Non-Finnish European ancestry |
| AC_asj | Integer | Alternate allele count for samples of Ashkenazi Jewish ancestry |
| AN_asj | Integer | Total number of alleles in samples of Ashkenazi Jewish ancestry |
| AF_asj | Float | Alternate allele frequency in samples of Ashkenazi Jewish ancestry |
| nhomalt_asj | Integer | Count of homozygous individuals in samples of Ashkenazi Jewish ancestry |
| AC_amr_male | Integer | Alternate allele count for male samples of Latino ancestry |
| AN_amr_male | Integer | Total number of alleles in male samples of Latino ancestry |
| AF_amr_male | Float | Alternate allele frequency in male samples of Latino ancestry |
| nhomalt_amr_male | Integer | Count of homozygous individuals in male samples of Latino ancestry |
| nhomalt | Integer | Count of homozygous individuals in samples |
| AC_amr_female | Integer | Alternate allele count for female samples of Latino ancestry |
| AN_amr_female | Integer | Total number of alleles in female samples of Latino ancestry |
| AF_amr_female | Float | Alternate allele frequency in female samples of Latino ancestry |
| nhomalt_amr_female | Integer | Count of homozygous individuals in female samples of Latino ancestry |
| AC_sas_female | Integer | Alternate allele count for female samples of South Asian ancestry |
| AN_sas_female | Integer | Total number of alleles in female samples of South Asian ancestry |
| AF_sas_female | Float | Alternate allele frequency in female samples of South Asian ancestry |
| nhomalt_sas_female | Integer | Count of homozygous individuals in female samples of South Asian ancestry |
| AC_fin | Integer | Alternate allele count for samples of Finnish ancestry |
| AN_fin | Integer | Total number of alleles in samples of Finnish ancestry |
| AF_fin | Float | Alternate allele frequency in samples of Finnish ancestry |
| nhomalt_fin | Integer | Count of homozygous individuals in samples of Finnish ancestry |
| AC_afr_female | Integer | Alternate allele count for female samples of African-American/African ancestry |
| AN_afr_female | Integer | Total number of alleles in female samples of African-American/African ancestry |
| AF_afr_female | Float | Alternate allele frequency in female samples of African-American/African ancestry |
| nhomalt_afr_female | Integer | Count of homozygous individuals in female samples of African-American/African ancestry |
| AC_sas_male | Integer | Alternate allele count for male samples of South Asian ancestry |
| AN_sas_male | Integer | Total number of alleles in male samples of South Asian ancestry |
| AF_sas_male | Float | Alternate allele frequency in male samples of South Asian ancestry |
| nhomalt_sas_male | Integer | Count of homozygous individuals in male samples of South Asian ancestry |
| AC_amr | Integer | Alternate allele count for samples of Latino ancestry |
| AN_amr | Integer | Total number of alleles in samples of Latino ancestry |
| AF_amr | Float | Alternate allele frequency in samples of Latino ancestry |
| nhomalt_amr | Integer | Count of homozygous individuals in samples of Latino ancestry |
| AC_nfe | Integer | Alternate allele count for samples of Non-Finnish European ancestry |
| AN_nfe | Integer | Total number of alleles in samples of Non-Finnish European ancestry |
| AF_nfe | Float | Alternate allele frequency in samples of Non-Finnish European ancestry |
| nhomalt_nfe | Integer | Count of homozygous individuals in samples of Non-Finnish European ancestry |
| AC_eas | Integer | Alternate allele count for samples of East Asian ancestry |
| AN_eas | Integer | Total number of alleles in samples of East Asian ancestry |
| AF_eas | Float | Alternate allele frequency in samples of East Asian ancestry |
| nhomalt_eas | Integer | Count of homozygous individuals in samples of East Asian ancestry |
| AC_ami_male | Integer | Alternate allele count for male samples of Amish ancestry |
| AN_ami_male | Integer | Total number of alleles in male samples of Amish ancestry |
| AF_ami_male | Float | Alternate allele frequency in male samples of Amish ancestry |
| nhomalt_ami_male | Integer | Count of homozygous individuals in male samples of Amish ancestry |
| AC_fin_female | Integer | Alternate allele count for female samples of Finnish ancestry |
| AN_fin_female | Integer | Total number of alleles in female samples of Finnish ancestry |
| AF_fin_female | Float | Alternate allele frequency in female samples of Finnish ancestry |
| nhomalt_fin_female | Integer | Count of homozygous individuals in female samples of Finnish ancestry |
| faf95_afr | Float | Filtering allele frequency (using Poisson 95% CI) for samples of African-American/African ancestry |
| faf99_afr | Float | Filtering allele frequency (using Poisson 99% CI) for samples of African-American/African ancestry |
| faf95_sas | Float | Filtering allele frequency (using Poisson 95% CI) for samples of South Asian ancestry |
| faf99_sas | Float | Filtering allele frequency (using Poisson 99% CI) for samples of South Asian ancestry |
| faf95_adj | Float | (No description from gnomAD) |
| faf99_adj | Float | (No description from gnomAD) |
| faf95_amr | Float | Filtering allele frequency (using Poisson 95% CI) for samples of Latino ancestry |
| faf99_amr | Float | Filtering allele frequency (using Poisson 99% CI) for samples of Latino ancestry |
| faf95_nfe | Float | Filtering allele frequency (using Poisson 95% CI) for samples of Non-Finnish European ancestry |
| faf99_nfe | Float | Filtering allele frequency (using Poisson 99% CI) for samples of Non-Finnish European ancestry |
| faf95_eas | Float | Filtering allele frequency (using Poisson 95% CI) for samples of East Asian ancestry |
| faf99_eas | Float | Filtering allele frequency (using Poisson 99% CI) for samples of East Asian ancestry |


