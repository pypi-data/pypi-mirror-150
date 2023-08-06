.. raw:: html

    <style> .navy {color:navy} </style>
	
.. role:: navy

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

.. raw:: html

    <style> .green {color:green} </style>
    <style> .blue {color:blue} </style>
    <style> .red {color:red} </style>

.. role:: green
.. role:: blue
.. role:: red


.. _SMAPinstallationquickstart:


############
Installation
############

Install the SMAP package and download the tutorial data from Zenodo.

The latest release of the SMAP-package can be found on the `Gitlab repository <https://gitlab.com/truttink/smap/-/releases/>`_, where `INSTALL.md <https://gitlab.com/truttink/smap/-/blob/master/INSTALL.md>`_ describes the installation guidelines.
Running SMAP on GBS data requires special preprocessing of reads before read mapping. Please use instructions and software for GBS read preprocessing as described in the manual of `GBprocesS <https://gbprocess.readthedocs.io/en/latest/index.html>`_. 

Quick installation in a virtual environment::

    git clone https://gitlab.com/truttink/smap.git
    cd smap
    git checkout master
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install .
    cd ..
    git clone https://gitlab.com/dschaumont/smap-haplotype-window
    cd smap-haplotype-window
    git checkout master
    pip install .

or, using pip::

    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install ngs-smap
    pip install smap-haplotype-window

Or, using Docker::

    docker run dschaumont/smap --help
    
| SMAP is only available for linux operating systems.
| A basic guide for running software on the linux command line can be found on `Ubuntu <https://ubuntu.com/tutorials/command-line-for-beginners#1-overview>`_'s site.

----

##############################
Analysis of simulated GBS data
##############################

Activate your virtual environment ::

	source .venv/bin/activate

Define the path to the download directory::

	download_dir=$/PATH/TO/DOWNLOAD_DIR/
	or (from the download dir itself):
	download_dir=$(pwd)

SMAP delineate
~~~~~~~~~~~~~~

Create and navigate to a new output directory to run **SMAP delineate** on the BAM files with mapped GBS reads::

	mkdir -p $download_dir/Simulated_data/SMAP_delineate/output/
	cd $download_dir/Simulated_data/SMAP_delineate/output/
	smap delineate $download_dir/Simulated_data/SMAP_delineate/input/ -mapping_orientation ignore --processes 8 --plot all --plot_type pdf --min_stack_depth 2 --max_stack_depth 1500 --min_cluster_length 50 --max_cluster_length 300 --max_stack_number 20 --min_stack_depth_fraction 10 --min_cluster_depth 10 --max_cluster_depth 1500 --max_smap_number 20 --name GBS 


SMAP haplotype-sites
~~~~~~~~~~~~~~~~~~~~

Create and navigate to a new output directory to run **SMAP haplotype-sites** on the BAM files with mapped GBS reads, its BED file from **SMAP delineate**, and a VCF file with SNP calls (See for third-party SNP calling software: `SAMtools <http://www.htslib.org/>`_, `BEDtools <https://bedtools.readthedocs.io/en/latest/index.html>`_, `Freebayes <https://github.com/ekg/freebayes>`_, or `GATK <https://gatk.broadinstitute.org/hc/en-us>`_).::

	mkdir -p $download_dir/Simulated_data/SMAP_haplotype_sites/output
	cd $download_dir/Simulated_data/SMAP_haplotype_sites/output 
	smap haplotype-sites $download_dir/Simulated_data/SMAP_delineate/input/ $download_dir/Simulated_data/SMAP_delineate/output/final_stack_positions_GBS_C0_SMAP20_CL50_300.bed $download_dir/Simulated_data/SMAP_haplotype_sites/input/snps.vcf --out prefix -mapping_orientation ignore --discrete_calls dosage --frequency_interval_bounds diploid --dosage_filter 2 --plot all --plot_type pdf -partial include --min_distinct_haplotypes 2 --min_read_count 10 --min_haplotype_frequency 5 --processes 8

Deactivate your virtual environment::

	deactivate

----

#########################
Analysis of real GBS data
#########################

Activate your virtual environment ::

	source .venv/bin/activate

Define the path to the download directory::

	download_dir=$/PATH/TO/DOWNLOAD_DIR/
	or (from the download dir itself):
	download_dir=$(pwd)

SMAP delineate
~~~~~~~~~~~~~~

Create and navigate to a new output directory to run **SMAP delineate** on the BAM files with mapped GBS reads of a set of **individuals**::

	mkdir -p $download_dir/Real_data/SMAP_delineate/output/ind
	cd $download_dir/Real_data/SMAP_delineate/output/ind/
	smap delineate $download_dir/Real_data/SMAP_delineate/input/ind/ -mapping_orientation ignore --processes 8 --plot all --plot_type pdf --min_stack_depth 2 --max_stack_depth 1500 --min_cluster_length 50 --max_cluster_length 300 --max_stack_number 20 --min_stack_depth_fraction 10 --min_cluster_depth 10 --max_cluster_depth 1500 --max_smap_number 20 --name 48_ind_GBS-PE 

Create and navigate to a new output directory to run **SMAP delineate** on the BAM files with mapped GBS reads of a set of **pool samples**::

	mkdir -p $download_dir/Real_data/SMAP_delineate/output/pools
	cd $download_dir/Real_data/SMAP_delineate/output/pools/
	smap delineate $download_dir/Real_data/SMAP_delineate/input/pools/ -mapping_orientation ignore --processes 8 --plot all --plot_type pdf --min_stack_depth 2 --max_stack_depth 1500 --min_cluster_length 50 --max_cluster_length 300 --max_stack_number 20 --min_stack_depth_fraction 5 --min_cluster_depth 30 --max_cluster_depth 1500 --max_smap_number 20 --name 16_pools_GBS-PE 


SMAP compare
~~~~~~~~~~~~

Create and navigate to a new output directory to run **SMAP compare** on the two BED files with MergedClusters generated by **SMAP delineate**::

	mkdir $download_dir/Real_data/SMAP_compare/output 
	cd $download_dir/Real_data/SMAP_compare/output
	smap compare $download_dir/Real_data/SMAP_delineate/output/ind/final_stack_positions_48_ind_GBS-PE_C0_SMAP20_CL50_300.bed $download_dir/Real_data/SMAP_delineate/output/pools/final_stack_positions_16_pools_GBS-PE_C0_SMAP20_CL50_300.bed 


SMAP haplotype-sites
~~~~~~~~~~~~~~~~~~~~

Create and navigate to a new output directory to run **SMAP haplotype-sites** on the BAM files with mapped GBS reads of a set of **individuals**, its BED file from **SMAP delineate**, and a VCF file with SNP calls (See for third-party SNP calling software: `SAMtools <http://www.htslib.org/>`_, `BEDtools <https://bedtools.readthedocs.io/en/latest/index.html>`_, `Freebayes <https://github.com/ekg/freebayes>`_, or `GATK <https://gatk.broadinstitute.org/hc/en-us>`_ for individuals).::

	mkdir -p $download_dir/Real_data/SMAP_haplotype_sites/output/ind
	cd $download_dir/Real_data/SMAP_haplotype_sites/output/ind 
	smap haplotype-sites $download_dir/Real_data/SMAP_delineate/input/ind/ $download_dir/Real_data/SMAP_delineate/output/ind/final_stack_positions_48_ind_GBS-PE_C0_SMAP20_CL50_300.bed $download_dir/Real_data/SMAP_haplotype_sites/input/48_ind_GBS-PE.vcf --out haplotypes_48_ind_GBS-PE -mapping_orientation ignore --discrete_calls dosage --frequency_interval_bounds diploid --dosage_filter 2 --plot all --plot_type pdf -partial include --min_distinct_haplotypes 2 --min_read_count 10 --min_haplotype_frequency 5 --processes 8


Create and navigate to a new output directory to run **SMAP haplotype-sites** on the BAM files with mapped GBS reads of a set of **pool samples**, its BED file from **SMAP delineate**, and a VCF file with SNP calls (See for third-party SNP calling software: `SNAPE-pooled <https://github.com/EmanueleRaineri/snape-pooled>`_ for Pool-Seq data).::

	mkdir -p $download_dir/Real_data/SMAP_haplotype_sites/output/pools
	cd $download_dir/Real_data/SMAP_delineate/output/pools/
	smap haplotype-sites $download_dir/Real_data/SMAP_delineate/input/pools/ $download_dir/Real_data/SMAP_delineate/output/pools/final_stack_positions_16_pools_GBS-PE_C0_SMAP20_CL50_300.bed $download_dir/Real_data/SMAP_haplotype_sites/input/48_ind_GBS-PE.vcf --out haplotypes_16_pools_GBS-PE -mapping_orientation ignore --plot all --plot_type pdf --mask_frequency 1 --undefined_representation "" -partial include --min_distinct_haplotypes 2 --min_read_count 30 --min_haplotype_frequency 5 --processes 8

Deactivate your virtual environment::

	deactivate

----

###########################################
Analysis of real CRISPR genome editing data
###########################################

Activate your virtual environment::

	source .venv/bin/activate

Define the path to the download directory::

	download_dir=$/PATH/TO/DOWNLOAD_DIR/
	or (from the download dir itself):
	download_dir=$(pwd)

SMAP haplotype-window
~~~~~~~~~~~~~~~~~~~~~

Create and navigate to a new output directory to run **SMAP haplotype-window** on a set of FASTQ files with HiPlex reads, their mapped BAM files, its GFF file with border positions and a gRNA FASTA file from **SMAP design**:: 

	mkdir -p $download_dir/Real_data/SMAP_haplotype_window/output
	cd $download_dir/Real_data/SMAP_haplotype_window/output
	smap haplotype-window $download_dir/Real_data/SMAP_haplotype_window/input/reference.fasta $download_dir/Real_data/SMAP_haplotype_window/input/borders.gff $download_dir/Real_data/SMAP_haplotype_window/input/ $download_dir/Real_data/SMAP_haplotype_window/input/ --mask_frequency 2 --undefined_representation "" --min_read_count 30 --min_haplotype_frequency 5 --processes 8

Deactivate your virtual environment::

	deactivate

