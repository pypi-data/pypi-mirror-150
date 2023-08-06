

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

.. code-block:: bash

    """
    file is location of the "small_cDNA_Sequences_pbmc_1k_v2_S1_L002_R2_001.fastq" 
    that you downloaded from https://tinyurl.com/cDNALibraryExampleFiles
    if it is in current directory, just use file name
    """
    >>> file = "small_cDNA_Sequences_pbmc_1k_v2_S1_L002_R2_001.fastq"

.. code-block:: bash

    """
    f is the file location and name
    length is the number of sequences we want in our scope
    encoding is one of three choices: "one-hot-encoding", "standard", or "no-encoding"
    bits is one of three choices: 2, 4, or 8
    """
    >>> VECSS = SimSearch.VecSS(f=dir, length=10000, encoding="one-hot-encoding",bits=8)
    >>> sequences = VECSS.readq()

.. code-block:: bash

    # embed produces the vector embedding of the sequence
    >>> embedded = VECSS.embed(VECSS.s)
    >>> print(embedded)

.. code-block:: bash

    """
    similarity search
    I are the indices of the similar sequences
    D are how different the similar sequences are from the query sequence
    time is the time it takes to perform this similarity search query
    """
    >>> D, I, time = VECSS.run_search()
    >>> print(D,I,time)

.. code-block:: bash

    #Testing the embedding and umembedding process
    >>> print(VECSS.unembed(VECSS.embed(VECSS.s)) == VECSS.s)
   'True'
