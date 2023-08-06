

GeneVecTools
===============
Reading in Variety of Genetic File Types

Vector Embedding Algorithms

Byte Array Encoders

Clustering and Preprocessing Steps for Compression

Similarity Search Tools for FASTA/FASTQ files

Installing

Tester files: https://tinyurl.com/cDNALibraryExampleFiles
============

.. code-block:: bash

    pip install GeneVecTools

Usage
=====

.. code-block:: bash

    >>> from GeneVecTools import SimSearch
    # file is location of the "small_cDNA_Sequences_pbmc_1k_v2_S1_L002_R2_001.fastq" 
    # that you downloaded from https://tinyurl.com/cDNALibraryExampleFiles
    # if it is in current directory, just use file name
    >>> file = "small_cDNA_Sequences_pbmc_1k_v2_S1_L002_R2_001.fastq"
    >>> VECSS = SimSearch.VecSS(dir)
    >>> sequences = VECSS.readq()

    >>> embedded = VECSS.embed(VECSS.s)
    >>> print(embedded )

    >>> D, I, time = VECSS.run_search()
    >>> print(D,I,time)

    >>> print(VECSS.unembed(VECSS.embed(VECSS.s)) == VECSS.s)
   'True'