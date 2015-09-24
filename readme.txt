How to use this program:
  Requirements:
    This program requires Python3 and the basic Python library (urllib was likely included with your installation).
    This program also has an absolute requirement of running on a cluster with a job scheduler like openSGE or similar
    for indexing a genome.  It would likely take days without this.  Searches can be run on a single system, but will
    probably take a long time.
  Setting different modes:
    There are 5 possible modes for this program to run in:
     "selection" will look through either a list of sequences, or a sequence
         passed on the command line, or a FASTA sequence file to find potential
         targets and rank them.
     "index" will search a genome and save any potential targets based on the
         user-defined guide length and PAM sequence.
     "search" will look through an indexed genome for anything matching the
         user-defined target site within the user-defined mismatch tolerance.
     "worker" is a search worker process for parallelizing the search to speed
         it up.  Users generally won't set this unless troubleshooting.
     "FASTAworker" is a worker process for indexing a genome.  Users will
         generally not set this either, unless troubleshooting.
     The mode will always be passed under the -m commandline argument and is always required.
  How to run a job:
    Defining your system:
     Every mode requires the user to define what their system looks like.  This
     will be done by passing either a specific sequence (for searches) or a generic
     sequence (for indexing and site selection).  A generic sequence with a 20bp
     guide RNA will be formatted as NNNNNNNNNNNNNNNNNNNN_PAM or can be written as
     20_PAM with PAM being the PAM sequence.  PAM sequences can, and often will,
     have at least one degenerate nucleotide in them.  The guide and PAM must be
     separated with an underscore.  For indexing a system that can take multiple
     lengths of gRNA, index the longest possible version (and even a little extra),
     as that same indexed genome can be used for shorter versions as well.  A
     specific sequence will be required for search jobs.  That is defined the same
     way, except that the N's in the gRNA portion will be replaced by your actual
     sequence.  The sequence will be passed under the -s commandline argument.
   Selecting your genome:
     Every job will require passing a genome argument.  This argument will be
     passed as -g GENOME.  For indexing, this will define the name of the genome
     (such as HG38).  Genome names can be arbitrary, but should be informative
     and easy to remember, as that name will be used to select it for searching
     in the future.
   Selecting a species:
     You will need to choose a species for your genome when indexing it.  In order
     to get back information regarding genes associated with a target or mismatch
     site, please be sure that the species name given is the same as is used by the
     Ensembl servers.
   Site selection:
     This requires the user to define a target sequence, which can either be in a
     file (passed as --targetFasta [filename] or directly as
     --targetSequence [sequence]).  Alternatively, the user can pass a list of
     already-determined target sites in a file as --targetList [filename] with one
     potential target site per line.  This also requires the user to define their
     system as described above.  The genome name is also required and can be passed
     under the -g argument.  Optional arguments include mismatch tolerance (-t,
     default value of 3) and parallel jobs per search (-p, default of 10).
     Azimuth analysis can be skipped entirely by passing --skipAzimuth.
     SAMPLE COMMANDLINE:
     dsNickFuryX.X.py -m selection -s 20_NGAG -g hg38 --targetFasta file.fa
   Mismatch search:
     This requires the user to define their system, as described above (passed as
     the -s argument and using a specific sequence instead of generic).  This also
     requires the user to define which genome they wish to search (passed as the -g
     argument).  The program will search the folder of indexed genomes for a
     suitable one (having a compatible PAM sequence, and a guide RNA of equal or
     greater length).  Optional arguments include the number of parallel jobs for
     the search (passed as -p with a default of 20) and mismatch tolerance (passed
     as -t with a default of 3).
     SAMPLE COMMANDLINE:
     dsNickFuryX.X.py -m search -s GATTACAGATTACAGAATTC_TGG -g hg38
   Genome index:
     This will be done for every genome/system combination unless a suitable
     indexed genome already exists (one with the same PAM and longer gRNA size).
     The indexing will gather information about target frequency between contigs
     and will also generate files listing these target sequences.  This speeds up
     the search process tremendously.  The user will have to define a generic
     target sequence for their system (as described above, passed under the -s
     argument as always).  They will also need to state which species the genome
     is from (passed as --species).  The stated species should use the same name
     as is listed in ensembl's website.  A FASTA formatted sequence is required for
     indexing.  This is passed under the -f argument.  The FASTA file needs to have
     been indexed (a companion .fai file generated) by SAMtools or another
     equivalent FASTA indexer.  Optional arguments include --ordered, which
     will generate only a single parallel job per contig.  Users can set the chunk
     size for parallel chromosome indexing.  With more nodes available for
     computing, a smaller chunksize can decrease the time required before indexing
     is complete.  This can be passed as --chunkSize INT, with INT representing an
     integer value.  If a value less than 100 is passed, it will be assumed to mean
     megabases.  To avoid causing conflicts with your cluster, the program may
     automatically increase your chunk size to avoid creating too many parallel
     jobs at once (this is useful to speed up processing on smaller genomes).  In
     order to ignore/overwrite an existing suitable genome or use a species name
     not listed on ensembl, run the indexing with command option -9 or --clobber.
     SAMPLE COMMANDLINE:
     dsNickFuryX.X.py -m index -f hg38.fa -g hg38 --species Human -s NNNNNNNNNNNNNNNNNNNN_NGG
  Azimuth analysis:
    In order to run an analysis using Azimuth, you will need an API key stored in the same
    directory as this program in file azimuth.apikey.  If you are not using the standard NGG
    Cas9/Crispr system, this program will try to force your sites to fit into their model.
    Because of this, the predictions may not be accurate.
