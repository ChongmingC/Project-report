### 1 Calculating Copy Number 

I take one sample as an example.

#### 1.1 Slicing

```bash
# Extract reads mapped to scaffold chrUn_GL000220v1 and output as a SAM file
samtools view -h "$input_bam" chrUn_GL000220v1 > "$output_sam_dir/$output_gl000220"

# Extract reads mapped to the chr1 region (chr1:226743523-231781906) and output as a SAM file
samtools view -h "$input_bam" chr1:226743523-231781906 > "$output_sam_dir/$output_chr1"

# Convert the SAM file of the GL000220v1 region to FASTQ format
samtools fastq "$output_sam_dir/$output_gl000220" > "$output_fastq_dir/$output_fastq_gl000220"

# Convert the SAM file of the chr1 region to FASTQ format
samtools fastq "$output_sam_dir/$output_chr1" > "$output_fastq_dir/$output_fastq_chr1"
```

#### 1.2 Mapping

**Indexing the Reference:**

```bash
bwa index 45S.fasta
bwa index 5S.fasta
```

**Mapping Reads:**

```bash
bwa mem TCGA-**-****-**A_1q42.fastq > TCGA-**-****-**A_1q42_5S.sam

bwa mem 45S.fasta TCGA-**-****-**A_GL000220v1.fastq > TCGA-**-****-**A_GL000220v1_45S.sam
```

**Filter Reads with FLAG 0 or 16:**

```bash
awk '($1 ~ /^@/) || ($2 == 0 || $2 == 16)' "$sam_file" > "$output_file"
```

#### 1.3 Calculation

**Convert SAM to BAM:**

```bash
samtools view -h -Sb TCGA-**-****-**A_GL000220v1_45S_f0_16.sam > TCGA-**-****-**A_GL000220v1_45S_f0_16.bam
```

**Sort BAM Files:**

```bash
samtools sort TCGA-**-****-**A_GL000220v1_45S_f0_16.bam -o TCGA-**-****-**A_GL000220v1_45S_f0_16.sorted.bam
```

**Index BAM Files:**

```bash
samtools index TCGA-**-****-**A_GL000220v1_45S_f0_16.sorted.bam
```

**Calculate Per-Base Depth:**

```bash
samtools depth -a TCGA-**-****-**A_GL000220v1_45S_f0_16.sorted.bam > TCGA-**-****-**A_45s_depth.txt
```

---

### 2. Ploidy Correction for Tumor Samples
Refer to the code in `ploidy_correction.Rmd`.

### 3. Calculate BRD
Refer to the code in `batch_BRD_average_results.py`.

### 4. Minimum Coefficient of Variation (CV) of Average Depth Across Samples
Refer to the code in `depth_min_CV.ipynb`.

### 5. Clinical Outcome Analysis
Refer to the code in `analysis_results_images`.

### 6. Cox Proportional-Hazards (CoxPH) Model
Refer to the code in `coxph.Rmd`.

