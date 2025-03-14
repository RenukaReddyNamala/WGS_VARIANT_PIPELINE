import os
import subprocess

# Define directories
raw_reads = "sample_data/"
trimmed_reads = "trimmed/"
aligned_reads = "aligned/"
variants = "variants/"
qc_reports = "qc_reports/"
reference_genome = "reference.fasta"

# Ensure directories exist
for directory in [trimmed_reads, aligned_reads, variants, qc_reports]:
    os.makedirs(directory, exist_ok=True)

def run_fastqc():
    """Run FastQC for quality control."""
    print(" Running FastQC...")
    subprocess.run(["fastqc", raw_reads + "*.fastq.gz", "-o", qc_reports])

def trim_reads():
    """Trim low-quality reads using Trimmomatic."""
    print(" Trimming reads with Trimmomatic...")
    subprocess.run(["java", "-jar", "/path/to/trimmomatic.jar", "PE", "-phred33",
                    raw_reads + "sample_R1.fastq.gz", raw_reads + "sample_R2.fastq.gz",
                    trimmed_reads + "R1_paired.fastq.gz", trimmed_reads + "R1_unpaired.fastq.gz",
                    trimmed_reads + "R2_paired.fastq.gz", trimmed_reads + "R2_unpaired.fastq.gz",
                    "ILLUMINACLIP:TruSeq3-PE.fa:2:30:10", "SLIDINGWINDOW:4:20", "MINLEN:50"])

def align_reads():
    """Align reads to the reference genome using BWA."""
    print(" Aligning reads with BWA...")
    subprocess.run(["bwa", "mem", reference_genome, 
                    trimmed_reads + "R1_paired.fastq.gz",
                    trimmed_reads + "R2_paired.fastq.gz"], stdout=open(aligned_reads + "sample.sam", "w"))

def convert_sam_to_bam():
    """Convert SAM to BAM and sort."""
    print(" Converting SAM to BAM...")
    subprocess.run(["samtools", "view", "-Sb", aligned_reads + "sample.sam", "-o", aligned_reads + "sample.bam"])
    subprocess.run(["samtools", "sort", "-o", aligned_reads + "sample_sorted.bam", aligned_reads + "sample.bam"])

def call_variants():
    """Call variants using GATK HaplotypeCaller."""
    print(" Calling variants with GATK...")
    subprocess.run(["gatk", "HaplotypeCaller", "-R", reference_genome, 
                    "-I", aligned_reads + "sample_sorted.bam",
                    "-O", variants + "sample_variants.vcf"])

def run_gwas():
    """Run GWAS analysis using PLINK."""
    print(" Running GWAS with PLINK...")
    subprocess.run(["plink", "--vcf", variants + "sample_variants.vcf",
                    "--assoc", "--out", "results/gwas_results"])

if __name__ == "__main__":
    run_fastqc()
    trim_reads()
    align_reads()
    convert_sam_to_bam()
    call_variants()
    run_gwas()
    print(" Pipeline Execution Completed.")
